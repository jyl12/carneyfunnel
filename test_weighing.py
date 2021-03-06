#!/usr/bin/env python3
import time
import serial

ser = serial.Serial(
 port='/dev/ttyUSB0',
 baudrate = 9600,
 parity=serial.PARITY_EVEN,
 stopbits=serial.STOPBITS_ONE,
 bytesize=serial.SEVENBITS,
 timeout=None
)

while 1:
    x=ser.readline()
    print(x)
    with open('raw_input.txt', 'a') as f:
        f.write(x + '\n')
