import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import scipy.fft as fft
import scipy.signal as sig

def main():

    data1, time1, N1 = ccData('QubitekkCC_Reader\DATA\COUNTS\data_20251023_190227.csv',1)

    print(N1)

    plt.plot(time1, data1)
    plt.show()



    return

    data = np.loadtxt(r'QubitekkCC_Reader\DATA\COUNTS\data_20251023_190227.csv', delimiter=',', skiprows=1)[:,0]
    N = len(data)
    data_dk = np.loadtxt(r'QubitekkCC_Reader\DATA\DARK COUNTS\data_20251023_015306.csv', delimiter=',', skiprows=1)[:,0]
    #data_nodk = data - np.mean(data_dk/2)

    dataT = data[500:750]


    meta = open(r'QubitekkCC_Reader\DATA\COUNTS\metadata_20251023_190227.txt')
    time = float(meta.readlines()[1].strip("Measurement Time (s):"))
    rtime = np.arange(0, time/(len(data)/(len(dataT))), time/(N-1))

    print(data)

    dfft = fft.fft(dataT)
    freqs = fft.fftfreq(n = len(dataT), d = time/(N-1))

    window = sig.get_window(('gaussian', 2000), N)
    windowed = data * window

    fig,axes = plt.subplots(3,1)
    axes[0].plot(rtime, dataT)
    axes[1].plot(freqs[np.where(freqs>0)], np.abs(dfft[np.where(freqs>0)])**2 / N )
    axes[2].plot(freqs[np.where(freqs>0)], np.abs(windowed[np.where(freqs>0)])**2 / N )
    axes[1].set_yscale('log')
    axes[2].set_yscale('log')
    #axes[1].set_xscale('log')
    plt.show()


    
    
    bins = np.arange(0,2000,20)
    fig,axes = plt.subplots(3,1, figsize=(10,8))
    axes[0].hist(dataT, bins=bins, alpha=0.7, color='blue', edgecolor='black')

    axes[1].hist(stats.poisson.rvs(np.mean(dataT), size= N), bins=bins, alpha=0.7, color='red', edgecolor='black')
    axes[2].hist(stats.norm.rvs(np.mean(dataT),np.sqrt(np.mean(data)), size= N), bins=bins, alpha=0.7, color='red', edgecolor='black')
    axes[0].set_xlabel(f'Mean = {np.mean(dataT)}, Variance = {np.std(dataT)**2}')
    plt.tight_layout()  
    plt.show()

    print(np.mean(data))
    print(np.std(data))



    return

def ccData(PATH:str, CH:int):
    
    METAPATH = PATH.replace("data_", "metadata_").replace(".csv", ".txt")

    data = np.loadtxt(PATH, delimiter=',', skiprows=1)[:, CH - 1]
    meta = open(METAPATH).readlines()

    length = int(meta[3].strip("Measurements Taken:"))
    total_t = float(meta[1].strip("Measurement Time (s):"))
    
    time = np.linspace(0, total_t, length)
    
    return data, time, length

if __name__ == "__main__":
    main()