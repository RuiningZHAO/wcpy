# -*- coding: utf-8 -*-
import os, warnings

# PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
# NumPy
import numpy as np
# SciPy
from scipy import interpolate
from scipy.signal import find_peaks
# matplotlib
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
# AstroPy
import astropy.units as u
from astropy.table import Table
# drpy
from drpy.onedspec.center import refinePeaks
from drpy.modeling import Poly1D, Spline1D

from .__init__ import __version__
from .ui import Ui_MainWindow, InformationBox, CheckBoxFileDialog, tableFont
from .io import loadLineList, loadSpectrum, saveSpectrum, savePeakTable

# Set plot parameters
plt.rcParams['axes.linewidth'] = 1
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'


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


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        
        # Call `QtWidgets.QMainWindow.__init__(self, parent)` (RNZ 07/20/2023):
        #   The default arguments are `self` and `None`, which makes `self` also a 
        #   `QtWidgets.QMainWindow` object with no parent.
        super().__init__()

        # Set up UI (RNZ 07/20/2023):
        #  Call the inherited `Ui_MainWindow.setupUi(self, MainWindow)` to set up 
        #  itself.
        self.setupUi(self)

        # Validate line edits
        self.validateLineEdit()

        # Initialize line edit
        self.initializeLineEdit()

        # Install event filter
        self.tableWidget.installEventFilter(self)
        
        # Connect up actions and buttons according to their object name (RNZ 07/20/2023)
        QtCore.QMetaObject.connectSlotsByName(self)
        # Connect up action `exit`
        self.exitAction.triggered.connect(self.close)

        # Disable `saveAction`
        self.saveAction.setEnabled(False)
        # Disable `savePeakAction`
        self.savePeakAction.setEnabled(False)
        # Disable group box `peak`
        self.setEnabled(group='peak', enable=False)
        # Disable group box `line`
        self.setEnabled(group='line', enable=False)
        # Disable group box `disp`
        self.setEnabled(group='disp', enable=False)
        
        # Line list
        self.line_list = None

        # Show residual
        self.show_residual = False

        # Flag
        self.isNewOpen = True


    def validateLineEdit(self):

        # Validate peak parameters
        rx_0_1 = QtCore.QRegExp("^(1|(0(\\.\\d{1,3})?))$")
        rx_0_100 = QtCore.QRegExp("^(100|((\\d{1}|[1-9]{1}[0-9]{1})(\\.\\d{1,2})?))$")
        rx_1_100 = QtCore.QRegExp("^(100|(([1-9]{1}[0-9]?)(\\.\\d{1,2})?))$")
        self.lineEdit_height.setValidator(QtGui.QRegExpValidator(rx_0_1))
        self.lineEdit_threshold.setValidator(QtGui.QRegExpValidator(rx_0_1))
        self.lineEdit_distance.setValidator(QtGui.QRegExpValidator(rx_1_100))
        self.lineEdit_prominence.setValidator(QtGui.QRegExpValidator(rx_0_1))
        self.lineEdit_width.setValidator(QtGui.QRegExpValidator(rx_0_100))
        self.lineEdit_wlen.setValidator(QtGui.QRegExpValidator(rx_0_100))
        self.lineEdit_rel.setValidator(QtGui.QRegExpValidator(rx_0_1))
        self.lineEdit_plateau.setValidator(QtGui.QRegExpValidator(rx_0_100))
        # Not empty
        self.lineEdit_height.textChanged.connect(lambda: self.disableButtonFind(self.lineEdit_height))
        self.lineEdit_threshold.textChanged.connect(lambda: self.disableButtonFind(self.lineEdit_threshold))
        self.lineEdit_distance.textChanged.connect(lambda: self.disableButtonFind(self.lineEdit_distance))
        self.lineEdit_prominence.textChanged.connect(lambda: self.disableButtonFind(self.lineEdit_prominence))
        self.lineEdit_width.textChanged.connect(lambda: self.disableButtonFind(self.lineEdit_width))
        self.lineEdit_wlen.textChanged.connect(lambda: self.disableButtonFind(self.lineEdit_wlen))
        self.lineEdit_rel.textChanged.connect(lambda: self.disableButtonFind(self.lineEdit_rel))
        self.lineEdit_plateau.textChanged.connect(lambda: self.disableButtonFind(self.lineEdit_plateau))

        # Validate autoid parameters
        rx_positive = QtCore.QRegExp("^([1-9]\d*)|([1-9]\d*\.\d*)|(0\.\d*[1-9]\d*)|()$")
        self.lineEdit_tolerance.setValidator(QtGui.QRegExpValidator(rx_positive))
        # Not empty
        self.lineEdit_tolerance.textChanged.connect(lambda: self.disableButtonAutoid(self.lineEdit_tolerance))

        # Validate fit parameters
        rx_1_20 = QtCore.QRegExp("^(20|([2-9]{1})|(1\\d?))$")
        rx_0_5 = QtCore.QRegExp("^(5|([0-4](\\.\\d{1,2})?))$")
        rx_0_10 = QtCore.QRegExp("^(10|\\d{1})$")
        self.lineEdit_degree.setValidator(QtGui.QRegExpValidator(rx_1_20))
        self.lineEdit_npieces.setValidator(QtGui.QRegExpValidator(rx_1_20))
        self.lineEdit_maxiters.setValidator(QtGui.QRegExpValidator(rx_0_10))
        self.lineEdit_sigma_lower.setValidator(QtGui.QRegExpValidator(rx_0_5))
        self.lineEdit_sigma_upper.setValidator(QtGui.QRegExpValidator(rx_0_5))
        # Not empty
        self.lineEdit_degree.textChanged.connect(lambda: self.disableButtonFit(self.lineEdit_degree))
        self.lineEdit_npieces.textChanged.connect(lambda: self.disableButtonFit(self.lineEdit_npieces))
        self.lineEdit_maxiters.textChanged.connect(lambda: self.disableButtonFit(self.lineEdit_maxiters))
        self.lineEdit_sigma_lower.textChanged.connect(lambda: self.disableButtonFit(self.lineEdit_sigma_lower))
        self.lineEdit_sigma_upper.textChanged.connect(lambda: self.disableButtonFit(self.lineEdit_sigma_upper))


    def initializeLineEdit(self):

        # Default peak parameters
        self.lineEdit_height.setText('0')
        self.lineEdit_threshold.setText('0')
        self.lineEdit_distance.setText('10')
        self.lineEdit_prominence.setText('0.05')
        self.lineEdit_width.setText('8')
        self.lineEdit_wlen.setText('20')
        self.lineEdit_rel.setText('0.5')
        self.lineEdit_plateau.setText('0')

        # Default line parameters
        self.lineEdit_lineList.setText('<line list>')
        self.lineEdit_tolerance.setText('10')

        # Default fit parameters
        self.lineEdit_degree.setText('1')
        self.lineEdit_npieces.setText('1')
        self.lineEdit_maxiters.setText('0')
        self.lineEdit_sigma_lower.setText('3')
        self.lineEdit_sigma_upper.setText('3')


    def disableButtonFind(self, LineEdit):
        """Enable or disable the Button Find"""

        if len(LineEdit.text()) == 0:
            self.button_find.setEnabled(False)

        else:
            self.button_find.setEnabled(True)


    def disableButtonFit(self, LineEdit):
        """Enable or disable the Button Fit"""

        if len(LineEdit.text()) == 0:
            self.button_fit.setEnabled(False)

        else:
            self.button_fit.setEnabled(True)


    def disableButtonAutoid(self, LineEdit):
        """Enable or disable the Button Autoid"""

        if len(LineEdit.text()) == 0:
            self.button_autoid.setEnabled(False)

        else:
            self.button_autoid.setEnabled(True)


    def setEnabled(self, group, enable):
        """Enable or disable group box."""

        if group == 'peak':
            # Disable tool bar
            self.toolBar_spec.setEnabled(enable)
            # Disable peak parameters
            self.lineEdit_height.setEnabled(enable)
            self.lineEdit_threshold.setEnabled(enable)
            self.lineEdit_distance.setEnabled(enable)
            self.lineEdit_prominence.setEnabled(enable)
            self.lineEdit_width.setEnabled(enable)
            self.lineEdit_wlen.setEnabled(enable)
            self.lineEdit_rel.setEnabled(enable)
            self.lineEdit_plateau.setEnabled(enable)
            # Disable button
            self.button_find.setEnabled(enable)
        
        elif group == 'line':
            # Disable auto parameters
            self.lineEdit_tolerance.setEnabled(enable)
            # Disable buttons
            self.button_load.setEnabled(enable)
            self.button_unload.setEnabled(enable)
            self.button_autoid.setEnabled(enable)
            self.button_undo.setEnabled(enable)
            # Disable line table
            self.tableWidget.setEnabled(enable)
            # Disable combo box
            self.comboBox.setEnabled(enable)

        elif group == 'disp':
            # Disable tool bar
            self.toolBar_fit.setEnabled(enable)
            # Disable fit parameters
            self.tabWidget.setEnabled(enable)
            self.lineEdit_degree.setEnabled(enable)
            self.lineEdit_npieces.setEnabled(enable)
            self.lineEdit_maxiters.setEnabled(enable)
            self.lineEdit_sigma_lower.setEnabled(enable)
            self.lineEdit_sigma_upper.setEnabled(enable)
            # Disable buttons
            self.button_residual.setEnabled(enable)
            self.button_fit.setEnabled(enable)
            self.button_mask.setEnabled(enable)
            self.button_unmask.setEnabled(enable)


    def setCompleter(self):
        """Set auto-completer for cells in the table.
        
        Call this function after the table widget or ``self.line_list`` been updated.
        """

        for i in range(self.tableWidget.rowCount()):
            self.tableWidget.item(i, 0).setData(QtCore.Qt.UserRole, self.line_list)


    def setupCell(self, row, column, text='', isChecked=False):

        # Column `WAVELENGTH`
        if column == 'wavelength':
            item = QtWidgets.QTableWidgetItem(text)
            item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            item.setFont(tableFont)
            item.setData(QtCore.Qt.UserRole, self.line_list) # set completer
            self.tableWidget.setItem(row, 0, item)

        # Column `MASK`
        elif column == 'mask':

            cell_widget = QtWidgets.QWidget()

            cell_layout = QtWidgets.QHBoxLayout(cell_widget)
            cell_layout.setAlignment(QtCore.Qt.AlignCenter)
            cell_layout.setContentsMargins(0, 0, 0, 0)

            checkBox = QtWidgets.QCheckBox()
            cell_widget.checkState = checkBox.checkState
            cell_widget.setCheckState = checkBox.setCheckState
            if isChecked:
                checkBox.setCheckState(QtCore.Qt.Checked)
            else:
                checkBox.setCheckState(QtCore.Qt.Unchecked)
            cell_layout.addWidget(checkBox)

            self.tableWidget.setCellWidget(row, 1, cell_widget)


    def eventFilter(self, source, event):
        """copy, paste, cut, and delete"""

        if event.type() == QtCore.QEvent.KeyPress:

            if event.matches(QtGui.QKeySequence.Copy):
                self.copySelection()
                return True

            elif event.matches(QtGui.QKeySequence.Paste):
                self.pasteSelection()
                return True

            elif (event.matches(QtGui.QKeySequence.Delete) | (event.key() == QtCore.Qt.Key_Backspace)):
                self.deleteSelection()
                return True

            elif event.matches(QtGui.QKeySequence.Cut):
                self.copySelection()
                self.deleteSelection()
                return True

        return super().eventFilter(source, event)


    def copySelection(self):

        index_list = self.tableWidget.selectedIndexes()

        if index_list:

            isNone_list = [index.data() is None for index in index_list]
            index_list = sorted(
                index for index, isNone in zip(index_list, isNone_list) if not isNone)

            if index_list:

                copy_text = ''

                for index in index_list:
                    copy_text += index.data() + '\r\n'

                QtWidgets.qApp.clipboard().setText(copy_text)


    def pasteSelection(self):

        index_list = self.tableWidget.selectedIndexes()

        if index_list:

            isNone_list = [index.data() is None for index in index_list]
            index_list = sorted(
                index for index, isNone in zip(index_list, isNone_list) if not isNone)

            if index_list:

                if len(index_list) == (index_list[-1].row() - index_list[0].row() + 1):

                    paste_text = QtWidgets.qApp.clipboard().text()
                    paste_text_list = [
                        text.strip('\r') for text in paste_text.split('\n')]

                    while paste_text_list:

                        if paste_text_list[-1] == '':
                            paste_text_list = paste_text_list[:-1]

                        else:
                            break

                    row0 = index_list[0].row()

                    for i in range(len(paste_text_list)):

                        if row0 + i < self.tableWidget.rowCount():
                            self.tableWidget.item(row0 + i, 0).setText(paste_text_list[i])


    def deleteSelection(self):

        index_list = self.tableWidget.selectedIndexes()

        if index_list:

            isNone_list = [index.data() is None for index in index_list]
            index_list = sorted(
                index for index, isNone in zip(index_list, isNone_list) if not isNone)

            if index_list:

                for index in index_list:
                    self.tableWidget.item(index.row(), 0).setText('')


    # Slot decorator (RNZ 07/20/2023):
    #   Without it, the slot function will be called twice.
    @QtCore.pyqtSlot()
    def on_open_triggered(self):
        """Get ``self.path_to_file``, ``self.file_format`` and ``self.reverse`` 
        through a file dialog."""

        openFileDialog = CheckBoxFileDialog(checkBox_text='Reverse spectral axis')

        if self.path_to_file is not None:
            openFileDialog.selectFile(self.path_to_file)

        openFileDialog.setNameFilters(
            ['FITS (*.fits *.fit *.FITS *.FIT)', 'Enhanced CSV Files (*.ecsv)', 
            'ASCII Files (*.*)'])
        # Default is FITS (RNZ 07/20/2023)
        if self.file_format == 'ecsv':
            openFileDialog.selectNameFilter('Enhanced CSV Files (*.ecsv)')
        elif self.file_format == 'ascii':
            openFileDialog.selectNameFilter('ASCII Files (*.*)')

        openFileDialog.checkBox.setChecked(self.reverse)

        if openFileDialog.exec_() == QtWidgets.QDialog.Accepted:

            self.path_to_file = openFileDialog.selectedUrls()[0].toLocalFile()

            if openFileDialog.selectedNameFilter().startswith('FITS'):
                self.file_format = 'fits'
            elif openFileDialog.selectedNameFilter().startswith('Enhanced'):
                self.file_format = 'ecsv'
            else:
                self.file_format = 'ascii'

            self.reverse = openFileDialog.checkBox.checkState() == QtCore.Qt.Checked

            self._loadSpectrum()


    @QtCore.pyqtSlot()
    def on_save_triggered(self):
        """Save calibrated spectrum

        Save ``self.spectrum`` to file.
        """

        saveFileDialog = CheckBoxFileDialog()
        saveFileDialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        saveFileDialog.setNameFilters(
            ['FITS (*.fits *.fit *.FITS *.FIT)', 'Enhanced CSV Files (*.ecsv)'])
        
        if not hasattr(self, 'path_to_save'):
            saveFileDialog.selectFile(os.path.splitext(self.path_to_file)[0])
        else:
            saveFileDialog.selectFile(self.path_to_save)

        if saveFileDialog.exec_() == QtWidgets.QDialog.Accepted:

            self.path_to_save = saveFileDialog.selectedUrls()[0].toLocalFile()

            extension = os.path.splitext(self.path_to_save)[1]

            if saveFileDialog.selectedNameFilter().startswith('FITS'):

                file_format = 'fits'

                if extension not in ['.fits', '.fit', '.FITS', '.FIT']:
                    self.path_to_save += '.fits'

            elif saveFileDialog.selectedNameFilter().startswith('Enhanced'):
                
                file_format = 'ecsv'

                if extension not in ['.ecsv', '.ECSV']:
                    self.path_to_save += '.ecsv'

            saveSpectrum(
                path_to_file=self.path_to_save, file_format=file_format, 
                spectrum=self.spectrum)
            
            self.statusBar.showMessage(f'{self.path_to_save} saved.', 2000)


    @QtCore.pyqtSlot()
    def on_savePeak_triggered(self):
        """Save peak information.

        Save ``self.peak_table`` to file.
        """

        saveFileDialog = CheckBoxFileDialog()
        saveFileDialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        saveFileDialog.setNameFilters(
            ['FITS (*.fits *.fit *.FITS *.FIT)', 'Enhanced CSV Files (*.ecsv)'])
        
        if not hasattr(self, 'path_to_peak'):
            saveFileDialog.selectFile(os.path.splitext(self.path_to_file)[0])
        else:
            saveFileDialog.selectFile(self.path_to_peak)

        if saveFileDialog.exec_() == QtWidgets.QDialog.Accepted:

            self.path_to_peak = saveFileDialog.selectedUrls()[0].toLocalFile()

            extension = os.path.splitext(self.path_to_peak)[1]

            if saveFileDialog.selectedNameFilter().startswith('FITS'):

                file_format = 'fits'

                if extension not in ['.fits', '.fit', '.FITS', '.FIT']:
                    self.path_to_peak += '.fits'

            elif saveFileDialog.selectedNameFilter().startswith('Enhanced'):
                
                file_format = 'ecsv'

                if extension not in ['.ecsv', '.ECSV']:
                    self.path_to_peak += '.ecsv'

            savePeakTable(
                path_to_file=self.path_to_peak, file_format=file_format, 
                peak_table=self.peak_table)
            
            self.statusBar.showMessage(f'{self.path_to_peak} saved.', 2000)


    @QtCore.pyqtSlot()
    def on_about_triggered(self):

        text = (
            'Wavelength Calibrator (ver <a href='
            f"'https://pypi.org/project/astro-drpy/{__version__}'>{__version__}</a> "
            'released on 2023-08-06) is a graphical user interface to facilitate '
            'wavelength calibration. It is developed by '
            f"<a href='mailto: ruiningzhao@mail.bnu.edu.cn'>Ruining Zhao</a> "
            'at National Astronomical Observatories, Chinese Academy of Sciences. '
            'Report issue via '
            "<a href='https://github.com/RuiningZHAO/wcpy/issues'>GitHub</a>."
        )
        messageBox = InformationBox(window_title='Wavelength Calibrator', text=text)
        messageBox.setTextFormat(QtCore.Qt.RichText)
        messageBox.exec_()


    # todo: dynamic xlabel and ylabel
    @QtCore.pyqtSlot()
    def on_find_clicked(self):
        """Find peaks.

        Find peaks (local maximal) in ``self.count``. ``self.peaks`` and 
        ``self.properties`` are generated. ``self.peak_lib`` is updated.
        """

        self._clearFit()

        # Save old contents
        rowCount_old = self.tableWidget.rowCount()
        if rowCount_old > 0:
            for i in range(rowCount_old):
                # Use integer as key (RNZ 07/20/2023):
                #   In most cases, two peaks would not be round to the same integer.
                self.peak_lib[int(self.peaks[i])] = (
                    self.tableWidget.item(i, 0).text(), 
                    self.tableWidget.cellWidget(i, 1).checkState()
                )

        # Get peak parameters
        height = float(self.lineEdit_height.text())
        threshold = float(self.lineEdit_threshold.text())
        distance = float(self.lineEdit_distance.text())
        prominence = float(self.lineEdit_prominence.text())
        width = float(self.lineEdit_width.text())
        wlen = float(self.lineEdit_wlen.text())
        rel = float(self.lineEdit_rel.text())
        plateau = float(self.lineEdit_plateau.text())

        # Find peaks
        peaks, properties = find_peaks(
            x=self.count, height=height, threshold=threshold, distance=distance, 
            prominence=prominence, width=width, wlen=wlen, rel_height=rel, 
            plateau_size=plateau)

        # Refine peaks
        if peaks.shape[0] > 0:
            self.peaks, self.properties, _ = refinePeaks(
                spectrum=self.count, peaks=peaks, properties=properties)

        else:
            self.peaks = peaks
            self.properties = properties

        # Set up table
        self.tableWidget.setRowCount(len(self.peaks))

        # Auto-fill peaks in the library.
        for i in range(self.tableWidget.rowCount()):

            if int(self.peaks[i]) in self.peak_lib.keys():

                text, isChecked = self.peak_lib[int(self.peaks[i])]
                # Column `WAVELENGTH`
                self.setupCell(row=i, column='wavelength', text=text)
                # Column `MASK`
                self.setupCell(row=i, column='mask', isChecked=isChecked)

            else:

                # Column `WAVELENGTH`
                self.setupCell(row=i, column='wavelength', text='')
                # Column `MASK`
                self.setupCell(row=i, column='mask', isChecked=False)

            # Row height
            self.tableWidget.verticalHeader().setSectionResizeMode(
                i, QtWidgets.QHeaderView.ResizeToContents)

        # Plot
        xlabel = 'spectral axis [pixel]'
        ylabel = 'flux'
        if self.unit_count.to_string():
            ylabel += f' [{self.unit_count.to_string()}]'

        self.figure_spec.clear()
        ax = self.figure_spec.add_subplot(111)
        trans = transforms.blended_transform_factory(
            ax.transData, ax.transAxes)
        for i, peak in enumerate(self.peaks):
            ax.plot([peak, peak], [0.0, 0.87], 'r--', transform=trans, lw=0.8)
            ax.plot([peak, peak], [0.94, 1.0], 'r--', transform=trans, lw=0.8)
            ax.annotate(
                f'{i + 1:d}', xy=(peak, 0.9), xycoords=trans, ha='center', va='center', 
                fontsize=12, color='r', annotation_clip=True)
        plotSpectrum(
            ax=ax, x=self.index, y=self.count, xlim=(self.index.min(), self.index.max()), 
            ylim=(-0.05, 1.15), xlabel=xlabel, ylabel=ylabel)
        self.figure_spec.tight_layout(pad=0.2)
        self.figureCanvas_spec.draw()


    @QtCore.pyqtSlot()
    def on_load_clicked(self):
        """Get ``self.path_to_line_list`` through a file dialog."""

        fileDialog = QtWidgets.QFileDialog()

        if self.path_to_line_list is not None:
            fileDialog.selectFile(self.path_to_line_list)

        fileDialog.setNameFilters(['ASCII Files (*.*)'])

        if fileDialog.exec_() == QtWidgets.QDialog.Accepted:

            self.path_to_line_list = fileDialog.selectedUrls()[0].toLocalFile()

            self._loadLineList()


    @QtCore.pyqtSlot()
    def on_unload_clicked(self):
        """Unload line list."""

        if self.line_list is not None:

            self.line_list = None
            # Unset completer
            self.setCompleter()

            # Show information
            self.lineEdit_lineList.setText('<None>')
            self.statusBar.showMessage(f'Line list unloaded.', 2000)


    @QtCore.pyqtSlot()
    def on_autoid_clicked(self):
        """Auto-identify unlabeled peaks according to the line list.
        
        self.wave_input
        """

        if self.line_list is None:

            text = (
                'Line list is needed for auto-identification. '
                'Load a line list first and try again.'
            )
            messageBox = InformationBox(window_title='Wavelength Calibrator', text=text)
            messageBox.exec_()
            
            return None

        # Get input lines
        self._getLines()

        if self.n_line < 2:

            messageBox = InformationBox(
                window_title='Wavelength Calibrator', 
                text='Identify two lines (at least) first to auto-identify.')
            messageBox.exec_()
            
            return None

        labeled = np.where(~np.isnan(self.wave_input))[0]
        unlabeled = np.where(np.isnan(self.wave_input))[0]

        # Check order and reverse or not
        if np.all(self.wave_input[labeled][:-1] < self.wave_input[labeled][1:]):

            isReversed = False

        elif np.all(self.wave_input[labeled][:-1] > self.wave_input[labeled][1:]):

            isReversed = True

        else:

            messageBox = InformationBox(
                window_title='Wavelength Calibrator', 
                text='Input lines should be in strict ascending or descending order.')
            messageBox.exec_()

            return None

        line_arr = np.array([float(line) for line in self.line_list])
        peak_arr = self.peaks[unlabeled]
        wave_arr = interpolate.interp1d(
            self.peaks[labeled], self.wave_input[labeled], bounds_error=False, 
            fill_value='extrapolate', assume_sorted=True)(peak_arr)

        line_peak = np.zeros(wave_arr.shape[0]) + np.nan
        dist_peak = np.zeros(wave_arr.shape[0]) + np.nan

        for i in range(labeled.shape[0] + 1):
            
            if i == 0:

                line_cri = self.wave_input[labeled][0]
                if isReversed:
                    line_subarr = line_arr[(line_arr > line_cri)]
                else:
                    line_subarr = line_arr[(line_arr < line_cri)]
                indx_subarr = np.where(peak_arr < self.peaks[labeled][0])[0]

            elif i == labeled.shape[0]:

                line_cri = self.wave_input[labeled][-1]
                if isReversed:
                    line_subarr = line_arr[(line_cri > line_arr)]
                else:
                    line_subarr = line_arr[(line_cri < line_arr)]
                indx_subarr = np.where(self.peaks[labeled][-1] < peak_arr)[0]

            else:

                line_min, line_max = (
                    self.wave_input[labeled][(i - 1)], self.wave_input[labeled][i])
                if isReversed:
                    line_min, line_max = line_max, line_min
                line_subarr = line_arr[(line_min < line_arr) & (line_arr < line_max)]
                peak_min, peak_max = (
                    self.peaks[labeled][(i - 1)], self.peaks[labeled][i])
                indx_subarr = np.where((peak_min < peak_arr) & (peak_arr < peak_max))[0]
            
            # Skip if empty
            if (not line_subarr.size) | (not indx_subarr.size):
                continue
            
            # Assign
            for j in indx_subarr:

                # Distance
                dist_subarr = np.abs(wave_arr[j] - line_subarr)
                # Sort
                indx_sorted = dist_subarr.argsort()
                dist_sorted = dist_subarr[indx_sorted]
                line_sorted = line_subarr[indx_sorted]

                for k in range(line_sorted.shape[0]):

                    if line_sorted[k] not in line_peak:
                        line_peak[j] = line_sorted[k]
                        dist_peak[j] = dist_sorted[k]
                        break
                    else:
                        indx = np.where(line_peak == line_sorted[k])[0][0]
                        if dist_peak[indx] > dist_sorted[k]:
                            line_peak[j] = line_sorted[k]
                            dist_peak[j] = dist_sorted[k]
                            line_peak[indx] = np.nan
                            dist_peak[indx] = np.nan
                        else:
                            break
            
        # Filter
        distance = np.abs(wave_arr - line_peak)
        tolerance = float(self.lineEdit_tolerance.text())
        line_peak[distance >= tolerance] = np.nan

        toLabel = ~np.isnan(line_peak)
        if toLabel.sum() > 0:
            
            self.unlabeled = unlabeled[toLabel]

            # Fill in
            for i, line in zip(self.unlabeled, line_peak[toLabel]):
                self.tableWidget.item(i, 0).setText(str(line))


    @QtCore.pyqtSlot()
    def on_undo_clicked(self):
        """Remove the lines auto-labeled by the auto-identification algorithm.
        
        Work if ``self.unlabeled`` exists and delete ``self.unlabeled`` afterwards. 
        Otherwise do nothing.
        """
        
        if hasattr(self, 'unlabeled'):

            for i in self.unlabeled:
                self.tableWidget.item(i, 0).setText('')

            del self.unlabeled


    @QtCore.pyqtSlot()
    def on_residual_clicked(self):

        self.show_residual = self.button_residual.isChecked()

        if hasattr(self, 'ax_fit'):
            self._plotFitting()


    @QtCore.pyqtSlot()
    def on_fit_clicked(self):
        """Fit dispersion solution.

        Use ``self.peaks``, ``self.wave_input``, and ``self.mask_input`` to fit a 
        dispersion solution. Then apply such solution to the whole ``self.index`` 
        array. ``self.rms`` is calculated. ``self.masked`` is generated. 
        ``self.spectrum`` and ``self.peak_table`` are generated for saving.
        """

        # Get input lines
        self._getLines()

        if self.n_line == 0:

            messageBox = InformationBox(
                window_title='Wavelength Calibrator', 
                text='There is no unmasked peak. Find peak first and try again.')
            messageBox.exec_()
            
            return None

        # Get fit parameters
        maxiters = int(self.lineEdit_maxiters.text())
        if maxiters == 0:
            sigma_lower = None
            sigma_upper = None
        else:
            sigma_lower = float(self.lineEdit_sigma_lower.text())
            sigma_upper = float(self.lineEdit_sigma_upper.text())

        # Get method
        method = self.tabWidget.currentWidget().objectName()

        if method == 'poly':

            # Get fit parameters
            degree = int(self.lineEdit_degree.text())

            # Fit polynomial function
            try:

                with warnings.catch_warnings():
                    warnings.simplefilter('error', np.RankWarning)
                    spl, self.residual, _, _, master_mask = Poly1D(
                        x=self.peaks, y=self.wave_input, w=None, m=self.mask_input, 
                        deg=degree, maxiters=maxiters, sigma_lower=sigma_lower, 
                        sigma_upper=sigma_upper, grow=False, use_relative=False)

            except np.RankWarning:

                messageBox = InformationBox(
                    window_title='Wavelength Calibrator', 
                    text='The number of points must exceed the degree of polynomial.')
                messageBox.exec_()

                return None
            
            # Deal with exceptions here.
            except Exception as err:

                if self.debug:
                    text = f'{err}'
                else:
                    text = 'Fitting error.'
                messageBox = InformationBox(
                    window_title='Wavelength Calibrator', text=text)
                messageBox.exec_()

                return None

        elif method == 'spline3':

            # Get fit parameters
            n_piece = int(self.lineEdit_npieces.text())

            # Fit cubic spline function
            try:

                spl, self.residual, _, _, master_mask = Spline1D(
                    x=self.peaks, y=self.wave_input, w=None, m=self.mask_input, 
                    order=3, n_piece=n_piece, maxiters=maxiters, 
                    sigma_lower=sigma_lower, sigma_upper=sigma_upper, 
                    use_relative=False)

            # Deal with exceptions here.
            except Exception as err:

                if self.debug:
                    text = f'{err}'
                else:
                    text = 'Fitting error.'
                messageBox = InformationBox(
                    window_title='Wavelength Calibrator', text=text)
                messageBox.exec_()

                return None

        if maxiters > 0:
            self.masked = np.where((~self.mask_input) != (~master_mask))[0]

        # Wavelength
        wavelength = spl(self.index)

        # Unit
        unit_wavelength = u.Unit(self.comboBox.currentText())

        # RMS
        rms = np.sqrt(
            (self.residual[~self.mask_input]**2).sum() / (~self.mask_input).sum())
        self.rms = round(number=rms, ndigits=3)

        # Spectrum
        self.spectrum = Table(
            data=[(wavelength * unit_wavelength), (self.count * self.unit_count)], 
            names=('spectral_axis', 'flux'), 
            meta=self.header
        )

        header_peak = {
            'EXTNAME': ('peak', 'name of the extension'), 
            'PEAKUSED': ((~self.mask_input).sum(), 'number of peaks used'), 
            'PEAKDETE': (self.wave_input.shape[0], 'number of peaks detected'), 
            'RMS': (self.rms, 'root mean squared of fitting'), 
            'METHOD': (method, 'fitting method')
        }
        if method == 'poly':
            header_peak['DEGREE'] = (degree, 'parameter of fitting method')

        elif method == 'spline3':
            header_peak['PIECE'] = (n_piece, 'parameter of fitting method')

        # Peak table
        self.peak_table = Table(
            data=[(self.peaks[~self.mask_input] * u.pixel), 
                  (self.properties['peak_heights'][~self.mask_input] * self.unit_count), 
                  (self.properties['left_bases'][~self.mask_input] * u.pixel), 
                  (self.properties['right_bases'][~self.mask_input] * u.pixel), 
                  (self.wave_input[~self.mask_input] * unit_wavelength)], 
            names=('peaks', 'heights', 'left_bases', 'right_bases', 'spectral_axis'), 
            meta=header_peak
        )

        # Plot
        self._plotFitting()

        # Enable save actions
        self.saveAction.setEnabled(True)
        self.savePeakAction.setEnabled(True)


    @QtCore.pyqtSlot()
    def on_mask_clicked(self):
        """Apply mask of the sigma clipping."""

        if hasattr(self, 'masked'):
            for i in self.masked:
                self.tableWidget.cellWidget(i, 1).setCheckState(QtCore.Qt.Checked)


    @QtCore.pyqtSlot()
    def on_unmask_clicked(self):
        """Remove the mask of the sigma clipping."""

        if hasattr(self, 'masked'):
            for i in self.masked:
                self.tableWidget.cellWidget(i, 1).setCheckState(QtCore.Qt.Unchecked)


    def _clearFind(self):
        """Clear previous peak-finding."""

        # External
        self.tableWidget.setRowCount(0)

        # Internal (RNZ 07/20/2023):
        #   There is no need to clear ``self.peaks`` and ``self.properties`` here, as 
        #   they will never be used before the row count been checked. If the row count 
        #   is `0`, they will not be called, otherwise, they are assigned properly in 
        #   advance.
        self.peak_lib = dict()


    def _clearFit(self):
        """Clear previous fitting."""

        if hasattr(self, 'masked'):
            del self.masked

        if hasattr(self, 'spectrum'):
            del self.spectrum

        if hasattr(self, 'peak_table'):
            del self.peak_table

        # Clear plot
        if hasattr(self, 'ax_fit'):
            del self.ax_fit

        self.figure_fit.clear()
        self.figureCanvas_fit.draw()

        # Disable save actions
        self.saveAction.setEnabled(False)
        self.savePeakAction.setEnabled(False)


    def _loadSpectrum(self):
        """Load spectrum.
        
        Take ``self.path_to_file``, ``self.file_format`` and ``self.reverse`` (from 
        file dialog or from command line) as input, and load spectrum if no exception 
        raised. ``self.index``, ``self.count`` ``self.unit_count``, ``self.header`` 
        and ``self.peak_lib`` will be generated)
        """

        # Catch exceptions (RNZ 07/20/2023):
        #   Exception can be used as a wildcard that catches (almost) everything. 
        #   However, it is good practice to be as specific as possible with the types 
        #   of exceptions that we intend to handle, and to allow any unexpected 
        #   exceptions to propagate on.
        try:

            self.index, self.count, self.unit_count, self.header = loadSpectrum(
                path_to_file=self.path_to_file, file_format=self.file_format, 
                reverse=self.reverse)

            self._plotSpectrum()

        # Deal with exceptions here.
        except Exception as err:

            if self.debug:
                text = f'{err}'
            else:
                text = (
                    'Wavelength Calibrator could not open '
                    f"'{os.path.basename(self.path_to_file)}' "
                    'because it is either not a supported file '
                    'type or because the file has been damaged.'
                )
            messageBox = InformationBox(
                window_title='Wavelength Calibrator', text=text)
            messageBox.exec_()

            return None

        # Clear everything except line list
        self._clearFind()
        self._clearFit()

        if self.isNewOpen:

            self.isNewOpen = False

            # Enable group box `peak`
            self.setEnabled(group='peak', enable=True)
            self.setEnabled(group='line', enable=True)
            self.setEnabled(group='disp', enable=True)


    def _loadLineList(self):
        """Load line list.

        Take ``self.path_to_line_list`` (from file dialog or from command line) as 
        input, and load line list if no exception raised. ``self.line_list`` will be 
        generated)
        """

        # Catch exceptions (RNZ 07/20/2023):
        #   Exception can be used as a wildcard that catches (almost) everything. 
        #   However, it is good practice to be as specific as possible with the types 
        #   of exceptions that we intend to handle, and to allow any unexpected 
        #   exceptions to propagate on.
        try:
            self.line_list = loadLineList(path_to_line_list=self.path_to_line_list)

        except Exception as err:

            if self.debug:
                text = f'{err}'
            else:
                text = (
                    'Wavelength Calibrator could not load '
                    f"'{os.path.basename(self.path_to_line_list)}' "
                    'as a line list, either because the format is '
                    'not supported or because the file has been '
                    'damaged.\n\n'
                    'An ascii file with one numeric column is '
                    'expected. Multiple columns are allowed, if '
                    'delimited by space, but only the first column '
                    'is used.'
                )
            messageBox = InformationBox(
                window_title='Wavelength Calibrator', text=text)
            messageBox.exec_()

            return None

        # Set completer
        self.setCompleter()

        # Show information
        basename = os.path.basename(self.path_to_line_list)
        self.statusBar.showMessage(f'Line list {basename} loaded.', 2000)
        self.lineEdit_lineList.setText(basename)


    def _getLines(self):
        """Get lines in the table."""

        self.wave_input = np.zeros(self.tableWidget.rowCount())
        self.mask_input = np.zeros(self.tableWidget.rowCount(), dtype=bool)

        for i in range(self.tableWidget.rowCount()):

            try:
                w = float(self.tableWidget.item(i, 0).text())
                m = bool(self.tableWidget.cellWidget(i, 1).checkState())

            except:
                w = np.nan
                m = True

            self.wave_input[i] = w
            self.mask_input[i] = m

        # Number of lines
        self.n_line = (~self.mask_input).sum()


    def _plotSpectrum(self):
        """Plot spectrum.

        Take ``self.index``, ``self.count``, ``self.unit_count`` as input.
        """

        if not self.isNewOpen:
            self.figure_spec.clear()

        xlabel = 'spectral axis [pixel]'
        ylabel = 'flux'
        if self.unit_count.to_string():
            ylabel += f' [{self.unit_count.to_string()}]'

        ax = self.figure_spec.add_subplot(111)
        plotSpectrum(
            ax=ax, x=self.index, y=self.count, xlim=(self.index.min(), self.index.max()), 
            ylim=(-0.05, 1.15), xlabel=xlabel, ylabel=ylabel)
        self.figure_spec.tight_layout(pad=0.2)
        self.figureCanvas_spec.draw()


    def _plotFitting(self):
        """self.wave_index -> self.spectrum.spectral_axis

        Input: ``self.show_residual``, ``self.wave_input``, ``self.peaks``, 
        ``self.mask_input``, ``self.spectrum``, ``self.residual``, ``self.rms``
        Output: None
        """

        data = self.spectrum['spectral_axis'].data
        unit = self.spectrum['spectral_axis'].unit.to_string()

        xlabel = f'spectral axis [{unit}]'
        ylabel = f'residuals [{unit}]'

        self.figure_fit.clear()
        self.ax_fit = self.figure_fit.add_subplot(111)

        if not self.show_residual:

            self.ax_fit.plot(
                self.wave_input[self.mask_input], self.peaks[self.mask_input], 'x', 
                c='grey', ms=8)
            self.ax_fit.plot(
                self.wave_input[~self.mask_input], self.peaks[~self.mask_input], 'x', 
                c='red', ms=8)
            self.ax_fit.plot(data, self.index, 'k-', lw=0.8)
            self.ax_fit.set_ylabel('dispersion axis [pixel]', fontsize=12)

        else:

            self.ax_fit.plot(
                self.wave_input[~self.mask_input], self.residual[~self.mask_input], 
                'x', c='red', ms=8)
            self.ax_fit.axhline(y=0, ls='--', color='k', lw=0.8)

            for i, peak in enumerate(self.peaks):

                if self.mask_input[i]:
                    self.ax_fit.annotate(
                        f'{i + 1:d}', (self.wave_input[i], 0), xycoords='data', 
                        ha='center', va='center', fontsize=12, color='grey')

                else:
                    self.ax_fit.annotate(
                        f'{i + 1:d}', (self.wave_input[i], 0), xycoords='data', 
                        ha='center', va='center', fontsize=12, color='r')

            self.ax_fit.set_ylabel(ylabel, fontsize=12)

        self.ax_fit.tick_params(
            which='major', direction='in', top=True, right=True, length=5, width=1.5, 
            labelsize=12)
        self.ax_fit.tick_params(
            which='minor', direction='in', top=True, right=True, length=3, width=1.5, 
            labelsize=12)
        self.ax_fit.set_xlim(data.min(), data.max())
        self.ax_fit.set_xlabel(xlabel, fontsize=12)
        self.ax_fit.annotate(
            f'$N={(~self.mask_input).sum()}/{self.wave_input.shape[0]}' + '$, $\\rm{RMS}=' + f'{self.rms}$',
            xy=(0.98, 0.1), xycoords='axes fraction', ha='right', fontsize=12)
        self.figure_fit.tight_layout(pad=0.2, h_pad=0)
        self.figureCanvas_fit.draw()