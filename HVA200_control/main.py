'''

Author: Miles Gannett
University of Alabama in Huntsville, Department of Physics and Astronomy
June 2026

Description: This script interfaces with the Thorlabs hvA200 High Voltage 
Amplifier (hvA) via serial COM port using the pySerial package.

This script should meet the following requirements: 
1. User can input overall experiment run time and single shot period/frequency.
2. User can choose between random operation and controlled operation.
3. Generates metadeta including experiment start/end time, shot timing, voltage value per shot,

'''

import numpy as np
import serial
import time
from datetime import datetime
import os

def main():

    # Open serial communication with each device, modify COM port values accordingly

    hv1 = serial.Serial(port="COM3", baudrate=115200,
    bytesize=8, parity='N', stopbits=1, timeout=1)

    '''
    hv2 = serial.Serial(port="COM5", baudrate=115200,
    bytesize=8, parity='N', stopbits=1, timeout=1)

    hv3 = serial.Serial(port="COM6", baudrate=115200,
    bytesize=8, parity='N', stopbits=1, timeout=1)

    hv4 = serial.Serial(port="COM7", baudrate=115200,
    bytesize=8, parity='N', stopbits=1, timeout=1) 
    '''

    # Initial query
    
    hv1.write(b"\r")
    print(hv1.read_until(b'>').decode().strip())
    
    hv1.write(b"id?\r")
    print(hv1.read_until(b'>').decode().strip())


    # Commands

    rand_op = True # Random operation or controlled operation
    shotperiod = 0.01 # Shot period in seconds
    Nshots = 100 # total number of shots 

    if rand_op:
        print('rand')
        startT = time.time_ns() # start time in ns
        dt = np.empty(Nshots)
        # Open uniform random number generator for integers 0 - 65535
        # Record time at beginning of run and end of each run to check overall time with what I expect, which is shotperiod*Nshots
        for i in np.arange(Nshots):
            t1 = time.time_ns()
            time.sleep(shotperiod)
            t2 = time.time_ns()
            dt[i] = t2-t1
            
        # Command the HV with b'value=_\r'
        # Record chosen value and maybe record the time at the beginning of each shot
        endT = time.time_ns() # end time in ns
    else:
        hv1.write(b"enable=1\r")
        print(hv1.read_until(b'>').decode().strip())

        hv1.write(b"enable?\r")
        print(hv1.read_until(b'>').decode().strip())

        hv1.write(b"enable=0\r")
        print(hv1.read_until(b'>').decode().strip())

        hv1.write(b"enable?\r")
        print(hv1.read_until(b'>').decode().strip())

    print(endT-startT)
    print(np.mean(dt))
    # Verify all output is OFF and close connections.



    hv1.close()

    '''
    hv2.close()
    hv3.close()
    hv4.close()
    '''
    return
def volt_to_bit(volts:np.float16):
    return 

if __name__ == "__main__":
    main()