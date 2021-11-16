import os
# NumPy
import numpy as np
# SciPy
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from scipy.interpolate import LSQUnivariateSpline
# AstroPy
from astropy.io import ascii
from astropy.time import Time
from astropy.table import Table

def loadSpectrum(filename, fileformat, inverse):
    """A function to load uncalibrated spectrum.

    Parameters
    ----------
    filename : str
    fileformat : str
    inverse : bool

    Returns
    -------
    index : np.ndarray
    count : np.ndarray

    Raise 
    -----
    1) load file (empty)
    2) all nan or inf
    3) less than 5 points
    """

    # Load
    if fileformat == 'ascii':
        tbl = ascii.read(filename, guess=True, data_start=0)
    else:
        if fileformat == 'ecsv': fileformat = 'ascii.' + fileformat
        tbl = Table.read(filename, format=fileformat)

    # Index
    index = np.arange(len(tbl))

    # Count
    if len(tbl.colnames) > 1:
        count = tbl[tbl.colnames[1]].data
    else:
        count = tbl[tbl.colnames[0]].data
    mask = np.isnan(count) | ~np.isfinite(count)
    if mask.any():
        count = np.interp(index, index[~mask], count[~mask])
    count = count / count.max()

    # Inverse
    if inverse:
        count = count[::-1]

    return index, count

def saveSpectrum(data, header, filename, fileformat):
    """A function to load uncalibrated spectrum.

    Parameters
    ----------
    data : np.ndarray
    header : dict
    filename : str
    fileformat : str
    """
    header['ORIGIN'] = ('Wavelength Calibrator (version 0.0.2)', 'File originator')
    header['DATE'] = (f'{Time.now().to_value("iso", subfmt="date_hm")}', 'Date file was generated')
    Table(data=data, 
          names=('wavelength', 'normalized count'),
          meta=header).write(filename, format=fileformat, overwrite=True)

def Gaussian(x, a, x0, sigma):
    """1D Gaussian

    Parameters
    ----------
    x: float or `numpy.ndarray`
        value or values to evaluate the Gaussian at
    a: float
        Magnitude
    x0: float
        Gaussian centre
    sigma: float
        Standard deviation (spread)

    Returns
    -------
    out: float or `numpy.ndarray`
        The Gaussian function evaluated at provided x
    """
    
    # return a * np.exp(-(x - x0)**2 / (2 * sigma**2 + 1e-9))
    return a * np.exp(-(x - x0)**2 / (2 * sigma**2))

def refine_peaks(spectrum, peaks, properties):
    """
    Refine peak locations in a spectrum from a set of initial estimates.
    This function attempts to fit a Gaussian to each peak in the provided
    list. It returns a list of sub-pixel refined peaks. If two peaks are
    very close, they can be refined to the same location. In this case
    only one of the peaks will be returned - i.e. this function will return
    a unique set of peak locations.

    Parameters
    ----------
    spectrum: array_like
        Input spectrum (intensities)
    peaks: array_list
        Peak locations in pixels
    properties: dict
        Peak properties dict returned by `scipy.signal.find_peaks`. Should
        contain `peak_heights`, `left_bases` and `right_bases`.

    Returns
    -------
    refined_peaks: `numpy.ndarray`
        Refined peak locations
    """

    refined_peaks = list()

    spectrum = np.array(spectrum)

    length = spectrum.shape[0]
    index = np.arange(length)

    peaks = np.round(peaks, 0).astype(int)
    npeaks = peaks.shape[0]

    heights = properties['peak_heights']
    left_bases = properties['left_bases']
    right_bases = properties['right_bases']
    widths = right_bases - left_bases

    for i in range(npeaks):
        if i == 0:
            left_base = left_bases[i]
        elif right_bases[i - 1] >= peaks[i]:
            left_base = left_bases[i]
        else:
            left_base = np.max([left_bases[i], right_bases[i - 1]])

        if i == (npeaks - 1):
            right_base = right_bases[i]
        elif left_bases[i + 1] <= peaks[i]:
            right_base = right_bases[i]
        else:
            right_base = np.min([right_bases[i], left_bases[i + 1]])

        if (right_base + 1 - left_base) < 5:
            left_base = peaks[i] - 2
            right_base = peaks[i] + 2
            if left_base < 0:
                right_base += 0 - left_base
                left_base = 0
            if right_base > (length - 1):
                left_base -= (right_base - length + 1)
                right_base = length - 1

        x = index[left_base:(right_base + 1)]
        y = spectrum[left_base:(right_base + 1)]

        try:
            popt, _ = curve_fit(Gaussian, x, y, p0=[heights[i], peaks[i], widths[i]])
            height, centre, _ = popt

            if (height > 0) & \
               (0 < centre) & \
               (centre < (length - 1)):
                refined_peaks.append(centre)
            else:
                continue

        except RuntimeError:
            continue
    refined_peaks = np.array(refined_peaks)

    # Remove peaks that are within rounding errors from each other from the
    # curve_fit
    distance_mask = np.isclose(refined_peaks[:-1], refined_peaks[1:])
    distance_mask = np.hstack([False, distance_mask])

    return refined_peaks[~distance_mask]

def findPeaks(x, **kwargs):
    """
    A function to find and refine peaks
    """

    peaks, properties = find_peaks(x=x, **kwargs)
    if peaks.shape[0] > 0:
        # Refine peaks
        return refine_peaks(spectrum=x, 
                            peaks=peaks, 
                            properties=properties)
    else:
        return peaks

def fitCubicSpline(x, y, mask, npieces):
    """
    A function to fit with cubic spline function
    """

    order = 3
    if ((~mask).sum() - 2) >= npieces:
        knots = x[~mask][0] + np.arange(1, npieces) * (x[~mask][-1] - x[~mask][0]) / npieces
        spl = LSQUnivariateSpline(x=x[~mask], 
                                  y=y[~mask], 
                                  t=knots, 
                                  w=None, 
                                  bbox=[None, None], 
                                  k=order, 
                                  ext='extrapolate', 
                                  check_finite=False)
        return spl
    else:
        raise
