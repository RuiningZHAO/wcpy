import os

# NumPy
import numpy as np
# AstroPy
import astropy.units as u
from astropy.io import ascii, fits
from astropy.time import Time
from astropy.table import Table
# drpsy
from drpsy.onedspec import _Spectrum1D_to_hdu, loadSpectrum1D

from __init__ import __version__ as version


def _plotSpectrum(ax, x, y, xlim, ylim, xlabel, ylabel):
    """Plot spectrum."""

    ax.step(x, y, 'k-', lw=0.8, where='mid')
    ax.tick_params(
        which='major', direction='in', top=True, right=True, length=5, width=1, 
        labelsize=12)
    ax.tick_params(
        which='minor', direction='in', top=True, right=True, length=3, width=1, 
        labelsize=12)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)

    return ax

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
        tbl = Table.read(file_name, format=('ascii.' + file_format))

    elif file_format == 'fits':
        tbl = loadSpectrum1D(file_name, ext='spec')

    # Index
    index = np.arange(len(tbl))

    # Count
    # Assume that flux is the second column for multi-column case.
    if len(tbl.colnames) > 1:
        colname = tbl.colnames[1]
    # Use the only column
    else:
        colname = tbl.colnames[0]

    count = tbl[colname].data

    # Unit of count
    if tbl[colname].unit is not None:
        unit_count = tbl[colname].unit
    # Default unit (use config in the future?)
    else:
        unit_count = u.Unit('')

    # Mask bad pixels
    mask = np.isfinite(count)
    if mask.any():
        count = np.interp(index, index[mask], count[mask])

    # Normalize
    count /= count.max()

    # Reverse
    if reverse:
        count = count[::-1]

    # Header
    if 'header' in tbl.meta:
        header = tbl.meta['header']

    else:
        header = dict()

    return index, count, unit_count, header


def saveSpectrum(file_name, spectrum, peak_table, saveECSV):
    """Save calibrated spectrum.

    Parameters
    ----------
    file_name : str
        File name.

    spectrum : `~astropy.table.table.Table`
        Calibrated spectrum to be saved.

    peak_table : `~astropy.table.table.Table`
        Properties of the peaks used to derive dispersion solution.

    saveECSV : bool
        If `True`, two .ecsv files containing the calibrated spectrum and the peak 
        properties are saved along with the .fits file.
    """

    # header['ORIGIN'] = (
    #     f'Wavelength Calibrator (version {version})', 'file generator')
    # header['DATE'] = (
    #     f'{Time.now().to_value("iso", subfmt="date_hm")}', 'date file was generated')

    hdu_spec = _Spectrum1D_to_hdu(spectrum, spectrum.meta['header'])
    
    hdu_spec.header['ORIGIN'] = (
        f'Wavelength Calibrator (version {version})', 'file generator')
    hdu_spec.header['DATE'] = (
        f'{Time.now().to_value("iso", subfmt="date_hm")}', 'date file was generated')

    hdu_peak = fits.table_to_hdu(peak_table)

    hdu_peak.header['ORIGIN'] = hdu_spec.header['ORIGIN']
    hdu_peak.header['DATE'] = hdu_spec.header['DATE']

    hdu_list = fits.HDUList([fits.PrimaryHDU(), hdu_spec, hdu_peak])

    hdu_list.writeto(file_name, overwrite=True)

    if saveECSV:
        Table.read(hdu_spec).write(
            os.path.splitext(file_name)[0] + '_spec.ecsv', format='ascii.ecsv', 
            overwrite=True)
        peak_table.write(
            os.path.splitext(file_name)[0] + '_peak.ecsv', format='ascii.ecsv', 
            overwrite=True)