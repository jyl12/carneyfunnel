#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Light sensor pin
pin = 21  #pin GPIO 21

# Laser pin
ledpin = 20 #pin GPIO 20

# Setup pin in and out directions
GPIO.setup(pin, GPIO.IN)
GPIO.setup(ledpin, GPIO.OUT)

def laser_detector(pin):
    #Turn on the laser
    GPIO.output(ledpin, GPIO.HIGH)

    # Delay for laser to activate
    time.sleep(0.1)

    # Read the light sensor value and print it to terminal
    print('Light sensor value: ',GPIO.input(pin))

    # Read light sensor and display status
    if GPIO.input(pin) == 1:
        print('Laser detected.')
    else:
        print('Laser not detected.')

    # Add time delay
    time.sleep(0.2)

# Start the program loop to activate the laser and read the light sensor.
try:
    while True:
        laser_detector(pin)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
# from pynput.keyboard import Key, Listener
#   
# def show(key):
#     
#     if key == Key.tab:
#         print("good")
#           
#     if key != Key.tab:
#         print("try again")
#           
#     # by pressing 'delete' button 
#     # you can terminate the loop 
#     if key == Key.delete: 
#         return False
#   
# # Collect all event until released
# with Listener(on_press = show) as listener:
#     listener.join()f
    
