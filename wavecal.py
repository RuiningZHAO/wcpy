# -*- coding: utf-8 -*-
import os, sys, argparse, warnings
# PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
# NumPy
import numpy as np
# AstroPy
from astropy.table import Table
# Plot
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
# Set plot parameters
plt.rcParams['axes.linewidth'] = 1
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'

from ui_mainwindow import Ui_MainWindow

# fonts
from fonts import table_font
# widgets
from widgets import CheckBoxFileDialog
# utils
from utils import loadSpectrum, saveSpectrum, findPeaks, fitCubicSpline

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        # Set up the user interface from Designer.
        self.setupUi(self)

        # Validate lineedit
        self.validateLineEdit()

        # Initialize lineedit
        self.initializeLineEdit()

        # Install event filter
        self.TableWidget_line.installEventFilter(self)

        # Connect up action `open`
        self.open_action.triggered.connect(self.load)
        # Connect up action `save`
        self.save_action.triggered.connect(self.save)
        # Connect up action `exit`
        self.exit_action.triggered.connect(self.close)
        # Connect up action `about`
        self.about_action.triggered.connect(self.about)
        # Connect up button `Find`
        self.Button_find.clicked.connect(self.find)
        # Connect up the switch button
        self.RectSwitch.clicked.connect(self.switchPlot)
        # Connect up button `Fit`
        self.Button_fit.clicked.connect(self.fitting)

        # Disable `save_action`
        self.save_action.setEnabled(False)
        # Disable group box `peak`
        self.setEnabled(group_box='peak', enable=False)
        # Disable group box `fit`
        self.setEnabled(group_box='fit', enable=False)
        
        # Tab order
        QtCore.QMetaObject.connectSlotsByName(self)
        self.setTabOrder(self.LineEdit_height, self.LineEdit_threshold)
        self.setTabOrder(self.LineEdit_threshold, self.LineEdit_distance)
        self.setTabOrder(self.LineEdit_distance, self.LineEdit_prominence)
        self.setTabOrder(self.LineEdit_prominence, self.LineEdit_width)
        self.setTabOrder(self.LineEdit_width, self.LineEdit_wlen)
        self.setTabOrder(self.LineEdit_wlen, self.LineEdit_rel)
        self.setTabOrder(self.LineEdit_rel, self.LineEdit_plateau)
        self.setTabOrder(self.LineEdit_plateau, self.Button_find)
        self.setTabOrder(self.Button_find, self.LineEdit_npieces)
        self.setTabOrder(self.LineEdit_npieces, self.RectSwitch)
        self.setTabOrder(self.RectSwitch, self.Button_fit)
        self.setTabOrder(self.Button_fit, self.TableWidget_line)
        
        # Flag
        self.isNewOpen = True

    def disableButtonFind(self, LineEdit):
        """
        """

        if len(LineEdit.text()) == 0:
            self.Button_find.setEnabled(False)
        else:
            self.Button_find.setEnabled(True)
    
    def disableButtonFit(self, LineEdit):
        """
        """

        if len(LineEdit.text()) == 0:
            self.Button_fit.setEnabled(False)
        else:
            self.Button_fit.setEnabled(True)

    def validateLineEdit(self):
        # Validate peak parameters
        rx_0_1 = QtCore.QRegExp('^(1|(0(\\.\\d{1,3})?))$')
        rx_0_100 = QtCore.QRegExp('^(100|((\\d{1}|[1-9]{1}[0-9]{1})(\\.\\d{1,2})?))$')
        rx_1_100 = QtCore.QRegExp('^(100|(([1-9]{1}[0-9]?)(\\.\\d{1,2})?))$')
        self.LineEdit_height.setValidator(QtGui.QRegExpValidator(rx_0_1))
        self.LineEdit_threshold.setValidator(QtGui.QRegExpValidator(rx_0_1))
        self.LineEdit_distance.setValidator(QtGui.QRegExpValidator(rx_1_100))
        self.LineEdit_prominence.setValidator(QtGui.QRegExpValidator(rx_0_1))
        self.LineEdit_width.setValidator(QtGui.QRegExpValidator(rx_0_100))
        self.LineEdit_wlen.setValidator(QtGui.QRegExpValidator(rx_0_100))
        self.LineEdit_rel.setValidator(QtGui.QRegExpValidator(rx_0_1))
        self.LineEdit_plateau.setValidator(QtGui.QRegExpValidator(rx_0_100))
        # Not empty
        self.LineEdit_height.textChanged.connect(lambda: self.disableButtonFind(self.LineEdit_height))
        self.LineEdit_threshold.textChanged.connect(lambda: self.disableButtonFind(self.LineEdit_threshold))
        self.LineEdit_distance.textChanged.connect(lambda: self.disableButtonFind(self.LineEdit_distance))
        self.LineEdit_prominence.textChanged.connect(lambda: self.disableButtonFind(self.LineEdit_prominence))
        self.LineEdit_width.textChanged.connect(lambda: self.disableButtonFind(self.LineEdit_width))
        self.LineEdit_wlen.textChanged.connect(lambda: self.disableButtonFind(self.LineEdit_wlen))
        self.LineEdit_rel.textChanged.connect(lambda: self.disableButtonFind(self.LineEdit_rel))
        self.LineEdit_plateau.textChanged.connect(lambda: self.disableButtonFind(self.LineEdit_plateau))

        # Validate fit parameters
        rx_1_20 = QtCore.QRegExp('^(20|([2-9]{1})|(1\\d?))$')
        # rx_0_5 = QtCore.QRegExp('^(5|([0-4](\\.\\d{1,2})?))$')
        # rx_0_10 = QtCore.QRegExp('^(10|\\d{1})$')
        self.LineEdit_npieces.setValidator(QtGui.QRegExpValidator(rx_1_20))
        # self.LineEdit_sig_lower.setValidator(QtGui.QRegExpValidator(rx_0_5))
        # self.LineEdit_sig_upper.setValidator(QtGui.QRegExpValidator(rx_0_5))
        # self.LineEdit_maxiter.setValidator(QtGui.QRegExpValidator(rx_0_10))
        # Not empty
        self.LineEdit_npieces.textChanged.connect(lambda: self.disableButtonFit(self.LineEdit_npieces))
        # self.LineEdit_sig_lower.textChanged.connect(lambda: self.disableButtonFit(self.LineEdit_sig_lower))
        # self.LineEdit_sig_upper.textChanged.connect(lambda: self.disableButtonFit(self.LineEdit_sig_upper))
        # self.LineEdit_maxiter.textChanged.connect(lambda: self.disableButtonFit(self.LineEdit_maxiter))

    def initializeLineEdit(self):
        # Default peak parameters
        self.LineEdit_height.setText('0')
        self.LineEdit_threshold.setText('0')
        self.LineEdit_distance.setText('10')
        self.LineEdit_prominence.setText('0.05')
        self.LineEdit_width.setText('8')
        self.LineEdit_wlen.setText('20')
        self.LineEdit_rel.setText('0.5')
        self.LineEdit_plateau.setText('0')

        # Default fit parameters
        self.LineEdit_npieces.setText('1')
        # self.LineEdit_sig_lower.setText('3')
        # self.LineEdit_sig_upper.setText('3')
        # self.LineEdit_maxiter.setText('1')

    def setEnabled(self, group_box, enable):
        if group_box == 'peak':
            # Disable peak parameters
            self.LineEdit_height.setEnabled(enable)
            self.LineEdit_threshold.setEnabled(enable)
            self.LineEdit_distance.setEnabled(enable)
            self.LineEdit_prominence.setEnabled(enable)
            self.LineEdit_width.setEnabled(enable)
            self.LineEdit_wlen.setEnabled(enable)
            self.LineEdit_rel.setEnabled(enable)
            self.LineEdit_plateau.setEnabled(enable)
            # Disable button `Find`
            self.Button_find.setEnabled(enable)

        elif group_box == 'fit':
            # Disable fit parameters
            self.LineEdit_npieces.setEnabled(enable)
            # self.LineEdit_sig_lower.setEnabled(enable)
            # self.LineEdit_sig_upper.setEnabled(enable)
            # self.LineEdit_maxiter.setEnabled(enable)
            # Disable the switch button
            self.RectSwitch.setEnabled(enable)
            # Disable button `Fit`
            self.Button_fit.setEnabled(enable)

    def setupCell(self, row, column, text='', isChecked=False):
        if column == 'wavelength':
            # Column `WAVELENGTH`
            item = QtWidgets.QTableWidgetItem(text)
            item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            item.setFont(table_font)
            self.TableWidget_line.setItem(row, 0, item)

        elif column == 'mask':
            # Column `MASK`
            cell_widget = QtWidgets.QWidget()
            cell_layout = QtWidgets.QHBoxLayout(cell_widget)
            check_box = QtWidgets.QCheckBox()
            cell_widget.checkState = check_box.checkState
            if isChecked:
                check_box.setCheckState(QtCore.Qt.Checked)
            else:
                check_box.setCheckState(QtCore.Qt.Unchecked)
            cell_layout.addWidget(check_box)
            cell_layout.setAlignment(QtCore.Qt.AlignCenter)
            cell_layout.setContentsMargins(0, 0, 0, 0)
            self.TableWidget_line.setCellWidget(row, 1, cell_widget)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.matches(QtGui.QKeySequence.Copy):
                self.copySelection()
                return True
            elif event.matches(QtGui.QKeySequence.Paste):
                self.pasteSelection()
                return True
            elif event.matches(QtGui.QKeySequence.Delete) | \
                (event.key() == QtCore.Qt.Key_Backspace):
                self.deleteSelection()
                return True
            elif event.matches(QtGui.QKeySequence.Cut):
                self.copySelection()
                self.deleteSelection()
                return True
        return super(MainWindow, self).eventFilter(source, event)

    def copySelection(self):
        index_list = self.TableWidget_line.selectedIndexes()
        if index_list:
            isNone_list = [index.data() is None for index in index_list]
            index_list = sorted(index for index, isNone in zip(index_list, isNone_list) if not isNone)
            if index_list:
                copy_text = ''
                for index in index_list:
                    copy_text += index.data() + '\r\n'
                QtWidgets.qApp.clipboard().setText(copy_text)

    def pasteSelection(self):
        index_list = self.TableWidget_line.selectedIndexes()
        if index_list:
            isNone_list = [index.data() is None for index in index_list]
            index_list = sorted(index for index, isNone in zip(index_list, isNone_list) if not isNone)
            if index_list:
                if len(index_list) == (index_list[-1].row() - 
                                       index_list[0].row() + 1):
                    paste_text = QtWidgets.qApp.clipboard().text()
                    paste_text_list = [text.strip('\r') for text in paste_text.split('\n')]
                    while paste_text_list:
                        if paste_text_list[-1] == '':
                            paste_text_list = paste_text_list[:-1]
                        else:
                            break
                    row0 = index_list[0].row()
                    for i in range(len(paste_text_list)):
                        if row0 + i < self.TableWidget_line.rowCount():
                            self.setupCell(row0 + i, column='wavelength', text=paste_text_list[i])

    def deleteSelection(self):
        index_list = self.TableWidget_line.selectedIndexes()
        if index_list:
            isNone_list = [index.data() is None for index in index_list]
            index_list = sorted(index for index, isNone in zip(index_list, isNone_list) if not isNone)
            if index_list:
                for index in index_list:
                    self.setupCell(index.row(), column='wavelength', text='')

    def plotSpectrum(self):

        if not self.isNewOpen:
            self.Figure_spectrum.clear()
        ax = self.Figure_spectrum.add_subplot(111)
        ax.step(self.index, self.count, 'k-', lw=0.8, where='mid')
        ax.tick_params(which='major', direction='in', top=True, right=True, length=5, width=1, labelsize=12)
        ax.tick_params(which='minor', direction='in', top=True, right=True, length=3, width=1, labelsize=12)
        ax.set_xlim(self.index.min(), self.index.max())
        ax.set_ylim(-0.05, 1.15)
        ax.set_xlabel('Pixel Index', fontsize=12)
        ax.set_ylabel('Normalized Count', fontsize=12)
        self.Figure_spectrum.tight_layout(pad=0.2)
        self.FigureCanvas_spectrum.draw()

    def load(self, external=False):
        """
        self.index
        self.count
        self.peak_lib
        """

        isAccepted = False

        if not external:
            file_dialog = CheckBoxFileDialog(check_box_text='inverse')
            file_dialog.setNameFilters(['ASCII Files (*.*)', 
                                        'Enhanced CSV Files (*.ecsv)', 
                                        'FITS (*.fits *.fit *.FITS *.FIT)'])
            if self.filename is not None:
                file_dialog.selectFile(self.filename)
            if self.fileformat == 'ascii':
                file_dialog.selectNameFilter('ASCII Files (*.*)')
            elif self.fileformat == 'ecsv':
                file_dialog.selectNameFilter('Enhanced CSV Files (*.ecsv)')
            elif self.fileformat == 'fits':
                file_dialog.selectNameFilter('FITS (*.fits *.fit *.FITS *.FIT)')
            if self.inverse is not None:
                file_dialog.check_box.setChecked(self.inverse)

            if file_dialog.exec_() == QtWidgets.QDialog.Accepted:
                
                isAccepted = True

                # ``filename``
                self.filename = file_dialog.selectedUrls()[0].toLocalFile()
                # ``fileformat``
                extension = os.path.splitext(self.filename)[1]
                if file_dialog.selectedNameFilter().startswith('Enhanced'):
                    self.fileformat = 'ecsv'
                elif file_dialog.selectedNameFilter().startswith('FITS'):
                    self.fileformat = 'fits'
                else:
                    self.fileformat = 'ascii'
                # ``inverse``
                self.inverse = file_dialog.check_box.checkState() == QtCore.Qt.Checked

        if external | isAccepted:
            # try:
            self.index, self.count = loadSpectrum(self.filename, self.fileformat, self.inverse)
            # except:
            self.peak_lib = dict()

            # Plot
            self.plotSpectrum()
            if self.isNewOpen:
                # Enable group box `peak`
                self.setEnabled(group_box='peak', enable=True)
                # Set flag `isNewOpen`
                self.isNewOpen = False
            else:
                # Initialize the table
                self.TableWidget_line.setRowCount(0)
                # Clear group box `fit`
                self.clearFitting()

    def save(self):
        """
        """

        file_dialog = CheckBoxFileDialog(check_box_text='Enhanced CSV Files (*.ecsv)')
        file_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        file_dialog.setNameFilters(['FITS (*.fits *.fit *.FITS *.FIT)'])
        file_dialog.selectFile(os.path.splitext(self.filename)[0])
        if file_dialog.exec_() == QtWidgets.QDialog.Accepted:
            # ``filename``
            filename = file_dialog.selectedUrls()[0].toLocalFile()
            extension = os.path.splitext(filename)[1]
            if extension not in ['.fits', '.fit', '.FITS', '.FIT']:
                filename += '.fits'
            # also save as Enhanced CSV Files (*.ecsv) or not
            saveECSV = file_dialog.check_box.checkState() == QtCore.Qt.Checked

            saveSpectrum(spectrum=self.spectrum, 
                         peak_prop=self.peak_prop, 
                         header=self.header, 
                         filename=filename, 
                         saveECSV=saveECSV)
            
            self.statusBar.showMessage(f'Saved to {filename} successfully.', 2000)

    def about(self):
        text = 'Wavelength Calibrator (ver 0.0.2)\n' +\
               'Developed by Ruining ZHAO\n' +\
               '12/22/2021\n' +\
               '1) Bugs to be fixed.\n' +\
               '2) Exceptions to be caught.'
        about_message_box = QtWidgets.QMessageBox()
        about_message_box.setIcon(QtWidgets.QMessageBox.Information)
        about_message_box.setText(text)
        # about_message_box.setInformativeText('More information')
        about_message_box.setWindowTitle('About')
        about_message_box.exec_()

    def find(self):
        """
        self.peaks
        self.properties
        """
    
        nrow_old = self.TableWidget_line.rowCount()
        # Get old contents
        if nrow_old > 0:
            for i in range(nrow_old):
                self.peak_lib[int(self.peaks[i])] = (
                    self.TableWidget_line.item(i, 0).text(),
                    self.TableWidget_line.cellWidget(i, 1).checkState()
                )

        # Get peak parameters
        height = float(self.LineEdit_height.text())
        threshold = float(self.LineEdit_threshold.text())
        distance = float(self.LineEdit_distance.text())
        prominence = float(self.LineEdit_prominence.text())
        width = float(self.LineEdit_width.text())
        wlen = float(self.LineEdit_wlen.text())
        rel = float(self.LineEdit_rel.text())
        plateau = float(self.LineEdit_plateau.text())

        # Find peaks
        self.peaks, self.properties = findPeaks(x=self.count, 
                                                height=height, 
                                                threshold=threshold, 
                                                distance=distance, 
                                                prominence=prominence, 
                                                width=width, 
                                                wlen=wlen, 
                                                rel_height=rel, 
                                                plateau_size=plateau)

        self.TableWidget_line.setRowCount(len(self.peaks))
        peak_lib_keys = self.peak_lib.keys()
        for i, peak in enumerate(self.peaks):
            if int(peak) in peak_lib_keys:
                text, isChecked = self.peak_lib[int(peak)]
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
            self.TableWidget_line.verticalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        
        nrow_new = self.TableWidget_line.rowCount()
        if nrow_new > 0:
            self.setEnabled(group_box='fit', enable=True)
        else:
            self.clearFitting()

        # Plot
        self.Figure_spectrum.clear()
        ax = self.Figure_spectrum.add_subplot(111)
        trans = transforms.blended_transform_factory(
            ax.transData, ax.transAxes)
        ax.step(self.index, self.count, 'k-', lw=0.8, where='mid')
        for i, peak in enumerate(self.peaks):
            ax.plot([peak, peak], [0.0, 0.87], 'r--', transform=trans, lw=0.8)
            ax.plot([peak, peak], [0.94, 1.0], 'r--', transform=trans, lw=0.8)
            ax.annotate(f'{i + 1:d}', 
                        xy=(peak, 0.9), 
                        xycoords=trans, 
                        ha='center', 
                        va='center', 
                        fontsize=12, 
                        color='r',
                        annotation_clip=True)
        ax.tick_params(which='major', direction='in', top=True, right=True, length=5, width=1, labelsize=12)
        ax.tick_params(which='minor', direction='in', top=True, right=True, length=3, width=1, labelsize=12)
        ax.set_xlim(self.index.min(), self.index.max())
        ax.set_ylim(-0.05, 1.15)
        ax.set_xlabel('Pixel Index', fontsize=12)
        ax.set_ylabel('Normalized Count', fontsize=12)
        self.Figure_spectrum.tight_layout(pad=0.2)
        self.FigureCanvas_spectrum.draw()

    def clearFitting(self):
        """
        """
        
        # Clear plot
        if hasattr(self, 'ax_fit'):
            del self.ax_fit
        self.Figure_fit.clear()
        self.FigureCanvas_fit.draw()

        # Disable group box `Fit`
        self.setEnabled(group_box='fit', enable=False)

        # Disable Button `Save`
        self.save_action.setEnabled(False)

    def fitting(self):
        """
        self.wave
        self.mask
        self.wave_peaks
        self.wave_index
        self.residual
        self.rms
        self.spectrum
        self.peak_prop
        """

        # Get fit parameters
        self.npieces = int(self.LineEdit_npieces.text())
        if not hasattr(self, 'show_residual'):
            self.show_residual = self.RectSwitch.isChecked()
        
        # Get labelled lines
        nrow = self.TableWidget_line.rowCount()
        self.wave_input = np.zeros(nrow)
        self.mask_input = np.zeros(nrow, dtype=bool)
        for i in range(nrow):
            try:
                w = float(self.TableWidget_line.item(i, 0).text())
                m = bool(self.TableWidget_line.cellWidget(i, 1).checkState())
            except:
                w = np.nan
                m = True
            self.wave_input[i] = w
            self.mask_input[i] = m

        # Fit with cubic spline function
        spl = fitCubicSpline(x=self.peaks, 
                             y=self.wave_input, 
                             mask=self.mask_input, 
                             npieces=self.npieces)
        self.wave_peaks = spl(self.peaks)
        self.wave_index = spl(self.index)
        self.residual = self.wave_input[~self.mask_input] - self.wave_peaks[~self.mask_input]
        self.rms = np.sqrt((self.residual**2).sum() / (~self.mask_input).sum())

        # Plot
        self.plotFitting()
        
        # Compile
        self.header = {
            'NPEAKU': ((~self.mask_input).sum(), 'Number of peaks used'),
            'NPEAKD': (self.wave_input.shape[0], 'Number of peaks detected'),
            'NPIECES': (self.npieces, 'Number of spline3 pieces'),
            'RMS': (round(self.rms, 3), 'Root mean squared of fitting'),
        }
        self.spectrum = Table(data=np.vstack([self.wave_index, self.count]).T, 
                              names=('wavelength', 'normalized count'))
        self.peak_prop = Table(data=np.vstack([self.peaks[~self.mask_input],
                                               self.properties['peak_heights'][~self.mask_input], 
                                               self.properties['left_bases'][~self.mask_input], 
                                               self.properties['right_bases'][~self.mask_input], 
                                               self.wave_input[~self.mask_input]]).T, 
                               names=('peaks', 'peak_heights', 'left_bases', 'right_bases', 'wavelength'))

        # Enable Button `Save`
        self.save_action.setEnabled(True)

    def plotFitting(self):

        self.Figure_fit.clear()
        self.ax_fit = self.Figure_fit.add_subplot(111)
        if not self.show_residual:
            self.ax_fit.plot(self.wave_input[self.mask_input], self.peaks[self.mask_input], 'x', c='grey', ms=8)
            self.ax_fit.plot(self.wave_input[~self.mask_input], self.peaks[~self.mask_input], 'x', c='red', ms=8)
            self.ax_fit.plot(self.wave_index, self.index, 'k-', lw=0.8)
            self.ax_fit.set_ylabel('Pixel Index', fontsize=12)
        else:
            self.ax_fit.plot(self.wave_peaks[~self.mask_input], self.residual, 'x', c='red', ms=8)
            self.ax_fit.axhline(y=0, ls='--', color='k', lw=0.8)
            for i, peak in enumerate(self.peaks):
                if self.mask_input[i]:
                    self.ax_fit.annotate(f'{i + 1:d}', (self.wave_peaks[i], 0), xycoords='data', ha='center', va='center', fontsize=12, color='grey')
                else:
                    self.ax_fit.annotate(f'{i + 1:d}', (self.wave_peaks[i], 0), xycoords='data', ha='center', va='center', fontsize=12, color='r')
            self.ax_fit.set_ylabel('Residuals', fontsize=12)
        self.ax_fit.tick_params(which='major', direction='in', top=True, right=True, length=5, width=1.5, labelsize=12)
        self.ax_fit.tick_params(which='minor', direction='in', top=True, right=True, length=3, width=1.5, labelsize=12)
        self.ax_fit.set_xlim(self.wave_index.min(), self.wave_index.max())
        self.ax_fit.set_xlabel('Wavelength', fontsize=12)
        self.ax_fit.annotate('$N=' + f'{(~self.mask_input).sum()}/{self.wave_input.shape[0]}$, ' + '$\\rm{RMS}=' + f'{self.rms:.3f}$',
                             xy=(0.98, 0.1), 
                             xycoords='axes fraction',
                             ha='right',
                             fontsize=12)
        self.Figure_fit.tight_layout(pad=0.2, h_pad=0)
        self.FigureCanvas_fit.draw()

    def switchPlot(self):
        self.show_residual = self.RectSwitch.isChecked()
        if hasattr(self, 'ax_fit'):
            self.plotFitting()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', 
                        default=None, 
                        help='Name of the input file')
    parser.add_argument('-f', '--format', 
                        default=None, 
                        help='Format of the input file (`ascii`, `ecsv`, or `fits`).')
    parser.add_argument('-i', '--inverse', 
                        action='store_true', 
                        default=False, 
                        help='Inverse or not')

    # UI
    app = QtWidgets.QApplication([])
    app.setStyle('Windows')
    # Setup
    main_window = MainWindow()
    # Show
    main_window.show()

    # Assignment
    args = parser.parse_args()
    main_window.filename = args.name
    main_window.fileformat = args.format
    main_window.inverse = args.inverse

    # warnings.filterwarnings('error')

    # Load spectrum if ``name`` and ``format`` is provided
    if main_window.filename is not None:
        main_window.filename = os.path.abspath(main_window.filename)
        if main_window.fileformat is not None:
            main_window.load(external=True)

    sys.exit(app.exec_())
    
    # from astropy.io import fits

    # hdulist = fits.open('aaass.fits')

    # print(hdulist[1].header)