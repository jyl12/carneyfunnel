import time
import serial
import datetime
import os
from pynput.keyboard import Key, Controller
import keyboard
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# Service modules
import analysis.main 
import state_data_storage.main
import data_collection.weighing
import data_collection.scanner

#General settings
count = 0
carney, hall = range (0,2)
FUNNEL = carney #funnel type: carney or hall
USER_INPUT = 1 #1:enable user input; 0:disable user input
CERTIFIED_CUP_VOLUME = 100.20 #certified cup volume

#GPIO settings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pin = 21 #Light sensor pin: pin GPIO 21
ledpin = 20 #Laser pin: pin GPIO 20
# Setup pin in and out directions
GPIO.setup(pin, GPIO.IN)
GPIO.setup(ledpin, GPIO.OUT)

def laser_detector(pin):
    #Turn on the laser
    GPIO.output(ledpin, GPIO.HIGH)
    # Delay for laser to activate
    time.sleep(0.1)
    # Read the light sensor value and print it to terminal
    # print('Light sensor value: ',GPIO.input(pin))
    # Read light sensor and display status
    if GPIO.input(pin) == 1:
#         print('Laser detected.')
        laser = 1 
    else:
#         print('Laser not detected.')
        laser = 0
    return laser
    
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

if __name__ == "__main__":
    step = 1
    print('---Booting up---')
    ##### communication not stable
#     analysis.main.Communication()
#     time.sleep(1)
#     print('main')
#     Communication()
    #####
#     weigh = data_collection.weighing.ServiceDataCollection()
#     weigh.start()
#     data_collection.scanner.Scanner().start() #camera
#     state_data_storage.main.start()
    print('---Ready---')
    if FUNNEL == carney:
        print('---Carney funnel selected.---')
    elif FUNNEL == hall:
        print('---Hall funnel selected.---')
    if USER_INPUT == 0:
        print('---User input disabled.---')
    elif USER_INPUT == 1:
        print('---User input enabled.---')
#     while True:
#         try:
#             FUNNEL = int(input('Choose funnel type [0:Carney, 1:Hall]: '))
#             if FUNNEL == carney:
#                 print('---Carney funnel selected.---')
#                 break
#             elif FUNNEL == hall:
#                 print('---Hall funnel selected.---')
#                 break
#             else:
#                 raise ValueError
#         except ValueError:
#             print('Please enter 0 or 1.')
#     while True:
#         try:
#             USER_INPUT = int(input('User input method [0:Disable, 1:Enable]: '))
#             if USER_INPUT == 0:
#                 print('---User input disabled.---')
#                 break
#             elif USER_INPUT == 1:
#                 print('---User input enabled.---')
#                 break
#             else:
#                 raise ValueError
#         except ValueError:
#             print('Please enter 0 or 1.')
    print('Please enter/scan a batch code.')
    while True:
        if step == 1:
            if USER_INPUT == 1:
                    batch_code = input("Enter batch code: ")
                    step = 2
            else:
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
                if USER_INPUT == 1:
                    weight_powder = float(input("Enter powder mass (gram): "))
                    print("Powder mass (gram): ", weight_powder)
                    step = 3
                    print('Stopwatch ready, release the powder.')
                else:
                    weigh.weight = 0
                    print('Enter powder mass:')
                    while weigh.weight == 0:
                        weight_powder = weigh.weight
                    weight_powder = weigh.weight
                    weigh.weight = 0
                    print("Powder mass (gram): ", weight_powder)
                    step = 3
                    print('Stopwatch ready, release the powder.')
            except ValueError:
                print("That's not a number.")
        elif step == 3:
            laser = laser_detector(pin)
            while laser == 1:
                laser = laser_detector(pin)
                start_time = time.time()
            print('Stopwatch started: ',datetime.datetime.now())
            while laser == 0:
                laser = laser_detector(pin)
                time.sleep(0.02)
                while laser == 1:
                    count += 1
                    if count == 5:
                        count = 0
                        break
            end_time = time.time()
            duration = end_time - start_time  
            if FUNNEL == carney:
                print('Duration (second): ', duration)
                flowrate = analysis.main.ServiceAnalysis.flowrate(duration, weight_powder)
                print('Flowrate (gram/second): ',flowrate)
                step = 4
            elif FUNNEL == hall:
                duration = 1.1 * duration
                print('Corrected duration (second): ', duration)
                flowrate = analysis.main.ServiceAnalysis.flowrate(duration, weight_powder)
                print('Flowrate (gram/second): ',flowrate)
                step = 4
            else:
                pass
        elif step == 4:
            try:
                if USER_INPUT == 1:
                    weight_scrapecup = float(input("Enter powder mass of scraped cup (gram): "))
                    print("Powder mass of scraped cup (gram): ", weight_scrapecup)
                    apparent_density = analysis.main.ServiceAnalysis.apparent_density(weight_scrapecup, CERTIFIED_CUP_VOLUME)
                    print('Apparent density (gram/cm3): ', apparent_density)
                    step = 5
                else:
                    weigh.weight = 0
                    print('Enter powder mass of scraped cup:')
                    while weigh.weight == 0:
                        weight_scrapecup = weigh.weight
                    weight_scrapecup = weigh.weight
                    weigh.weight = 0
                    print("Powder mass of scraped cup (gram): ", weight_scrapecup)
                    apparent_density = analysis.main.ServiceAnalysis.apparent_density(weight_scrapecup, CERTIFIED_CUP_VOLUME)
                    print('Apparent density (gram/cm3): ', apparent_density)
                    step = 5
            except ValueError:
                print("That's not a number.")
        elif step == 5:
#             state_data_storage.main.Temp1.set_value(time.ctime(int(start_time)))
#             state_data_storage.main.Temp2.set_value(batch_code)
#             state_data_storage.main.Temp3.set_value(round(flowrate,6))
#             state_data_storage.main.Temp4.set_value(round(apparent_density,6))
#             state_data_storage.main.write_csv('record_file',start = time.ctime(int(start_time)),
#                                               batch = batch_code,
#                                               duration = round(duration,6),
#                                               flowrate = round(flowrate,6),
#                                               apparentdensity = round(apparent_density,6))
            step = 1
            print('----------')
            print('Please enter/scan a batch code.')
        else:
            pass

        
        
