import os

# NumPy
import numpy as np
# AstroPy
from astropy.io import ascii, fits
from astropy.time import Time
from astropy.table import Table

from __init__ import __version__ as version


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