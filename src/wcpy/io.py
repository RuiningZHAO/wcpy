# -*- coding: utf-8 -*-
import os
from copy import deepcopy
from collections import OrderedDict

# NumPy
import numpy as np
# AstroPy
import astropy.units as u
from astropy.io import ascii, fits
from astropy.time import Time
from astropy.table import Table
# specutils
from specutils import Spectrum1D
from specutils.io.parsing_utils import generic_spectrum_from_table

from .__init__ import __version__ as version


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
        Reverse or not.

    Returns
    -------
    index : `~numpy.ndarray`
        Pixel index.

    count : `~numpy.ndarray`
        Normalized count.

    Raise 
    -----
    EOFError
        Empty file.
    
    ValueError
        all nan or inf
        less than 5 points
    """

    # Load
    if file_format == 'fits':

        tbl = Table.read(path_to_file, format='fits', hdu=1)

        ndim = tbl['flux'].data.ndim

        if ndim == 0:
            raise EOFError(f"No spectrum found in '{path_to_file}'.")
        
        else:

            length = tbl['flux'].data.shape[0]

            # Count
            if ndim == 1:
                count = tbl['flux'].data

            else:

                count = tbl['flux'].data[0]

            # Unit of count
            unit_count = tbl['flux'].unit

            # Header
            header = fits.getheader(path_to_file, ext=1)

    else:
        
        if file_format == 'ecsv':
            tbl = Table.read(path_to_file, format='ascii.ecsv')

        elif file_format == 'ascii':
            tbl = ascii.read(path_to_file, guess=True, data_start=0)
        
        length = len(tbl)

        if length == 0:
            raise EOFError(f"No spectrum found in '{path_to_file}'.")

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
        # Default unit (use config?)
        else:
            unit_count = u.Unit('')

        # Header
        header = fits.Header(tbl.meta)

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

    return index, count, unit_count, header


def saveSpectrum(path_to_file, file_format, spectrum):
    """Save calibrated spectrum.

    Parameters
    ----------
    path_to_file : str
        Path to file.

    file_format : str
        File format.

    spectrum : `~astropy.table.table.Table`
        Calibrated spectrum to be saved.
    """

    spectrum.meta['ORIGIN'] = (f'wcpy (ver {version})', 'file generator')
    spectrum.meta['DATE'] = (
        f'{Time.now().to_value("iso", subfmt="date_hm")}', 'date file was generated')

    if file_format == 'fits':
        spectrum = generic_spectrum_from_table(spectrum)
        spectrum.write(path_to_file, format='tabular-fits', overwrite=True)

    elif file_format == 'ecsv':
        meta = OrderedDict()
        for key, val in spectrum.meta.items():
            meta[key] = val
        spectrum.meta = meta
        spectrum.write(path_to_file, format='ascii.ecsv', overwrite=True)


def savePeakTable(path_to_file, file_format, peak_table):
    """Save peak information.

    Parameters
    ----------
    path_to_file : str
        Path to file.

    file_format : str
        File format.

    peak_table : `~astropy.table.table.Table`
        Properties of the peaks used to derive dispersion solution.
    """

    peak_table.meta['ORIGIN'] = (f'wcpy (ver {version})', 'file generator')
    peak_table.meta['DATE'] = (
        f'{Time.now().to_value("iso", subfmt="date_hm")}', 'date file was generated')

    if file_format == 'fits':
        peak_table.write(path_to_file, format='fits', overwrite=True)

    elif file_format == 'ecsv':
        meta = OrderedDict()
        for key, val in peak_table.meta.items():
            meta[key] = val
        peak_table.meta = meta
        peak_table.write(path_to_file, format='ascii.ecsv', overwrite=True)