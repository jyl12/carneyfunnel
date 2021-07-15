import serial
import re
import threading

class ServiceDataCollection(object):
    def __init__(self):
        pass
#         ser = serial.Serial(
#          port='/dev/ttyUSB0',
#          baudrate = 2400,
#          parity=serial.PARITY_EVEN,
#          stopbits=serial.STOPBITS_ONE,
#          bytesize=serial.SEVENBITS,
#          timeout=None
#         )
        
    def start(self):
        t = threading.Thread(target = self.run)
        t.start()
        
    def run(self):
        print('usbweight')
#         raw = ser.readline()
#         w = raw.decode('UTF-8')
#         weight = (re.findall(r"[-+]?\d*\.?\d+|\d+", w))
#         weight = float(weight[0])       
#         return weight

if __name__ == "__main__":
    print('analysis main')
    my_string_two = b'+   123.56 g  /r/n'
    print(my_string_two.decode('UTF-8'))
    my_string_two = my_string_two.decode('UTF-8')
    print(re.findall(r"[-+]?\d*\.?\d+|\d+", my_string_two))
    weight = (re.findall(r"[-+]?\d*\.?\d+|\d+", my_string_two))
    weight = float(weight[0])
    print('weight: ',weight)
    print(type(weight))
    

    
