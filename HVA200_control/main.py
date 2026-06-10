'''

Author: Miles Gannett
University of Alabama in Huntsville, Department of Physics and Astronomy
June 2026

Description: This script interfaces with the Thorlabs HVA200 High Voltage 
Amplifier (HVA) via serial COM port using the InstrumentKit package. 
Work in progress.

'''


import numpy as np
import instruments as ik
import time
from datetime import datetime
import os

def main():
    HV1 = ik.Instrument.open_serial(port="COM1", baud=115200)
    print(HV1.query("id?"))

    return

if __name__ == "__main__":
    main()