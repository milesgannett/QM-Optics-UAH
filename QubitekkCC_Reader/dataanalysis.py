import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import scipy.fft as fft
import scipy.signal as sig

def main():

    data, time, meta = ccData('QubitekkCC_Reader\data\dark_counts\data_20251222_165131.csv', 2)
    smean = np.mean(data)
    svar = np.var(data, ddof=1)
    print(f"Sample Mean: {smean}")
    print(f"Sample Variance: {svar}")

    plots = True # Plot data, histograms, etc.

    if plots:

        ePMF, eCDF, drange = pmfcdf(data, discrete=True)
        mPMF = stats.poisson.pmf(drange, mu=smean)

        fig, axes = plt.subplots(nrows=1,ncols=2)

        axes[0].scatter(time, data, color='black', s=1)
        axes[0].plot(time, data, color='gray', lw=.5, alpha=.5)
        axes[0].axhline(smean, 0, 1, color='red', label=fr'$\bar{{x}}$ = {np.round(smean,3)}', alpha=.5)
        axes[0].set_title(fr'Time Series for Dark Counts from APD')
        axes[0].set_xlabel(r'Time ($s$)')
        axes[0].set_ylabel(r'Counts per Second ($s^{-1}$)')
        axes[0].legend()
        axes[1].bar(drange, ePMF, color='black', label='Empirical PMF')
        axes[1].bar(drange, mPMF, color='blue', alpha=0.3, label='Model PMF')
        axes[1].plot(drange, mPMF, color='blue', alpha=0.3)
        axes[1].set_xlabel(r'Counts per Second ($s^{-1}$)')
        axes[1].set_ylabel(r'Probability')
        axes[1].set_title(fr'Dark Count Distribution, Poisson Model for Reference: $\mu = s^2$ = {np.round(svar, 1)}')
        axes[1].legend()
        plt.show()




    
 
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

def pmfcdf(data:np.ndarray, discrete:bool = False):
    n = len(data)
    dsort = np.sort(data)

    if discrete:
        pmf, drange = np.histogram(data, bins = np.arange(min(data), max(data)+2))
        pmf = pmf/n
        drange = drange[:len(drange)-1]
        cdf = np.cumsum(pmf)

        return pmf, cdf, drange
    else: 
        cdf = np.arange(1, n+1, 1)/n
        return cdf, dsort


if __name__ == "__main__":
    main()