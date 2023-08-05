# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wavecal.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!
#
# 11/06/2021: RNZ added a menu bar and a link to `~scipy.signal.find_peak`
# 07/20/2023: RNZ added line list and polynomial fitting.
#             RNZ replaced the RectSwitch with a toggle button.
#             RNZ optimized the structure of the code.


# PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
# matplotlib
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt

from .fonts import labelFont, tableFont, buttonFont
from .widgets import TableItemCompleter, FormLayout

# Deprecated in 0.0.2.0 (RNZ 07/20/2023)
# # switch
# from .widgets import RectSwitch

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        # ===========
        # MAIN WINDOW
        # ===========

        # Window-resizing (RNZ 07/20/2023):
        #   Window-resizing is handled by the OS's window manager, not QT. The size 
        #   policy works only in layouts. Setting any size policy for a window is 
        #   useless.
        # sizePolicy = QtWidgets.QSizePolicy(
        #     QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        # sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())

        # Main window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setMinimumSize(QtCore.QSize(1200, 800))

        # Menu bar (RNZ 11/06/2021)
        self.menuBar = MainWindow.menuBar()
        self.menuBar.setObjectName("menuBar")
        self.menuBar.setNativeMenuBar(False)

        self.fileMenu = self.menuBar.addMenu("&File")
        self.openAction = QtWidgets.QAction("Open File...", MainWindow)
        self.openAction.setObjectName("open")
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.setIcon(
            self.style().standardIcon(QtWidgets.QStyle.SP_DialogOpenButton))
        self.saveAction = QtWidgets.QAction("Save As...", MainWindow)
        self.saveAction.setObjectName("save")
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.setIcon(
            self.style().standardIcon(QtWidgets.QStyle.SP_DialogSaveButton))
        self.savePeakAction = QtWidgets.QAction("Save Peak Info...", MainWindow)
        self.savePeakAction.setObjectName("savePeak")
        self.savePeakAction.setIcon(
            self.style().standardIcon(QtWidgets.QStyle.SP_DialogSaveButton))
        self.exitAction = QtWidgets.QAction("Exit", MainWindow)
        self.exitAction.setShortcut("Ctrl+Q")
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addAction(self.savePeakAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAction)

        self.helpMenu = self.menuBar.addMenu("&Help")
        self.aboutAction = QtWidgets.QAction("About", MainWindow)
        self.aboutAction.setObjectName("about")
        self.aboutAction.setIcon(
            self.style().standardIcon(QtWidgets.QStyle.SP_MessageBoxInformation))
        self.helpMenu.addAction(self.aboutAction)

        # Central widget
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")

        # Grid layout
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setObjectName("gridLayout")

        # Add to main window
        MainWindow.setCentralWidget(self.centralWidget)

        # Status bar
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        # Add to main window
        MainWindow.setStatusBar(self.statusBar)

        # ==============
        # IN GRID LAYOUT
        # ==============

        # Size policy for group box `peak` and `disp`
        sizePolicy_twoGroupBoxes = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        # Stretch (RNZ 7/20/2023):
        #   When two widgets are adjacent to each other in a horizontal layout, setting 
        #   the horizontal stretch factor of the widget on the left to 2 and the factor 
        #   of widget on the right to 1 will ensure that the widget on the left will 
        #   always be twice the size of the one on the right. The default value is 0.
        sizePolicy_twoGroupBoxes.setHorizontalStretch(0)
        sizePolicy_twoGroupBoxes.setVerticalStretch(1)

        # Minimum size for group box `peak` and `disp`
        minimumSize_twoGroupBoxes = QtCore.QSize(100, 276)

        # Group box `peak`
        self.groupBox_peak = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox_peak.setObjectName("groupBox_peak")
        self.groupBox_peak.setSizePolicy(sizePolicy_twoGroupBoxes)
        self.groupBox_peak.setMinimumSize(minimumSize_twoGroupBoxes)
        self.groupBox_peak.setFont(labelFont)
        # Add to the grid layout
        self.gridLayout.addWidget(self.groupBox_peak, 0, 0, 1, 1)

        # Group box `disp`
        self.groupBox_disp = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox_disp.setObjectName("groupBox_disp")
        self.groupBox_disp.setSizePolicy(sizePolicy_twoGroupBoxes)
        self.groupBox_disp.setMinimumSize(minimumSize_twoGroupBoxes)
        self.groupBox_disp.setFont(labelFont)
        # Add to the grid layout
        self.gridLayout.addWidget(self.groupBox_disp, 1, 0, 1, 1)

        # Size policy for group box `line`
        sizePolicy_groupBoxLine = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy_groupBoxLine.setHorizontalStretch(0)
        sizePolicy_groupBoxLine.setVerticalStretch(0)

        # Group box `line`
        self.groupBox_line = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox_line.setObjectName("groupBox_line")
        self.groupBox_line.setSizePolicy(sizePolicy_groupBoxLine)
        self.groupBox_line.setMinimumSize(QtCore.QSize(215, 700))
        self.groupBox_line.setFont(labelFont)
        # Add to the grid layout
        self.gridLayout.addWidget(self.groupBox_line, 0, 1, 2, 1)

        # =================
        # IN GROUP BOX PEAK
        # =================

        # Horizontal layout `peak`
        self.horizontalLayout_peak = QtWidgets.QHBoxLayout(self.groupBox_peak)
        self.horizontalLayout_peak.setObjectName("horizontalLayout_peak")

        # Vertical layout `spec`
        self.verticalLayout_spec = QtWidgets.QVBoxLayout()
        self.verticalLayout_spec.setObjectName("verticalLayout_spec")
        # Add to horizontal layout `peak`
        self.horizontalLayout_peak.addLayout(self.verticalLayout_spec)

        # Vertical layout `peak`
        self.verticalLayout_peak = QtWidgets.QVBoxLayout()
        self.verticalLayout_peak.setObjectName("verticalLayout_peak")
        self.verticalLayout_peak.setContentsMargins(5, -1, 5, -1)
        self.verticalLayout_peak.setSpacing(5)
        # Add to horizontal layout `peak`
        self.horizontalLayout_peak.addLayout(self.verticalLayout_peak)

        # Set stretch
        self.horizontalLayout_peak.setStretch(0, 1)

        # =================
        # IN GROUP BOX DISP
        # =================

        # Horizontal layout `disp`
        self.horizontalLayout_disp = QtWidgets.QHBoxLayout(self.groupBox_disp)
        self.horizontalLayout_disp.setObjectName("horizontalLayout_disp")

        # Vertical layout `fit`
        self.verticalLayout_fit = QtWidgets.QVBoxLayout()
        self.verticalLayout_fit.setObjectName("verticalLayout_fit")
        # Add to horizontal layout `disp`
        self.horizontalLayout_disp.addLayout(self.verticalLayout_fit)

        # Vertical layout `disp`
        self.verticalLayout_disp = QtWidgets.QVBoxLayout()
        self.verticalLayout_disp.setObjectName("verticalLayout_disp")
        self.verticalLayout_disp.setContentsMargins(5, -1, 5, -1)
        self.verticalLayout_disp.setSpacing(5)
        # Add to horizontal layout `disp`
        self.horizontalLayout_disp.addLayout(self.verticalLayout_disp)

        # Set stretch
        self.horizontalLayout_disp.setStretch(0, 1)

        # =================
        # IN GROUP BOX LINE
        # =================

        # Vertical layout `line`
        self.verticalLayout_line = QtWidgets.QVBoxLayout(self.groupBox_line)
        self.verticalLayout_line.setObjectName("verticalLayout_line")
        self.verticalLayout_line.setContentsMargins(5, -1, 5, -1)
        self.verticalLayout_line.setSpacing(5)

        # =================
        # CANVAS SPEC & FIT
        # =================

        # Size policy for canvas `spec` and `fit`
        sizePolicy_canvas = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        
        # Size policy for tool bar `spec` and `fit`
        sizePolicy_toolBar = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)

        # Minimum size for canvases and tool bars
        minimumSize_canvas = QtCore.QSize(100, 276)
        minimumSize_toolBar = QtCore.QSize(100, 30)

        # Canvas `spec`
        self.figure_spec = plt.figure()
        self.figureCanvas_spec = FigureCanvas(self.figure_spec)
        self.figureCanvas_spec.setObjectName("figureCanvas_spec")
        self.figureCanvas_spec.setSizePolicy(sizePolicy_canvas)
        self.figureCanvas_spec.setMinimumSize(minimumSize_canvas)
        
        # Tool bar `spec`
        self.toolBar_spec = NavigationToolbar(self.figureCanvas_spec, MainWindow)
        self.toolBar_spec.setObjectName("toolBar_spec")
        self.toolBar_spec.setSizePolicy(sizePolicy_toolBar)
        self.toolBar_spec.setMinimumSize(minimumSize_toolBar)
        
        # Add to vertical layout `spec`
        self.verticalLayout_spec.addWidget(self.toolBar_spec)
        self.verticalLayout_spec.addWidget(self.figureCanvas_spec)

        # Canvas `fit`
        self.figure_fit = plt.figure()
        self.figureCanvas_fit = FigureCanvas(self.figure_fit)
        self.figureCanvas_fit.setObjectName("figureCanvas_fit")
        self.figureCanvas_fit.setSizePolicy(sizePolicy_canvas)
        self.figureCanvas_fit.setMinimumSize(minimumSize_canvas)

        # Tool bar `fit`
        self.toolBar_fit = NavigationToolbar(self.figureCanvas_fit, MainWindow)
        self.toolBar_fit.setObjectName("toolBar_fit")
        self.toolBar_fit.setSizePolicy(sizePolicy_toolBar)
        self.toolBar_fit.setMinimumSize(minimumSize_toolBar)
        
        # Add to Vertical layout `fit`
        self.verticalLayout_fit.addWidget(self.toolBar_fit)
        self.verticalLayout_fit.addWidget(self.figureCanvas_fit)

        # =======================
        # IN VERTICAL LAYOUT PEAK
        # =======================

        # Label `peak`
        self.label_peak = QtWidgets.QLabel(self.groupBox_peak)
        self.label_peak.setObjectName("label_peak")
        self.label_peak.setMinimumSize(QtCore.QSize(180, 25))
        self.label_peak.setMaximumSize(QtCore.QSize(180, 25))
        self.label_peak.setFont(labelFont)
        # Add to vertical layout `peak`
        self.verticalLayout_peak.addWidget(self.label_peak)

        # Line `peak`
        self.line_peak = QtWidgets.QFrame(self.groupBox_peak)
        self.line_peak.setObjectName("line_peak")
        self.line_peak.setMinimumSize(QtCore.QSize(180, 0))
        self.line_peak.setMaximumSize(QtCore.QSize(180, 16777215))
        self.line_peak.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_peak.setFrameShadow(QtWidgets.QFrame.Sunken)
        # Add to vertical layout `peak`
        self.verticalLayout_peak.addWidget(self.line_peak)

        # Form layout `peak`
        self.formLayout_peak = FormLayout(object_name="formLayout_peak")
        # Add to vertical layout `peak`
        self.verticalLayout_peak.addLayout(self.formLayout_peak)
        
        # Button `Find`
        self.button_find = QtWidgets.QPushButton(self.groupBox_peak)
        self.button_find.setObjectName("find")
        self.button_find.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button_find.setMinimumSize(QtCore.QSize(180, 22))
        self.button_find.setMaximumSize(QtCore.QSize(180, 22))
        self.button_find.setFont(buttonFont)
        # Add to vertical layout `peak`
        self.verticalLayout_peak.addWidget(self.button_find)

        # Stretch (RNZ 7/20/2023):
        #   All widgets are fixed in vertical size except the form layout. There is no 
        #   need to set stretch here.
        # self.verticalLayout_peak.setStretch(2, 1)

        # =======================
        # IN VERTICAL LAYOUT DISP
        # =======================

        # Label `disp`
        self.label_disp = QtWidgets.QLabel(self.groupBox_disp)
        self.label_disp.setObjectName("label_disp")
        self.label_disp.setMinimumSize(QtCore.QSize(180, 25))
        self.label_disp.setMaximumSize(QtCore.QSize(180, 25))
        self.label_disp.setFont(labelFont)
        # Add to vertical layout `disp`
        self.verticalLayout_disp.addWidget(self.label_disp)
        
        # Line `disp`
        self.line_disp = QtWidgets.QFrame(self.groupBox_disp)
        self.line_disp.setObjectName("line_disp")
        self.line_disp.setMinimumSize(QtCore.QSize(180, 0))
        self.line_disp.setMaximumSize(QtCore.QSize(180, 16777215))
        self.line_disp.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_disp.setFrameShadow(QtWidgets.QFrame.Sunken)
        # Add to vertical layout `disp`
        self.verticalLayout_disp.addWidget(self.line_disp)

        # Tab widget
        self.tabWidget = QtWidgets.QTabWidget(self.groupBox_disp)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.tabBar().setDocumentMode(True)
        self.tabWidget.setFont(labelFont)
        # Add to vertical layout `disp`
        self.verticalLayout_disp.addWidget(self.tabWidget)

        # Form layout `sigma`
        self.formLayout_sigma = FormLayout(object_name="formLayout_sigma")
        # Add to vertical layout `disp`
        self.verticalLayout_disp.addLayout(self.formLayout_sigma)

        # Button `fit`
        self.button_fit = QtWidgets.QPushButton(self.groupBox_disp)
        self.button_fit.setObjectName("fit")
        self.button_fit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button_fit.setMinimumSize(QtCore.QSize(180, 22))
        self.button_fit.setMaximumSize(QtCore.QSize(180, 22))
        self.button_fit.setFont(buttonFont)
        # Add to vertical layout `disp`
        self.verticalLayout_disp.addWidget(self.button_fit)

        # Button `residual`
        self.button_residual = QtWidgets.QPushButton(self.groupBox_disp)
        self.button_residual.setObjectName("residual")
        self.button_residual.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button_residual.setCheckable(True)
        self.button_residual.setMinimumSize(QtCore.QSize(180, 22))
        self.button_residual.setMaximumSize(QtCore.QSize(180, 22))
        self.button_residual.setFont(buttonFont)
        # Add to vertical layout `disp`
        self.verticalLayout_disp.addWidget(self.button_residual)

        # Form layout `mask`
        self.formLayout_mask = FormLayout(object_name="formLayout_mask")
        # Add to vertical layout `disp`
        self.verticalLayout_disp.addLayout(self.formLayout_mask)

        # Stretch (RNZ 7/20/2023):
        #   All widgets are fixed in vertical size except the tab widget. There is no 
        #   need to set stretch here.
        # self.verticalLayout_disp.setStretch(2, 1)

        # ==========
        # TAB WIDGET
        # ==========

        # Tab `poly`
        self.tab_poly = QtWidgets.QWidget()
        self.tab_poly.setObjectName("poly")
        self.tabWidget.addTab(self.tab_poly, "Poly")

        # Form layout `poly`
        self.formLayout_poly = FormLayout(object_name="formLayout_poly")
        self.formLayout_poly.setContentsMargins(10, -1, 10, -1)
        # Add to tab `poly`
        self.tab_poly.setLayout(self.formLayout_poly)

        # Tab `spline3`
        self.tab_spline3 = QtWidgets.QWidget()
        self.tab_spline3.setObjectName("spline3")
        self.tabWidget.addTab(self.tab_spline3, "Spline3")
        
        # Form layout `spline3`
        self.formLayout_spline3 = FormLayout(object_name="formLayout_spline3")
        self.formLayout_spline3.setContentsMargins(10, -1, 10, -1)
        # Add to tab `spline3`
        self.tab_spline3.setLayout(self.formLayout_spline3)

        # =======================
        # IN VERTICAL LAYOUT LINE
        # =======================

        # Horizontal layout `line`
        self.horizontalLayout_line = QtWidgets.QHBoxLayout()
        self.horizontalLayout_line.setObjectName("horizontalLayout_line")
        self.horizontalLayout_line.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout_line.setSpacing(10)
        # Add to vertical layout `line`
        self.verticalLayout_line.addLayout(self.horizontalLayout_line)

        # Form layout `unit`
        self.formLayout_unit = FormLayout(object_name="formLayout_unit")
        # Add to vertical layout `line`
        self.verticalLayout_line.addLayout(self.formLayout_unit)

        # Table widget
        self.tableWidget = QtWidgets.QTableWidget(self.groupBox_line)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setMinimumSize(QtCore.QSize(200, 500))
        self.tableWidget.setMaximumSize(QtCore.QSize(200, 16777215))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        # Resize mode
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
        # Table header 0
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFont(tableFont)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        # Table header 1
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFont(tableFont)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        # Item delegate
        self.tableWidget.setItemDelegate(TableItemCompleter(self.tableWidget))
        # Add to vertical layout `line`
        self.verticalLayout_line.addWidget(self.tableWidget)

        # Form layout `tolerance`
        self.formLayout_tolerance = FormLayout(object_name="formLayout_tolerance")
        # Add to vertical layout `line`
        self.verticalLayout_line.addLayout(self.formLayout_tolerance)

        # Form layout `autoid`
        self.formLayout_autoid = FormLayout(object_name="formLayout_autoid")
        # Add to vertical layout `line`
        self.verticalLayout_line.addLayout(self.formLayout_autoid)

        # Stretch (RNZ 7/20/2023):
        #   All widgets are fixed in vertical size except the table widget. There is no 
        #   need to set stretch here.
        # self.verticalLayout_line.setStretch(3, 1)

        # ===================
        # IN FORM LAYOUT PEAK
        # ===================

        # Size for labels and line edits
        size_label = QtCore.QSize(97, 22)
        size_lineEdit = QtCore.QSize(73, 22)

        # (1, 1) Label `height`
        self.label_height = QtWidgets.QLabel(self.groupBox_peak)
        self.label_height.setObjectName("label_height")
        self.label_height.setMinimumSize(size_label)
        self.label_height.setMaximumSize(size_label)
        self.label_height.setFont(labelFont)
        # Add to form layout `peak`
        self.formLayout_peak.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.label_height)
        
        # (1, 2) Line edit `height`
        self.lineEdit_height = QtWidgets.QLineEdit(self.groupBox_peak)
        self.lineEdit_height.setObjectName("lineEdit_height")
        self.lineEdit_height.setMinimumSize(size_lineEdit)
        self.lineEdit_height.setMaximumSize(size_lineEdit)
        self.lineEdit_height.setFont(labelFont)
        # Add to form layout `peak`
        self.formLayout_peak.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_height)
        
        # (2, 1) Label `threshold`
        self.label_threshold = QtWidgets.QLabel(self.groupBox_peak)
        self.label_threshold.setObjectName("label_threshold")
        self.label_threshold.setMinimumSize(size_label)
        self.label_threshold.setMaximumSize(size_label)
        self.label_threshold.setFont(labelFont)
        # Add to form layout `peak`
        self.formLayout_peak.setWidget(
            1, QtWidgets.QFormLayout.LabelRole, self.label_threshold)
        
        # (2, 2) Line edit `threshold`
        self.lineEdit_threshold = QtWidgets.QLineEdit(self.groupBox_peak)
        self.lineEdit_threshold.setObjectName("lineEdit_threshold")
        self.lineEdit_threshold.setMinimumSize(size_lineEdit)
        self.lineEdit_threshold.setMaximumSize(size_lineEdit)
        self.lineEdit_threshold.setFont(labelFont)
        # Add to form layout `peak`
        self.formLayout_peak.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_threshold)
        
        # (3, 1) Label `distance`
        self.label_distance = QtWidgets.QLabel(self.groupBox_peak)
        self.label_distance.setObjectName("label_distance")
        self.label_distance.setMinimumSize(size_label)
        self.label_distance.setMaximumSize(size_label)
        self.label_distance.setFont(labelFont)
        # Add to form layout `peak`
        self.formLayout_peak.setWidget(
            2, QtWidgets.QFormLayout.LabelRole, self.label_distance)
        
        # (3, 2) Line edit `distance`
        self.lineEdit_distance = QtWidgets.QLineEdit(self.groupBox_peak)
        self.lineEdit_distance.setObjectName("lineEdit_distance")
        self.lineEdit_distance.setMinimumSize(size_lineEdit)
        self.lineEdit_distance.setMaximumSize(size_lineEdit)
        self.lineEdit_distance.setFont(labelFont)
        # Add to form layout `peak`
        self.formLayout_peak.setWidget(
            2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_distance)
        
        # (4, 1) Label `prominence`
        self.label_prominence = QtWidgets.QLabel(self.groupBox_peak)
        self.label_prominence.setObjectName("label_prominence")        
        self.label_prominence.setMinimumSize(size_label)
        self.label_prominence.setMaximumSize(size_label)
        self.label_prominence.setFont(labelFont)
        # Add to form layout `peak`
        self.formLayout_peak.setWidget(
            3, QtWidgets.QFormLayout.LabelRole, self.label_prominence)
        
        # (4, 2) Line edit `prominence`
        self.lineEdit_prominence = QtWidgets.QLineEdit(self.groupBox_peak)
        self.lineEdit_prominence.setObjectName("lineEdit_prominence")        
        self.lineEdit_prominence.setMinimumSize(size_lineEdit)
        self.lineEdit_prominence.setMaximumSize(size_lineEdit)
        self.lineEdit_prominence.setFont(labelFont)
        # Add to form layout `peak`
        self.formLayout_peak.setWidget(
            3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_prominence)
        
        # (5, 1) Label `width`
        self.label_width = QtWidgets.QLabel(self.groupBox_peak)
        self.label_width.setObjectName("label_width")
        self.label_width.setMinimumSize(size_label)
        self.label_width.setMaximumSize(size_label)
        self.label_width.setFont(labelFont)
        # Add to form layout `peak`
        self.formLayout_peak.setWidget(
            4, QtWidgets.QFormLayout.LabelRole, self.label_width)

        # (5, 2) Line edit `width`
        self.lineEdit_width = QtWidgets.QLineEdit(self.groupBox_peak)
        self.lineEdit_width.setObjectName("lineEdit_width")
        self.lineEdit_width.setMinimumSize(size_lineEdit)
        self.lineEdit_width.setMaximumSize(size_lineEdit)
        self.lineEdit_width.setFont(labelFont)
        # Add to form layout `peak`
        self.formLayout_peak.setWidget(
            4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_width)
        
        # (6, 1) Label `wlen`
        self.label_wlen = QtWidgets.QLabel(self.groupBox_peak)
        self.label_wlen.setObjectName("label_wlen")
        self.label_wlen.setMinimumSize(size_label)
        self.label_wlen.setMaximumSize(size_label)
        self.label_wlen.setFont(labelFont)
        # Add to form layout `peak`
        self.formLayout_peak.setWidget(
            5, QtWidgets.QFormLayout.LabelRole, self.label_wlen)
        
        # (6, 2) Line edit `wlen`
        self.lineEdit_wlen = QtWidgets.QLineEdit(self.groupBox_peak)
        self.lineEdit_wlen.setObjectName("lineEdit_wlen")
        self.lineEdit_wlen.setMinimumSize(size_lineEdit)
        self.lineEdit_wlen.setMaximumSize(size_lineEdit)
        self.lineEdit_wlen.setFont(labelFont)
        # Add to form layout `peak`
        self.formLayout_peak.setWidget(
            5, QtWidgets.QFormLayout.FieldRole, self.lineEdit_wlen)
        
        # (7, 1) Label `rel`
        self.label_rel = QtWidgets.QLabel(self.groupBox_peak)
        self.label_rel.setObjectName("label_rel")
        self.label_rel.setMinimumSize(size_label)
        self.label_rel.setMaximumSize(size_label)
        self.label_rel.setFont(labelFont)
        # Add to form layout `peak`
        self.formLayout_peak.setWidget(
            6, QtWidgets.QFormLayout.LabelRole, self.label_rel)
        
        # (7, 2) Line edit `rel`
        self.lineEdit_rel = QtWidgets.QLineEdit(self.groupBox_peak)
        self.lineEdit_rel.setObjectName("lineEdit_rel")
        self.lineEdit_rel.setMinimumSize(size_lineEdit)
        self.lineEdit_rel.setMaximumSize(size_lineEdit)
        self.lineEdit_rel.setFont(labelFont)
        # Add to form layout `peak`
        self.formLayout_peak.setWidget(
            6, QtWidgets.QFormLayout.FieldRole, self.lineEdit_rel)
        
        # (8, 1) Label `plateau`
        self.label_plateau = QtWidgets.QLabel(self.groupBox_peak)
        self.label_plateau.setObjectName("label_plateau")
        self.label_plateau.setMinimumSize(size_label)
        self.label_plateau.setMaximumSize(size_label)
        self.label_plateau.setFont(labelFont)
        # Add to form layout `peak`
        self.formLayout_peak.setWidget(
            7, QtWidgets.QFormLayout.LabelRole, self.label_plateau)
        
        # (8, 2) Line edit `plateau`
        self.lineEdit_plateau = QtWidgets.QLineEdit(self.groupBox_peak)
        self.lineEdit_plateau.setObjectName("lineEdit_plateau")
        self.lineEdit_plateau.setMinimumSize(size_lineEdit)
        self.lineEdit_plateau.setMaximumSize(size_lineEdit)
        self.lineEdit_plateau.setFont(labelFont)
        # Add to form layout `peak`
        self.formLayout_peak.setWidget(
            7, QtWidgets.QFormLayout.FieldRole, self.lineEdit_plateau)
        
        # (9, 1) Label `help` (RNZ 11/06/2021)
        self.label_help = QtWidgets.QLabel(self.groupBox_peak)
        self.label_help.setObjectName("label_help")
        self.label_help.setMinimumSize(size_label)
        self.label_help.setMaximumSize(size_label)
        self.label_help.setFont(labelFont)
        # Add to form layout `peak`
        self.formLayout_peak.setWidget(
            8, QtWidgets.QFormLayout.LabelRole, self.label_help)

        # ===================
        # IN FORM LAYOUT POLY
        # ===================
        
        # Label `degree`
        self.label_degree = QtWidgets.QLabel(self.groupBox_disp)
        self.label_degree.setObjectName("label_degree")
        self.label_degree.setMinimumSize(QtCore.QSize(87, 22))
        self.label_degree.setMaximumSize(QtCore.QSize(87, 22))
        self.label_degree.setFont(labelFont)
        # Add to form layout `poly`
        self.formLayout_poly.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.label_degree)
        
        # Line edit `degree`
        self.lineEdit_degree = QtWidgets.QLineEdit(self.groupBox_disp)
        self.lineEdit_degree.setObjectName("lineEdit_degree")
        self.lineEdit_degree.setMinimumSize(QtCore.QSize(63, 22))
        self.lineEdit_degree.setMaximumSize(QtCore.QSize(63, 22))
        self.lineEdit_degree.setFont(labelFont)
        # Add to form layout `poly`
        self.formLayout_poly.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_degree)

        # ======================
        # IN FORM LAYOUT SPLINE3
        # ======================

        # Label `npieces`
        self.label_npieces = QtWidgets.QLabel(self.groupBox_disp)
        self.label_npieces.setObjectName("label_npieces")
        self.label_npieces.setMinimumSize(QtCore.QSize(87, 22))
        self.label_npieces.setMaximumSize(QtCore.QSize(87, 22))
        self.label_npieces.setFont(labelFont)
        # Add to form layout `spline3`
        self.formLayout_spline3.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.label_npieces)
        
        # Line edit `npieces`
        self.lineEdit_npieces = QtWidgets.QLineEdit(self.groupBox_disp)
        self.lineEdit_npieces.setObjectName("lineEdit_npieces")
        self.lineEdit_npieces.setMinimumSize(QtCore.QSize(63, 22))
        self.lineEdit_npieces.setMaximumSize(QtCore.QSize(63, 22))
        self.lineEdit_npieces.setFont(labelFont)
        # Add to form layout `spline3`
        self.formLayout_spline3.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_npieces)

        # ====================
        # IN FORM LAYOUT SIGMA
        # ====================

        # (1, 1) Label `maxiters`
        self.label_maxiters = QtWidgets.QLabel(self.groupBox_disp)
        self.label_maxiters.setObjectName("label_maxiter")
        self.label_maxiters.setMinimumSize(size_label)
        self.label_maxiters.setMaximumSize(size_label)
        self.label_maxiters.setFont(labelFont)
        # Add to form layout `sigma`
        self.formLayout_sigma.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.label_maxiters)
        
        # (1, 2) Line edit `maxiters`
        self.lineEdit_maxiters = QtWidgets.QLineEdit(self.groupBox_disp)
        self.lineEdit_maxiters.setObjectName("lineEdit_maxiter")
        self.lineEdit_maxiters.setMinimumSize(size_lineEdit)
        self.lineEdit_maxiters.setMaximumSize(size_lineEdit)
        self.lineEdit_maxiters.setFont(labelFont)
        # Add to form layout `sigma`
        self.formLayout_sigma.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_maxiters)

        # (2, 1) Label `sigma_lower`
        self.label_sigma_lower = QtWidgets.QLabel(self.groupBox_disp)
        self.label_sigma_lower.setObjectName("label_sigma_lower")        
        self.label_sigma_lower.setMinimumSize(size_label)
        self.label_sigma_lower.setMaximumSize(size_label)
        self.label_sigma_lower.setFont(labelFont)
        # Add to form layout `sigma`
        self.formLayout_sigma.setWidget(
            1, QtWidgets.QFormLayout.LabelRole, self.label_sigma_lower)
        
        # (2, 2) Line edit `sigma_lower`
        self.lineEdit_sigma_lower = QtWidgets.QLineEdit(self.groupBox_disp)
        self.lineEdit_sigma_lower.setObjectName("lineEdit_sigma_lower")
        self.lineEdit_sigma_lower.setMinimumSize(size_lineEdit)
        self.lineEdit_sigma_lower.setMaximumSize(size_lineEdit)
        self.lineEdit_sigma_lower.setFont(labelFont)
        # Add to form layout `sigma`
        self.formLayout_sigma.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_sigma_lower)

        # (3, 1) Label `sigma_upper`
        self.label_sigma_upper = QtWidgets.QLabel(self.groupBox_disp)
        self.label_sigma_upper.setObjectName("label_sigma_upper")
        self.label_sigma_upper.setMinimumSize(size_label)
        self.label_sigma_upper.setMaximumSize(size_label)
        self.label_sigma_upper.setFont(labelFont)
        # Add to form layout `sigma`
        self.formLayout_sigma.setWidget(
            2, QtWidgets.QFormLayout.LabelRole, self.label_sigma_upper)

        # (3, 2) Line edit `sigma_upper`
        self.lineEdit_sigma_upper = QtWidgets.QLineEdit(self.groupBox_disp)
        self.lineEdit_sigma_upper.setObjectName("lineEdit_sigma_upper")
        self.lineEdit_sigma_upper.setMinimumSize(size_lineEdit)
        self.lineEdit_sigma_upper.setMaximumSize(size_lineEdit)
        self.lineEdit_sigma_upper.setFont(labelFont)
        # Add to form layout `sigma`
        self.formLayout_sigma.setWidget(
            2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_sigma_upper)
        
        # # (4, 1) Label `switch`
        # self.label_switch = QtWidgets.QLabel(self.groupBox_disp)
        # self.label_switch.setObjectName("label_switch")
        # self.label_switch.setMinimumSize(QtCore.QSize(90, 22))
        # self.label_switch.setMaximumSize(QtCore.QSize(90, 22))
        # self.label_switch.setFont(labelFont)
        # # Add to form layout `sigma`
        # self.formLayout_sigma.setWidget(
        #     4, QtWidgets.QFormLayout.LabelRole, self.label_switch)
        
        # # (4, 2) Switch
        # self.RectSwitch = RectSwitch(
        #     self.groupBox_disp, margin=-9, thumb_width=0.4, duration=150)
        # self.RectSwitch.setObjectName("RectSwitch")
        # self.RectSwitch.setMinimumSize(QtCore.QSize(73, 22))
        # self.RectSwitch.setMaximumSize(QtCore.QSize(73, 22))
        # # Add to form layout `sigma`
        # self.formLayout_sigma.setWidget(
        #     1, QtWidgets.QFormLayout.FieldRole, self.RectSwitch)

        # ===================
        # IN FORM LAYOUT MASK
        # ===================

        # (1, 1) Button `mask`
        self.button_mask = QtWidgets.QPushButton(self.groupBox_line)
        self.button_mask.setObjectName("mask")
        self.button_mask.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button_mask.setMinimumSize(size_label)
        self.button_mask.setMaximumSize(size_label)
        self.button_mask.setFont(buttonFont)
        # Add to form layout `mask`
        self.formLayout_mask.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.button_mask)

        # (1, 2) Button `unmask`
        self.button_unmask = QtWidgets.QPushButton(self.groupBox_line)
        self.button_unmask.setObjectName("unmask")
        self.button_unmask.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button_unmask.setMinimumSize(size_lineEdit)
        self.button_unmask.setMaximumSize(size_lineEdit)
        self.button_unmask.setIcon(QtGui.QIcon.fromTheme("edit-undo"))
        self.button_unmask.setFont(buttonFont)
        # Add to form layout `unmask`
        self.formLayout_mask.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.button_unmask)

        # =========================
        # IN HORIZONTAL LAYOUT LINE
        # =========================

        # Button `load`
        self.button_load = QtWidgets.QPushButton(self.groupBox_line)
        self.button_load.setObjectName("load")
        self.button_load.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button_load.setMinimumSize(QtCore.QSize(20, 22))
        self.button_load.setMaximumSize(QtCore.QSize(20, 22))
        self.button_load.setIcon(
            self.style().standardIcon(QtWidgets.QStyle.SP_DirOpenIcon))
        self.button_load.setStyleSheet("border: none")
        # Add to horizontal layout `load`
        self.horizontalLayout_line.addWidget(self.button_load, QtCore.Qt.AlignLeft)

        # Button `unload`
        self.button_unload = QtWidgets.QPushButton(self.groupBox_line)
        self.button_unload.setObjectName("unload")
        self.button_unload.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button_unload.setMinimumSize(QtCore.QSize(20, 22))
        self.button_unload.setMaximumSize(QtCore.QSize(20, 22))
        self.button_unload.setIcon(
            self.style().standardIcon(QtWidgets.QStyle.SP_TrashIcon))
        self.button_unload.setStyleSheet("border: none")
        # Add to horizontal layout `load`
        self.horizontalLayout_line.addWidget(self.button_unload, QtCore.Qt.AlignLeft)

        # Line edit `lineList`
        self.lineEdit_lineList = QtWidgets.QLineEdit(self.groupBox_line)
        self.lineEdit_lineList.setObjectName("lineEdit_lineList")
        self.lineEdit_lineList.setReadOnly(True)
        self.lineEdit_lineList.setStyleSheet("background-color: palette(window);")
        self.lineEdit_lineList.setMinimumSize(QtCore.QSize(140, 22))
        self.lineEdit_lineList.setMaximumSize(QtCore.QSize(140, 22))
        self.lineEdit_lineList.setFont(labelFont)
        # Add to horizontal layout `line`
        self.horizontalLayout_line.addWidget(
            self.lineEdit_lineList, QtCore.Qt.AlignLeft)

        # ===================
        # IN FORM LAYOUT UNIT
        # ===================

        # (1, 1) Label `unit`
        self.label_unit = QtWidgets.QLabel(self.groupBox_line)
        self.label_unit.setObjectName("label_unit")        
        self.label_unit.setMinimumSize(QtCore.QSize(104, 22))
        self.label_unit.setMaximumSize(QtCore.QSize(104, 22))
        self.label_unit.setFont(labelFont)
        # Add to form layout `unit`
        self.formLayout_unit.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.label_unit)
        
        # (1, 2) Combo box `unit`
        self.comboBox = QtWidgets.QComboBox(self.groupBox_line)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setMinimumSize(QtCore.QSize(86, 22))
        self.comboBox.setMaximumSize(QtCore.QSize(86, 22))
        self.comboBox.setFont(labelFont)
        self.comboBox.addItems(['Angstrom', 'nm', 'micron', 'mm', 'cm'])
        # Add to form layout `unit`
        self.formLayout_unit.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.comboBox)

        # ========================
        # IN FORM LAYOUT TOLERANCE
        # ========================

        # (1, 1) Label `tolerance`
        self.label_tolerance = QtWidgets.QLabel(self.groupBox_line)
        self.label_tolerance.setObjectName("label_tolerance")
        self.label_tolerance.setMinimumSize(QtCore.QSize(117, 22))
        self.label_tolerance.setMaximumSize(QtCore.QSize(117, 22))
        self.label_tolerance.setFont(labelFont)
        # Add to form layout `tolerance`
        self.formLayout_tolerance.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.label_tolerance)
        
        # (1, 2) Line edit `tolerance`
        self.lineEdit_tolerance = QtWidgets.QLineEdit(self.groupBox_line)
        self.lineEdit_tolerance.setObjectName("lineEdit_tolerance")
        self.lineEdit_tolerance.setMinimumSize(size_lineEdit)
        self.lineEdit_tolerance.setMaximumSize(size_lineEdit)
        self.lineEdit_tolerance.setFont(labelFont)
        # Add to form layout `tolerance`
        self.formLayout_tolerance.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_tolerance)

        # =====================
        # IN FORM LAYOUT AUTOID
        # =====================

        # (1, 1) Button `autoid`
        self.button_autoid = QtWidgets.QPushButton(self.groupBox_line)
        self.button_autoid.setObjectName("autoid")
        self.button_autoid.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button_autoid.setMinimumSize(QtCore.QSize(117, 22))
        self.button_autoid.setMaximumSize(QtCore.QSize(117, 22))
        self.button_autoid.setFont(buttonFont)
        # Add to form layout `autoid`
        self.formLayout_autoid.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.button_autoid)

        # (1, 2) Button `undo`
        self.button_undo = QtWidgets.QPushButton(self.groupBox_line)
        self.button_undo.setObjectName("undo")
        self.button_undo.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button_undo.setMinimumSize(size_lineEdit)
        self.button_undo.setMaximumSize(size_lineEdit)
        self.button_undo.setIcon(QtGui.QIcon.fromTheme("edit-undo"))
        self.button_undo.setFont(buttonFont)
        # Add to form layout `autoid`
        self.formLayout_autoid.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.button_undo)

        # ===========
        # RETRANSLATE
        # ===========

        self.retranslateUi(MainWindow)


    def retranslateUi(self, MainWindow):

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Wavelength Calibrator"))
        self.groupBox_peak.setTitle(_translate("MainWindow", "Peak Detection"))
        self.label_peak.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Peak parameters</span></p></body></html>"))
        self.label_height.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">height</span></p></body></html>"))
        self.label_threshold.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">threshold</span></p></body></html>"))
        self.label_distance.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">distance</span></p></body></html>"))
        self.label_prominence.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">prominence</span></p></body></html>"))
        self.label_width.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">width</span></p></body></html>"))
        self.label_wlen.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">wlen</span></p></body></html>"))
        self.label_rel.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">rel_height</span></p></body></html>"))
        self.label_plateau.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">plateau_size</span></p></body></html>"))
        self.label_help.setText(_translate("MainWindow", "<a href=\"https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html\">help</a>"))
        self.label_help.setOpenExternalLinks(True)
        self.button_find.setText(_translate("MainWindow", "Find"))

        self.groupBox_disp.setTitle(_translate("MainWindow", "Dispersion Solution"))
        self.label_disp.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Fit parameters</span></p></body></html>"))
        self.label_degree.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">degree</span></p></body></html>"))
        self.label_npieces.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">npieces</span></p></body></html>"))
        self.label_maxiters.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">maxiters</span></p></body></html>"))
        self.label_sigma_lower.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">sigma_lower</span></p></body></html>"))
        self.label_sigma_upper.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">sigma_upper</span></p></body></html>"))
        # self.label_switch.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">show_residual</span></p></body></html>"))
        self.button_residual.setText(_translate("MainWindow", "Show Residual"))
        self.button_fit.setText(_translate("MainWindow", "Fit"))
        self.button_mask.setText(_translate("MainWindow", "Mask"))
        self.button_unmask.setText(_translate("MainWindow", "Undo"))

        self.groupBox_line.setTitle(_translate("MainWindow", "Line Identification"))
        self.label_unit.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">wavelength unit</span></p></body></html>"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "WAVELENGTH"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "MASK"))
        self.label_tolerance.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">tolerance</span></p></body></html>"))
        self.button_autoid.setText(_translate("MainWindow", "Auto-identify"))
        self.button_undo.setText(_translate("MainWindow", "Undo"))