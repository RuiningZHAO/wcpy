import os, warnings

# NumPy
import numpy as np
# SciPy
from scipy.signal import find_peaks
from scipy.interpolate import LSQUnivariateSpline
from scipy.optimize import curve_fit, OptimizeWarning
# AstroPy
from astropy.io import ascii, fits
from astropy.time import Time
from astropy.table import Table
# drpsy
from drpsy.modeling.function import Gaussian1D

from __init__ import __version__ as version

warnings.simplefilter('error', OptimizeWarning)

def loadSpectrum(file_name, file_format, reverse):
    """Load uncalibrated spectrum.

    Parameters
    ----------
    file_name : str
        File name.

    file_format : str
        File format.

    reverse : bool
        Reverse ot not.

    Returns
    -------
    index : `~numpy.ndarray`
        Pixel index.

    count : `~numpy.ndarray`
        Normalized count.

    Raise 
    -----
    1) load file (empty)
    2) all nan or inf
    3) less than 5 points
    """

    # Load
    if file_format == 'ascii':
        tbl = ascii.read(file_name, guess=True, data_start=0)

    elif file_format == 'ecsv':
        tbl = Table.read(file_name, format='ascii.' + file_format)

    elif file_format == 'fits':
        tbl = Table.read(file_name, format=file_format, hdu='spec')

    # Index
    index = np.arange(len(tbl))

    # Count
    if len(tbl.colnames) > 1:
        count = tbl[tbl.colnames[1]].data

    else:
        count = tbl[tbl.colnames[0]].data

    # Mask bad pixels
    mask = np.isfinite(count)

    if mask.any():
        count = np.interp(index, index[mask], count[mask])

    # Normalize
    count = count / count.max()

    # Reverse
    if reverse:
        count = count[::-1]

    return index, count


def saveSpectrum(file_name, spectrum, peak_prop, header, saveECSV):
    """Save calibrated spectrum.

    Parameters
    ----------
    file_name : str
        File name.

    spectrum : `~astropy.table.table.Table`
        Calibrated spectrum to be saved.

    peak_prop : `~astropy.table.table.Table`
        Properties of the peaks used to derive dispersion solution.

    header : dict
        Header of the file to be saved.

    saveECSV : bool
        If `True`, two .ecsv files containing the calibrated spectrum and the peak 
        properties are saved along with the .fits file.
    """

    header['ORIGIN'] = (
        f'Wavelength Calibrator (version {version})', 'file generator')
    header['DATE'] = (
        f'{Time.now().to_value("iso", subfmt="date_hm")}', 'date file was generated')

    
    spectrum.meta['EXTNAME'] = ('spec', 'name of the extension')
    peak_prop.meta['EXTNAME'] = ('peak', 'name of the extension')
    for key, val in header.items():
        spectrum.meta[key] = val
        peak_prop.meta[key] = val

    hdu_list = fits.HDUList([
        fits.PrimaryHDU(),
        fits.table_to_hdu(spectrum),
        fits.table_to_hdu(peak_prop), 
    ])
    hdu_list.writeto(file_name, overwrite=True)

    if saveECSV:
        spectrum.write(
            os.path.splitext(file_name)[0] + '_spec.ecsv', format='ascii.ecsv', 
            overwrite=True)
        peak_prop.write(
            os.path.splitext(file_name)[0] + '_peak.ecsv', format='ascii.ecsv', 
            overwrite=True)


