"""
Author: Miles Alden Gannett, University of Alabama in Huntsville, Department of Physics and Astronomy

Description: Frequency analysis of lab power supply Elenco Model XP-581A.
"""

import numpy as np
import scipy.fft as spft
import matplotlib.pyplot as plt

def main():

    N = 50
    psPATH = r'PS_analysis\XP-581A\C1_xp581a_5v_'
    backPATH = r'PS_analysis\Oscilloscope Background\C1_oscope_bkgrnd_'
    avgPS = 0
    for i in np.arange(N):
        pspath = f"{psPATH}{i:05d}.csv"
        data, time = oscopeData(pspath)
        tf = spft.fftshift(spft.fft(data))
        avgPS += tf
    avgPS = avgPS/N
    avgBK = 0 

    for i in np.arange(N):
        backpath = f"{backPATH}{i:05d}.csv"
        data, time = oscopeData(backpath)
        tf = spft.fftshift(spft.fft(data))
        avgBK += tf
    avgBK = avgBK/N

    freqs = spft.fftshift(spft.fftfreq(data.size, time[1]-time[0]))

    mask = freqs >= 0
    freqs = freqs[mask]
    avgPS = avgPS[mask]
    avgBK = avgBK[mask]

    plt.plot(freqs[1:], np.abs(avgBK[1:]), color='red')
    plt.plot(freqs[1:], np.abs(avgPS[1:]), color='blue')
    plt.plot(freqs[1:], np.abs(avgPS[1:] - avgBK[1:]), color='green')
    plt.show()


    pass

def oscopeData(PATH:str):

    '''
    Creates an array from Oscope data provided by PATH.
    '''

    data = np.loadtxt(PATH, delimiter = ',', skiprows = 5)

    return data[:,1], data[:,0]

if __name__ == "__main__":
    main()

