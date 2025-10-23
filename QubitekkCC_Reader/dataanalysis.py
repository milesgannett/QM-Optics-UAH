import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import scipy.fft as fft
import scipy.signal as sig

def main():


    data = np.loadtxt(r'C:\Users\QDM0001\Desktop\Coincidence Counter Data\QubitekkCC_Reader\QubitekkCC_Reader\DATA\COUNTS\data_20251022_173703.csv', delimiter=',', skiprows=1)[:,0]
    N = len(data)
    data_dk = np.loadtxt(r'C:\Users\QDM0001\Desktop\Coincidence Counter Data\QubitekkCC_Reader\QubitekkCC_Reader\DATA\DARK COUNTS\data_20251014_112335.csv', delimiter=',', skiprows=1)[:,0]
    #data_nodk = data - np.mean(data_dk/2)


    meta = open(r'C:\Users\QDM0001\Desktop\Coincidence Counter Data\QubitekkCC_Reader\QubitekkCC_Reader\DATA\COUNTS\metadata_20251022_173703.txt')

    time = float(meta.readlines()[1].strip("Measurement Time (s):"))
    rtime = np.arange(0, time, time/(N-1))

    dfft = fft.fft(data)
    freqs = fft.fftfreq(n = N, d = time/(N-1))

    window = sig.get_window(('gaussian', 2000), N)
    windowed = data * window

    fig,axes = plt.subplots(3,1)
    axes[0].plot(rtime, data)
    axes[1].plot(freqs[np.where(freqs>0)], np.abs(dfft[np.where(freqs>0)])**2 / N )
    axes[2].plot(freqs[np.where(freqs>0)], np.abs(windowed[np.where(freqs>0)])**2 / N )
    axes[1].set_yscale('log')
    axes[2].set_yscale('log')
    #axes[1].set_xscale('log')
    plt.show()


    
    
    bins = np.arange(0,2000,20)
    fig,axes = plt.subplots(3,1, figsize=(10,8))
    axes[0].hist(data, bins=bins, alpha=0.7, color='blue', edgecolor='black')

    axes[1].hist(stats.poisson.rvs(np.mean(data), size= N), bins=bins, alpha=0.7, color='red', edgecolor='black')
    axes[2].hist(stats.norm.rvs(np.mean(data),np.sqrt(np.mean(data)), size= N), bins=bins, alpha=0.7, color='red', edgecolor='black')
    axes[0].set_xlabel(f'Mean = {np.mean(data)}, Variance = {np.std(data)**2}')
    plt.tight_layout()  
    plt.show()

    print(np.mean(data))
    print(np.std(data))



    return

if __name__ == "__main__":
    main()