def refinePeaks(spectrum, peaks, properties):
    """Refine peak locations in a spectrum from a set of initial estimates.
    This function attempts to fit a Gaussian to each peak in the provided
    list. It returns a list of sub-pixel refined peaks. If two peaks are
    very close, they can be refined to the same location. In this case
    only one of the peaks will be returned - i.e. this function will return
    a unique set of peak locations.

    Parameters
    ----------
    spectrum: array_like
        Input spectrum (intensities).
    peaks: array_like
        Peak locations in pixels.
    properties: dict
        Peak properties dict returned by `scipy.signal.find_peaks`. Should
        contain `peak_heights`, `left_bases` and `right_bases`.

    Returns
    -------
    refined_peaks: `numpy.ndarray`
        Refined peak locations in pixels.
    """

    # Validate inputs
    try:
        spectrum = np.array(spectrum)
    except:
        raise ValueError(f'Invalid type {type(spectrum)} for refining peak locations.')

    try:
        peaks = np.array(peaks, dtype=float)
    except:
        raise ValueError(f'Invalid type {type(peaks)} for refining peak locations.')
    
    if ('peak_heights' not in properties) | \
       ('left_bases' not in properties) | \
       ('right_bases' not in properties):
        raise ValueError('``properties`` should contain `peak_heights`, `left_bases` and `right_bases`.')

    index = np.arange(spectrum.shape[0])

    n_peaks = peaks.shape[0]

    heights = properties['peak_heights'].astype(float)
    left_bases = properties['left_bases'].astype(float)
    right_bases = properties['right_bases'].astype(float)
    widths = right_bases - left_bases

    refined_index = list()
    refined_peaks = list()
    for i in range(n_peaks):
        # Refine left base
        if i == 0:
            left_base = left_bases[i]
        elif right_bases[i - 1] >= peaks[i]:
            left_base = left_bases[i]
        else:
            left_base = np.max([left_bases[i], right_bases[i - 1]])
        # Refine right base
        if i == (n_peaks - 1):
            right_base = right_bases[i]
        elif left_bases[i + 1] <= peaks[i]:
            right_base = right_bases[i]
        else:
            right_base = np.min([right_bases[i], left_bases[i + 1]])
        # too few points
        if (right_base + 1 - left_base) < 5:
            left_base = peaks[i] - 2
            right_base = peaks[i] + 2
            if left_base < 0:
                right_base -= left_base
                left_base = 0
            if right_base > index[-1]:
                left_base -= (right_base - index[-1])
                right_base = index[-1]
        left_base, right_base = int(left_base), int(right_base)
        
        # Fit
        x = index[left_base:(right_base + 1)]
        y = spectrum[left_base:(right_base + 1)]

        try:
            popt, _ = curve_fit(Gaussian1D, x, y, p0=[heights[i], peaks[i], widths[i]])
            height, centre, _ = popt

            if (height > 0) & \
               (left_base < centre) & \
               (centre < right_base):
                refined_index.append(i)
                refined_peaks.append(centre)

        except (RuntimeError, OptimizeWarning):
            continue

    refined_index = np.array(refined_index)
    refined_peaks = np.array(refined_peaks)

    # Mask peaks that are within rounding errors from each other
    mask = np.isclose(refined_peaks[:-1], refined_peaks[1:])
    mask = np.hstack([False, mask])

    refined_index = refined_index[~mask]
    refined_peaks = refined_peaks[~mask]
    refined_properties = dict()
    for key, val in properties.items():
        refined_properties[key] = val[refined_index]

    return refined_peaks, refined_properties, refined_index


def findPeaks(x, **kwargs):
    """Find and refine peaks"""

    peaks, properties = find_peaks(x=x, **kwargs)
    if peaks.shape[0] > 0:
        # Refine peaks
        refined_peaks, refined_properties, _ = refinePeaks(
            spectrum=x, peaks=peaks, properties=properties)
        return refined_peaks, refined_properties

    else:
        return peaks, properties


def fitCubicSpline(x, y, mask, npieces):
    """Fit with cubic spline function"""

    order = 3
    if ((~mask).sum() - 2) >= npieces:
        knots = (
            x[~mask][0] + np.arange(1, npieces) * (x[~mask][-1] - x[~mask][0]) / npieces
        )
        spl = LSQUnivariateSpline(
            x=x[~mask], y=y[~mask], t=knots, w=None, bbox=[None, None], k=order, 
            ext='extrapolate', check_finite=False)
        return spl
    else:
        raise