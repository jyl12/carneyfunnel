import os
import re
import sys
import time
import datetime

from string import Template

import asyncio
import evdev

from KeyParser import KeyParser

__dt = -1 * (time.timezone if (time.localtime().tm_isdst == 0) else time.altzone)
tz = datetime.timezone(datetime.timedelta(seconds = __dt))

class BarcodeScanner:
    def __init__(self,config,service_config):
        #config
        self.location = service_config.get('location',"location_not_set")
        self.service_id = service_config.get('id',"error_id_not_set")

        self.scanner_serial = config.get('serial',"")
        self.connection_point = config.get('connection_point',['*'])
        self.scanner_modes = config.get('mode_barcodes',{})
        self.mode_text_dict = config.get('mode_text',{})

        self.mode_change_topic = config.get('mode_change_topic','')
        self.mode_change_format = config.get('mode_change_format','')
        #'{"mode_changed_to":"$mode"}'
        
        self.barcode_topic_template = config.get('barcode_topic_template','topic_not_set')
        self.barcode_match_re = config.get('barcode_match_re','')
        self.barcode_event_format = config.get('barcode_event_format','')

        #setup
        self.mode = list(self.scanner_modes.values())[0]
        self.parser = KeyParser.Parser()

        while(self.find_scanner()==False):
            time.sleep(2)
       
        self.grab_exclusive_access()

    def find_scanner(self):
        try:
            import pyudev
            print("BS> pyudev version: {vsn}".format(vsn=pyudev.__version__))
            print("BS> udev version: {vsn}".format(vsn=pyudev.udev_version()))
        except ImportError:
            print("BS> Unable to import pyudev. Ensure that it is installed",file=sys.stderr)
            exit(0)

        self.udev_ctx = pyudev.Context()
        
        print("BS> looking for barcode reader with serial number {sn} on connection point {cp}".format(sn=self.scanner_serial,cp=self.connection_point))

        for dev in self.udev_ctx.list_devices(subsystem='input', ID_BUS='usb'):
            if dev.device_node is not None:
                
                try:
                    if dev.properties['ID_INPUT_KEYBOARD'] == "1" and ( dev.properties['ID_SERIAL'] == self.scanner_serial or f"{dev.properties['ID_VENDOR_ID']}_{dev.properties['ID_MODEL_ID']}" == self.scanner_serial ):
                        if self.connection_point[0] != '*':
                            _, connection_point = dev.properties['ID_PATH'].split('-usb-')
                            cp_entries = connection_point.split(':')
                            match = True
                            for i in range(0,len(self.connection_point)):
                                if self.connection_point[i] != cp_entries[i]:
                                    match = False
                                    break
                            if not match:
                                continue

                        print('BS> Scanner found')
                        self.scanner_device=evdev.InputDevice(dev.device_node)
                        return True;
                except Exception as e:
                    print("exception>")
                    print(e)
        
        print("BS> Error: Scanner not found", file=sys.stderr)
        
        for dev in self.udev_ctx.list_devices(subsystem='input', ID_BUS='usb'):
            if dev.device_node is not None:
                
                try:
                    if dev.properties['ID_INPUT_KEYBOARD'] == "1":
                        _, connection_point = dev.properties['ID_PATH'].split('-usb-')
                        print(f"available: {dev.properties['ID_SERIAL']} or {dev.properties['ID_VENDOR_ID']}_{dev.properties['ID_MODEL_ID']} on connection point {connection_point.split(':')}")
                except Exception as e:
                    print(e)
        
        time.sleep(5)

        return False

    def grab_exclusive_access(self):
        self.scanner_device.grab()

    def mode_change_barcode(self,barcode):
        if barcode in self.scanner_modes:
            self.set_mode(self.scanner_modes[barcode])
            return True
        return False
        
    def mode_change_command(self,q_in):
        mode_set=False            
        try:
            while True:
                msg_in = q_in.get_nowait()
                if msg_in.payload in self.scanner_modes.values():
                    self.set_mode(msg_in)
                    mode_set = True
        except asyncio.QueueEmpty:
            pass
        return mode_set

    def set_mode(self,mode):
        print("BS> mode set to "+ mode)
        self.mode = mode

    async def key_event_loop(self):
        #handles key events from the barcode scanner
        async for event in self.scanner_device.async_read_loop():
            if event.type == 1: #key event
                self.parser.parse(event.code,event.value)
                #print("code ",event.code," value ",event.value)
                if self.parser.complete_available():
                    msg_content = self.parser.get_next_string()
                    #print("complete string >",msg_content)
                    timestamp = (datetime.datetime.fromtimestamp(event.sec,tz=tz)+ datetime.timedelta(microseconds=event.usec)).isoformat()
                    yield {'content':msg_content,'ts':timestamp}
                    
    async def scan_loop(self,q_out,q_in):
        #handles complete scans deom the key_event_loop
        async for scan in self.key_event_loop():
            scan_code = scan['content']
            mc_barcode = self.mode_change_barcode(scan_code)
            mc_command = self.mode_change_command(q_in)
            if mc_barcode or mc_command:
                #todo format
                t = Template(self.mode_change_format)
                payload = t.substitute(mode=self.mode)
                await self.mqtt_send(q_out,self.mode_change_topic,payload)
            
            if not mc_barcode:
                bc_match = re.search(self.barcode_match_re,scan_code)
                if bc_match:
                    bc_data = bc_match.group(1)
                    mode_text = self.mode_text_dict[self.mode]
                    t = Template(self.barcode_event_format)
                    timestamp = scan['ts']
                    payload = t.substitute(bc_data=bc_data,location=self.location,timestamp=timestamp,mode_text=mode_text)
                    #print(payload)
                    t = Template(self.barcode_topic_template)
                    topic = t.substitute(service_id=self.service_id,location=self.location,mode=self.mode)
                    await self.mqtt_send(q_out,topic,payload)
                else:
                    print("BS> barcode {0} did not match template and was ignored".format(scan_code),file=sys.stderr)
    


    async def mqtt_send(self,q_out,topic,payload):
        msg = {'topic':topic,'payload':payload}
        print("BS> putting msg {msg} onto queue".format(msg=msg))
        await q_out.put(msg)

#async def main(loop):
#    x = BarcodeScanner()
#    t = asyncio.create_task(x.read())
#    await t


#loop = asyncio.get_event_loop()
#loop.run_until_complete(main(loop))
