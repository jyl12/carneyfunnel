#!/usr/bin/env python3

import serial
import re
import threading

class ServiceDataCollection(object):
    def __init__(self):     
        self.weight = 0
        self.ser = serial.Serial(
         port='/dev/ttyUSB0', #'/dev/ttyUSB0', /dev/ttyACM0'
         baudrate = 9600,
         parity=serial.PARITY_ODD,
         stopbits=serial.STOPBITS_ONE,
         bytesize=serial.SEVENBITS,
         timeout=None
        )
        self.ser.flush()
        
    def start(self):
        t = threading.Thread(target = self.run)
        t.daemon = True
        t.start()
        
    def run(self):
#         print('usbweight')
#         while True:
#             self.weight = input("try: ")
        while True:
            raw = self.ser.readline()
            w = raw.decode('UTF-8')
            self.weight = (re.findall(r"[-+]?\d*\.?\d+|\d+", w))
            self.weight = float(self.weight[0])
            
    def read(self):
        raw = ser.readline()
        w = raw.decode('UTF-8')
        weight = (re.findall(r"[-+]?\d*\.?\d+|\d+", w))
        weight = float(weight[0])       
        return weight        

if __name__ == "__main__":
    ser = serial.Serial('/dev/ttyACM0', 9600,
                        parity=serial.PARITY_ODD,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.SEVENBITS,
                        timeout=1)
    ser.flush()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            
#     print('analysis main')
#     my_string_two = b'+   123.56 g  /r/n'
#     print(my_string_two.decode('UTF-8'))
#     my_string_two = my_string_two.decode('UTF-8')
#     print(re.findall(r"[-+]?\d*\.?\d+|\d+", my_string_two))
#     weight = (re.findall(r"[-+]?\d*\.?\d+|\d+", my_string_two))
#     weight = float(weight[0])
#     print('weight: ',weight)
#     print(type(weight))
#     

    
