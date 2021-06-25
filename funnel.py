import time
import serial
import vision
import datetime
# ser = serial.Serial(
#  port='/dev/ttyUSB0',
#  baudrate = 2400,
#  parity=serial.PARITY_EVEN,
#  stopbits=serial.STOPBITS_ONE,
#  bytesize=serial.SEVENBITS,
#  timeout=None
# )
laser=0

if __name__ == "__main__":
    while True:
        powder_code = input("Enter powder code: ")
        print("Powder code is: " + powder_code)
#          weight_emptycup = ser.readline()
        weight_powder = float(input("Enter weight of powder (gram): "))
        print("Weight of empty cup (gram): ", weight_powder)
        weight_emptycup = float(input("Enter weight of empty cup (gram): "))
        print("Weight of empty cup (gram): ", weight_emptycup)
        while laser == 1:
            time.sleep(0.02)
            start_time = time.time()
        print('Stopwatch started')
        while laser == 0:
            time.sleep(0.02)
        end_time = time.time()
        duration = end_time - start_time
        print('Duration (second): ', duration)
        flowrate = duration / weight_powder
        print('Flowrate (second/gram): ',flowrate)
        weight_scrapecup = float(input("Enter weight of scraped cup (gram): "))
        print("Weight of scraped cup (gram): ", weight_scrapecup)
        apparent_density = weight_scrapecup / weight_powder
        print('Apparent density (gram/cm3): ', apparent_density)

        
        
