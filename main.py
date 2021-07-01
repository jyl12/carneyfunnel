import time
import serial
import datetime
import analysis.main 
import state_data_storage.main
import data_collection.main

laser = 1
step = 1
if __name__ == "__main__":
    print('---Booting up---')
    data_collection.main.service_data_collection.usb_scale()
#     state_data_storage.main.start()
    while True:
        if step == 1:
            batch_code = input("Enter batch code: ")
            print("Batch code is: " + batch_code)
            step = 2
#          weight_emptycup = ser.readline()
        elif step == 2:
            try:
                weight_powder = float(input("Enter weight of powder (gram): "))
                print("Weight of empty cup (gram): ", weight_powder)
                step = 3
            except ValueError:
                print("That's not a number.")
        elif step == 3:
            try:
                weight_emptycup = float(input("Enter weight of empty cup (gram): "))
                print("Weight of empty cup (gram): ", weight_emptycup)
                step = 4
            except ValueError:
                print("That's not a number.")
        elif step == 4:
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
            flowrate = analysis.main.service_analysis.flowrate(duration, weight_powder)
            print('Flowrate (second/gram): ',flowrate)
            step = 5
        elif step == 5:
            try:
                weight_scrapecup = float(input("Enter weight of scraped cup (gram): "))
                print("Weight of scraped cup (gram): ", weight_scrapecup)
                apparent_density = analysis.main.service_analysis.apparent_density(weight_scrapecup, weight_powder)
                print('Apparent density (gram/cm3): ', apparent_density)
                step = 6
            except ValueError:
                print("That's not a number.")
        elif step == 6:
            state_data_storage.main.Temp1.set_value(time.ctime(int(start_time)))
            state_data_storage.main.Temp2.set_value(batch_code)
            state_data_storage.main.Temp3.set_value(round(flowrate,6))
            state_data_storage.main.Temp4.set_value(round(apparent_density,6))
            state_data_storage.main.write_csv('file',start = time.ctime(int(start_time)),
                                              batch = batch_code,
                                              duration = round(duration,6),
                                              flowrate = round(flowrate,6),
                                              apparentdensity = round(apparent_density,6))
            step = 1

        
        
