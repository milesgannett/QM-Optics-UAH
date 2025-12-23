'''

Author: Miles Gannett
University of Alabama in Huntsville, Department of Physics and Astronomy
October 2025

Description: This script connects to a Qubitekk Coincidence Counter (CC)
via serial COM port, using the Qubitekk CC1 class from the instruments package,
originally contributed by Catherine Holloway. It allows for setting various
counting parameters, acquiring photon count data from two channels and their
coincidences, and saving the data along with relevant metadata to files. 

'''


import numpy as np
import instruments as ik
import time
from datetime import datetime
import os

def main():

    '''
    
    SETTINGS NOTES:


    Changing the trigger mode seems to have some potentially unexpected behavior.
    When calling inst.trigger_mode the opposite of the true setting is returned. 
    This is likely a bug in the instruments package. For example, if
    inst.trigger_mode = 'start_stop', then calling inst.trigger_mode 
    returns '_TriggerModeOld.continuous'. However, the trigger mode is
    actually set correctly on the CC. Additionally, changing the trigger mode
    seems to set the counting state to OFF. The state can be set back to ON
    by calling inst.sendcmd(':COUN:ON'). This is important to note because
    the ":COUN:ON" command is not present in the documentation's list of 
    commands OR as a method in the InstrumentKit package. It was found in the
    example program provided in the CC documentation. It is necessary to
    use this command to ensure that counts are only stored AFTER the 
    dwell time has elapsed. 

    To prevent sending commands/requests to the CC more than necessary, the 
    settings are stored in variables. Since the settings are not changed during 
    data acquisition, there is no need to request them from the CC for each 
    measurement. This also allows metadata to be compiled without requesting
    each setting from the CC.

    For this program to function as intended (and to trust the counts you get) 
    you must use the "start_stop" trigger mode. If you do not control how the 
    CC starts counting so that it is synchronized with your data collection,
    then requests for the number of counts may arrive before the dwell time is
    finished, resulting in extremely inaccurate and inconsistent data. 
    
    '''

    # Settings - CHANGE THESE
    
    N = 20000 # N = number of measurements to take
    CH1dserial = 38635 # CH1 Detector serial number 
    CH2dserial = 38634 # CH2 Detector serial number
    CH1pserial = 0 # CH1 Power Supply serial number
    CH2pserial = 0 # CH2 Power Supply serial number
    # Add note to metadata to describe the set-up
    desc = "38635 using the new supply, 38634 using the old supply." 


    wait_time = 60 # Time to wait after program start before data collection



    laser_power = 0 # mW as reported by Toptica software, enter "0" if dark count data
    fine = "off" # FINE setting in Toptica software "off" or "on"
    fine_A = 80 # FINE A value (%)
    fine_B = 20 # FINE B value (%)


    com_port = "COM5" # Set COM port (shouldn't change unless PC changes)

    # Counting Settings:
    dwell_time = 1 # seconds (0.1, 0.2, 0.3, ..., 1, 2)
    gate = False # bool (True/False)
    trigger_mode = 'start_stop' # 'continuous' or 'start_stop' 
    
    # Coincidence Specific Settings:
    subtract = False # Subtract accidentals, bool (True/False)
    window = 1 # Coincidence window (nanoseconds, 1 - 7)
    delay = 0 # Delay on CH1 (nanoseconds, 0, 2, 4, ..., 12, 14)

    '''
    InstrumentKit connects via COM port to the counter.
    The COM port settings must match those specified in the CC documentation.
    Baud rate (bits/sec) is communication speed between computer and CC.
    A baud rate of 19200 is required by CC (do not change).
    The COM port number must be changed as needed (check device manager).
    Timeout is time (sec) to wait for response from CC before giving up.
    '''

    print('Initializing connection to Qubitekk CC...')
    inst = ik.qubitekk.CC1.open_serial(com_port, baud=19200, timeout=5)
    firmware = inst.firmware # Request firmware version to ensure connection is valid
    print(f'Connected! CC Firmware Version: {firmware}')

    
    time.sleep(.3) # Wait a moment before applying settings.

    print("Applying settings...")

    inst.dwell_time = dwell_time
    time.sleep(.3)
    inst.gate = gate
    time.sleep(.3)
    inst.trigger_mode = trigger_mode 
    time.sleep(.3)
    inst.subtract = subtract 
    time.sleep(.3)
    inst.window = window 
    time.sleep(.3)
    inst.delay = delay
    time.sleep(.3)

    print("Settings applied.")
    time.sleep(.3) # Ensure settings are finished applying.

    print(f"Collection will take approximately {(dwell_time+1.4)*N/60} minutes.")

    for j in range(wait_time):
        print( f"Time before data acquisition: {wait_time - j} (sec)  ", end="\r")
        time.sleep(1)

    time_str = datetime.now().strftime('%Y%m%d_%H%M%S') # Acquisition start time

    # Data Acquisition -

    print("\nStarting Data Acquisition")
    data = np.empty([N,3]) # 2 count channels, 1 coincidence channel, N measurements


    startTime = time.time()
    for i in range(N):
        # Time delays need to be added here to allow the counts to accumulate.

        inst.sendcmd(':COUN:ON')
        time.sleep(dwell_time + 0.5) # Wait for dwell time to finish + small buffer

        data[i,0] = inst.channel[0].count # CH1 counts
        data[i,1] = inst.channel[1].count # CH2 counts
        data[i,2] = inst.channel[2].count # Coincidence counts
        
        time.sleep(0.1) # Short delay to ensure counts finish reading before next measurement starts
        print(f"Measurement {i+1} of {N} complete.", end='\r')
    totalTime = time.time() - startTime

    print("\nData Acquisition Complete")
    

    # Storing Data -

    # Creates a metadata file including CC settings.
    # MUST specify a valid path on your computer
    print("Generating metadata for this run...")
    
    metadata = np.array(
        [f"Date and Time (YrMtDy_HrMnSc): {time_str}",
        f"Measurement Time (s): {totalTime}",
        f"Laser Power (mW): {laser_power}",
        f"Measurements Taken: {N}",
        f"Dwell Time (s): {dwell_time}",
        f"CH1 Detector Serial #: {CH1dserial}",
        f"CH2 Detector Serial #: {CH2dserial}",
        f"CH1 Power Supply Serial #: {CH1pserial}",
        f"CH2 Power Supply Serial #: {CH2pserial}",        
        f"FINE?: {fine}",
        f"FINE A (%): {fine_A}",
        f"FINE B (%): {fine_B}",
        f"Gate Enabled: {gate}",
        f"Trigger Mode: {trigger_mode}",
        f"Subtract Accidentals: {subtract}",
        f"Coincidence Window (ns): {window}",
        f"Delay on CH1 (ns): {delay}",
        f"Firmware Version: {firmware}",
        f"Description: {desc}"])
        

    print("Success.")

    print("Generating file paths...")

    metafilename = f"metadata_{time_str}.txt" 
    filename = f"data_{time_str}.csv"
    


    if laser_power > 0:
        # Counts Path
        path = r'QubitekkCC_Reader\data\counts' 
    else: 
        # Dark Counts Path
        path = r'QubitekkCC_Reader\data\dark_counts' 

    datapath = os.path.join(path, filename) 
    metapath = os.path.join(path, metafilename)
    print("Success.")

    print(f"Saving metadata to file in {path}...")
    np.savetxt(metapath, metadata, fmt='%s')
    print("Saved!")

    print(f"Saving data to file in {path}...")
    np.savetxt(datapath, data, fmt='%i', delimiter=',', header='CH1, CH2, Coincidence')
    print("Saved!")

    time.sleep(1) 

    print("Finished! Exiting...")

    return

if __name__ == "__main__":
    main()