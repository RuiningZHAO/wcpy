# -*- coding: utf-8 -*-
import os
from copy import deepcopy

# NumPy
import numpy as np
# AstroPy
import astropy.units as u
from astropy.io import ascii, fits
from astropy.time import Time
from astropy.table import Table
# drpy
from drpy.onedspec.io import _Spectrum1D_to_hdu, loadSpectrum1D

from .__init__ import __version__ as version


def plotSpectrum(ax, x, y, xlim, ylim, xlabel, ylabel):
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


def loadLineList(path_to_line_list):
    """Load line list.
    
    Parameters
    ----------
    path_to_line_list : str
        Path to line list.
    
    Returns
    -------
    
    """

    with open(path_to_line_list, 'r') as f:

        # Get rid of empty lines and comments starting with #
        lines = [line.strip() for line in f.read().replace('#', '\n#').split('\n')]
        lines = [line for line in lines if (~line.startswith('#')) & (line != '')]

        line_list = [line.split()[0] for line in lines]

    # Check if all lines are numeric
    for line in line_list:
        try:
            float(line)
        except:
            raise ValueError('There are non-numeric lines in the line list.')

    return line_list


def loadSpectrum(path_to_file, file_format, reverse):
    """Load uncalibrated spectrum.

    Parameters
    ----------
    path_to_file : str
        Path to file.

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
    if file_format == 'fits':
        tbl = loadSpectrum1D(path_to_file, ext='spec')

        length = tbl.data.shape[-1]

        # Count
        count = tbl.data.flatten()[:length]

        # Unit of count
        unit_count = tbl.unit

    else:
        if file_format == 'ascii':
            tbl = ascii.read(path_to_file, guess=True, data_start=0)
        
        elif file_format == 'ecsv':
            tbl = Table.read(path_to_file, format='ascii.ecsv')
        
        length = len(tbl)

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

    # Index
    index = np.arange(length)
    
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
        header = fits.Header(tbl.meta)

    return index, count, unit_count, header


def saveSpectrum(path_to_file, spectrum):
    """Save calibrated spectrum.

    Parameters
    ----------
    path_to_file : str
        Path to file.

    spectrum : `~astropy.table.table.Table`
        Calibrated spectrum to be saved.
    """
    
    hdu_spec = _Spectrum1D_to_hdu(spectrum, spectrum.meta['header'])
    
    hdu_spec.header['ORIGIN'] = (f'wcpy (version {version})', 'file generator')
    hdu_spec.header['DATE'] = (
        f'{Time.now().to_value("iso", subfmt="date_hm")}', 'date file was generated')

    hdu_peak = fits.table_to_hdu(peak_table)

    hdu_peak.header['ORIGIN'] = hdu_spec.header['ORIGIN']
    hdu_peak.header['DATE'] = hdu_spec.header['DATE']

    hdu_list = fits.HDUList([fits.PrimaryHDU(), hdu_spec, hdu_peak])

    hdu_list.writeto(path_to_file, overwrite=True)

    if saveECSV:
        Table.read(hdu_spec).write(
            os.path.splitext(path_to_file)[0] + '_spec.ecsv', format='ascii.ecsv', 
            overwrite=True)
        peak_table.write(
            os.path.splitext(path_to_file)[0] + '_peak.ecsv', format='ascii.ecsv', 
            overwrite=True)


def savePeakTable(path_to_file, peak_table):
    """Save peak information.

    Parameters
    ----------
    path_to_file : str
        Path to file.

    peak_table : `~astropy.table.table.Table`
        Properties of the peaks used to derive dispersion solution.
    """

    pass