'''

Author: Miles Gannett
University of Alabama in Huntsville, Department of Physics and Astronomy
June 2026

Description: This script interfaces with the Thorlabs HVA200 High Voltage 
Amplifier (HVA) via serial COM port using the pySerial package.
Work in progress...

'''

import numpy as np
import serial
import time
from datetime import datetime
import os

def main():
    HV1 = serial.Serial(port="COM3", baudrate=115200,
    bytesize=8, parity='N', stopbits=1, timeout=1)

    HV1.write(b"\r")
    print(HV1.read_until(b'>').decode().strip())
    
    HV1.write(b"id?\r")
    print(HV1.read_until(b'>').decode().strip())

    HV1.write(b"enable=1\r")
    print(HV1.read_until(b'>').decode().strip())

    HV1.write(b"enable?\r")
    print(HV1.read_until(b'>').decode().strip())

    HV1.write(b"enable=0\r")
    print(HV1.read_until(b'>').decode().strip())

    HV1.write(b"enable?\r")
    print(HV1.read_until(b'>').decode().strip())



    HV1.close()

    return

if __name__ == "__main__":
    main()