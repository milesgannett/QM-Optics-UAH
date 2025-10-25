import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import scipy.fft as fft
import scipy.signal as sig

def main():

    data, time, meta = ccData('QubitekkCC_Reader\DATA\COUNTS\data_20251024_124309.csv', 1)
    dark, dtime, metad = ccData('QubitekkCC_Reader\DATA\DARK COUNTS\data_20251023_015306.csv', 1)
    N = len(data)

    
    # covar, corr = coVar(data, dark[:N])
    # Maybe... find the covariance/correlation of "data"
    # with many different parts of "dark" and average them?
    corr = 0
    covar = 0
    ratioN = int(len(dark)/len(data))
    for i in np.arange(ratioN):
        covar1, corr1 = coVar(data,dark[i*N:(i+1)*N])
        covar += covar1
        corr += corr1

    corr = corr/ratioN
    covar = covar/ratioN

    mean = np.mean(data)
    dmean = np.mean(dark)
    var = np.var(data, ddof = 1)
    dvar = np.var(dark, ddof = 1)


    print(f"Mean of Data: {mean}, Mean of Dark Count Data: {dmean}")
    print(f"Variance of Data: {var}, Variance of Dark Count Data: {dvar}")
    print(f"Covariance: {covar}, Correlation Coefficient: {corr}")

    # Sample variances add like: var(x+y) = varx + vary + 2 covarxy
    # Want varx and to see if equal to mean - dmean ? 
    print(f"Possible 'true' mean: {mean - dmean}, Possible 'true' variance: {var - dvar - 2*covar}")

    return

def ccData(PATH:str, CH:int):

    '''
    Picks the provided channel out of the data provided by PATH.
    Looks for a metadata file in the same folder with the same timestamp.
    Relevant quantities are taken from the metadata to determine an
    appropriate time array for the data. Metadata is returned as a list. 
    '''

    METAPATH = PATH.replace("data_", "metadata_").replace(".csv", ".txt")

    data = np.loadtxt(PATH, delimiter = ',', skiprows = 1)[:, CH - 1]
    meta = open(METAPATH).readlines()

    for i, line in enumerate(meta):
        if "Measurement Time" in line:
            total_t = float(line.strip("Measurement Time (s):"))
        if "Measurements Taken" in line:
            N = int(line.strip("Measurements Taken:"))

    time = np.linspace(0, total_t, N)
    
    return data, time, meta

def coVar(data1:np.ndarray, data2:np.ndarray):

    '''
    Returns the covariance and correlation coefficient
    of two data arrays of the same length.
    '''

    N = len(data1)

    if  len(data2) != N:
        return Exception("Cannot compute covariance of different length arrays.")

    mean1 = np.mean(data1)
    mean2 = np.mean(data2)
    var1 = np.var(data1, ddof = 1)
    var2 = np.var(data2, ddof = 1)

    sum = 0
    for i in np.arange(N):
        sum += (data1[i] - mean1)*(data2[i] - mean2)

    covar = sum/(N - 1)
    corr = covar/np.sqrt(var1*var2)

    return covar, corr

if __name__ == "__main__":
    main()