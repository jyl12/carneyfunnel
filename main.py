import time
import serial
import datetime
import os
import paho.mqtt.client as mqtt

import analysis.main 
import state_data_storage.main
import data_collection.main
import data_collection.scanner

USER_INPUT = 1

class Communication (object):
    def __init__(self, message = None):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect('127.0.0.1', 1883, 60)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.loop_start()
        print('init')
        self.run()
    
    def on_connect (self, client, userdata, flags, rc):
        if rc == 0:
            print ('Connected to broker.')
        else:
            print ('Connection failed.')
        self.mqtt_client.subscribe("analysis/main")
        
    def on_disconnect(self, client, userdata, flags, rc):
        self.mqtt_client.reconnect()
        
    def on_message(self, client, userdata, message):
        print('on message')
        print('received:',str(message.payload.decode('utf-8')))
        message_payload = str(message.payload.decode('utf-8'))
        if message.topic == 'analysis/main':
            print('from analysis message')
    def run(self):
        self.mqtt_client.publish('analysis/main','feasfds')
        print('run')
        time.sleep(4)
laser = 1
if __name__ == "__main__":
    step = 1
    print('---Booting up---')
    ##### communication not stable
#     analysis.main.Communication()
#     time.sleep(1)
#     print('main')
#     Communication()
    #####
#     data_collection.main.ServicDataCollection.usb_scale()
    data_collection.scanner.Scanner().start()
#     state_data_storage.main.start()
    print('---Ready---')
    while True:
        if step == 1:
            with open('data_collection/barcode_result.txt', 'r+') as f:
                if os.stat('data_collection/barcode_result.txt').st_size == 0:
                    pass
                else:
                    batch_code = f.readline()
                    print("Batch code is: " + batch_code)
                    time.sleep(5)
                    f.truncate(0)
                    step = 2
#          weight_emptycup = ser.readline()
        elif step == 2:
            try:
                weight_powder = float(input("Enter powder mass (gram): "))
                print("Powder mass (gram): ", weight_powder)
                step = 3
            except ValueError:
                print("That's not a number.")
        elif step == 3:
            while laser == 1:
                laser = float(input("Enter laser: "))
                time.sleep(0.02)
                start_time = time.time()
            print('Stopwatch started: ',datetime.datetime.now())
            while laser == 0:
                time.sleep(0.02)
                while laser == 1:
                    count += 1
                    if count == 5:
                        break
                laser = float(input("Enter laser: "))
            end_time = time.time()
            duration = end_time - start_time
            print('Duration (second): ', duration)
            flowrate = analysis.main.ServiceAnalysis.flowrate(duration, weight_powder)
            print('Flowrate (second/gram): ',flowrate)
            step = 4
        elif step == 4:
            try:
                weight_scrapecup = float(input("Enter powder mass of scraped cup (gram): "))
                print("Powder mass of scraped cup (gram): ", weight_scrapecup)
                apparent_density = analysis.main.ServiceAnalysis.apparent_density(weight_scrapecup, weight_powder)
                print('Apparent density (gram/cm3): ', apparent_density)
                step = 5
            except ValueError:
                print("That's not a number.")
        elif step == 5:
#             state_data_storage.main.Temp1.set_value(time.ctime(int(start_time)))
#             state_data_storage.main.Temp2.set_value(batch_code)
#             state_data_storage.main.Temp3.set_value(round(flowrate,6))
#             state_data_storage.main.Temp4.set_value(round(apparent_density,6))
#             state_data_storage.main.write_csv('file',start = time.ctime(int(start_time)),
#                                               batch = batch_code,
#                                               duration = round(duration,6),
#                                               flowrate = round(flowrate,6),
#                                               apparentdensity = round(apparent_density,6))
            step = 1
        else:
            pass

        
        
