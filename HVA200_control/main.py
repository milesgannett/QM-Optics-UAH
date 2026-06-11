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
    HV1 = serial.Serial(port="COM4", baudrate=115200)
    print(HV1.name)
    HV1.write(b"id?\r")
    print(HV1.readline())
    HV1.close()

    return

if __name__ == "__main__":
    main()