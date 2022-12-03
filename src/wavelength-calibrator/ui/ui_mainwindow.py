# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wavecal.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

# PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
# Matplotlib
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt

# switch
from .widgets import RectSwitch
# fonts
from .fonts import table_font


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # The main window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 800)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1200, 800))

        # The menu bar (Added by RNZ 11/06/2021)
        self.menu_bar = MainWindow.menuBar()
        self.menu_bar.setNativeMenuBar(False)
        self.file_menu = self.menu_bar.addMenu("&File")
        self.open_action = QtWidgets.QAction("Open File...", MainWindow)
        self.open_action.setShortcut("Ctrl+O")
        self.save_action = QtWidgets.QAction("Save As...", MainWindow)
        self.save_action.setShortcut("Ctrl+S")
        self.exit_action = QtWidgets.QAction("Exit", MainWindow)
        self.exit_action.setShortcut("Ctrl+Q")
        self.file_menu.addAction(self.open_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.save_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_action)
        self.help_menu = self.menu_bar.addMenu("&Help")
        self.about_action = QtWidgets.QAction("About", MainWindow)
        self.help_menu.addAction(self.about_action)

        # The central widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # The grid layout
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        
        # Group box `peak`
        self.GroupBox_peak = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GroupBox_peak.sizePolicy().hasHeightForWidth())
        self.GroupBox_peak.setSizePolicy(sizePolicy)
        self.GroupBox_peak.setMinimumSize(QtCore.QSize(100, 276))
        self.GroupBox_peak.setObjectName("GroupBox_peak")

        # Horizontal layout 1
        self.HorizontalLayout_1 = QtWidgets.QHBoxLayout(self.GroupBox_peak)
        self.HorizontalLayout_1.setObjectName("HorizontalLayout_1")

        # Vertical layout `spectrum`
        self.VerticalLayout_spectrum = QtWidgets.QVBoxLayout()
        self.VerticalLayout_spectrum.setObjectName("VerticalLayout_spectrum")

        # Canvas `spectrum`
        self.Figure_spectrum = plt.figure()
        self.FigureCanvas_spectrum = FigureCanvas(self.Figure_spectrum)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FigureCanvas_spectrum.sizePolicy().hasHeightForWidth())
        self.FigureCanvas_spectrum.setSizePolicy(sizePolicy)
        self.FigureCanvas_spectrum.setMinimumSize(QtCore.QSize(100, 276))
        self.FigureCanvas_spectrum.setObjectName("FigureCanvas_spectrum")
        
        # Tool bar `spectrum`
        self.ToolBar_spectrum = NavigationToolbar(self.FigureCanvas_spectrum, MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ToolBar_spectrum.sizePolicy().hasHeightForWidth())
        self.ToolBar_spectrum.setSizePolicy(sizePolicy)
        self.ToolBar_spectrum.setMinimumSize(QtCore.QSize(100, 30))
        self.ToolBar_spectrum.setMaximumSize(QtCore.QSize(16777215, 30))
        self.ToolBar_spectrum.setObjectName("ToolBar_spectrum")
        
        # Add to vertical layout `spectrum`
        self.VerticalLayout_spectrum.addWidget(self.ToolBar_spectrum)
        self.VerticalLayout_spectrum.addWidget(self.FigureCanvas_spectrum)

        # Add to horizontal layout 1
        self.HorizontalLayout_1.addLayout(self.VerticalLayout_spectrum)

        # Vertical layout `peak`
        self.VerticalLayout_peak = QtWidgets.QVBoxLayout()
        self.VerticalLayout_peak.setContentsMargins(5, -1, 5, -1)
        self.VerticalLayout_peak.setSpacing(5)
        self.VerticalLayout_peak.setObjectName("VerticalLayout_peak")

        # Label `peak`
        self.Label_peak = QtWidgets.QLabel(self.GroupBox_peak)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_peak.sizePolicy().hasHeightForWidth())
        self.Label_peak.setSizePolicy(sizePolicy)
        self.Label_peak.setMinimumSize(QtCore.QSize(180, 25))
        self.Label_peak.setMaximumSize(QtCore.QSize(180, 25))
        self.Label_peak.setObjectName("Label_peak")
        # Add to vertical layout `peak`
        self.VerticalLayout_peak.addWidget(self.Label_peak)

        # Line `peak`
        self.Line_peak = QtWidgets.QFrame(self.GroupBox_peak)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Line_peak.sizePolicy().hasHeightForWidth())
        self.Line_peak.setSizePolicy(sizePolicy)
        self.Line_peak.setMinimumSize(QtCore.QSize(180, 0))
        self.Line_peak.setMaximumSize(QtCore.QSize(180, 16777215))
        self.Line_peak.setFrameShape(QtWidgets.QFrame.HLine)
        self.Line_peak.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Line_peak.setObjectName("Line_peak")
        # Add to vertical layout `peak`
        self.VerticalLayout_peak.addWidget(self.Line_peak)

        # Form layout `peak`
        self.FormLayout_peak = QtWidgets.QFormLayout()
        self.FormLayout_peak.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.FormLayout_peak.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.FormLayout_peak.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.FormLayout_peak.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.FormLayout_peak.setContentsMargins(0, -1, 0, -1)
        self.FormLayout_peak.setHorizontalSpacing(10)
        self.FormLayout_peak.setObjectName("FormLayout_peak")
        # 1.1 height label
        self.Label_height = QtWidgets.QLabel(self.GroupBox_peak)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_height.sizePolicy().hasHeightForWidth())
        self.Label_height.setSizePolicy(sizePolicy)
        self.Label_height.setMinimumSize(QtCore.QSize(97, 20))
        self.Label_height.setMaximumSize(QtCore.QSize(97, 20))
        self.Label_height.setObjectName("Label_height")
        self.FormLayout_peak.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.Label_height)
        # 1.1 height lineedit
        self.LineEdit_height = QtWidgets.QLineEdit(self.GroupBox_peak)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LineEdit_height.sizePolicy().hasHeightForWidth())
        self.LineEdit_height.setSizePolicy(sizePolicy)
        self.LineEdit_height.setMinimumSize(QtCore.QSize(73, 20))
        self.LineEdit_height.setMaximumSize(QtCore.QSize(73, 20))
        self.LineEdit_height.setObjectName("LineEdit_height")
        self.FormLayout_peak.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.LineEdit_height)
        # 1.2 threshold label
        self.Label_threshold = QtWidgets.QLabel(self.GroupBox_peak)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_threshold.sizePolicy().hasHeightForWidth())
        self.Label_threshold.setSizePolicy(sizePolicy)
        self.Label_threshold.setMinimumSize(QtCore.QSize(97, 20))
        self.Label_threshold.setMaximumSize(QtCore.QSize(97, 20))
        self.Label_threshold.setObjectName("Label_threshold")
        self.FormLayout_peak.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.Label_threshold)
        # 1.2 threshold lineedit
        self.LineEdit_threshold = QtWidgets.QLineEdit(self.GroupBox_peak)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LineEdit_threshold.sizePolicy().hasHeightForWidth())
        self.LineEdit_threshold.setSizePolicy(sizePolicy)
        self.LineEdit_threshold.setMinimumSize(QtCore.QSize(73, 20))
        self.LineEdit_threshold.setMaximumSize(QtCore.QSize(73, 20))
        self.LineEdit_threshold.setObjectName("LineEdit_threshold")
        self.FormLayout_peak.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.LineEdit_threshold)
        # 1.3 distance label
        self.Label_distance = QtWidgets.QLabel(self.GroupBox_peak)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_distance.sizePolicy().hasHeightForWidth())
        self.Label_distance.setSizePolicy(sizePolicy)
        self.Label_distance.setMinimumSize(QtCore.QSize(97, 20))
        self.Label_distance.setMaximumSize(QtCore.QSize(97, 20))
        self.Label_distance.setObjectName("Label_distance")
        self.FormLayout_peak.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.Label_distance)
        # 1.3 distance lineedit
        self.LineEdit_distance = QtWidgets.QLineEdit(self.GroupBox_peak)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LineEdit_distance.sizePolicy().hasHeightForWidth())
        self.LineEdit_distance.setSizePolicy(sizePolicy)
        self.LineEdit_distance.setMinimumSize(QtCore.QSize(73, 20))
        self.LineEdit_distance.setMaximumSize(QtCore.QSize(73, 20))
        self.LineEdit_distance.setBaseSize(QtCore.QSize(0, 0))
        self.LineEdit_distance.setObjectName("LineEdit_distance")
        self.FormLayout_peak.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.LineEdit_distance)
        # 1.4 prominence label
        self.Label_prominence = QtWidgets.QLabel(self.GroupBox_peak)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_prominence.sizePolicy().hasHeightForWidth())
        self.Label_prominence.setSizePolicy(sizePolicy)
        self.Label_prominence.setMinimumSize(QtCore.QSize(97, 20))
        self.Label_prominence.setMaximumSize(QtCore.QSize(97, 20))
        self.Label_prominence.setObjectName("Label_prominence")
        self.FormLayout_peak.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.Label_prominence)
        # 1.4 prominence lineedit
        self.LineEdit_prominence = QtWidgets.QLineEdit(self.GroupBox_peak)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LineEdit_prominence.sizePolicy().hasHeightForWidth())
        self.LineEdit_prominence.setSizePolicy(sizePolicy)
        self.LineEdit_prominence.setMinimumSize(QtCore.QSize(73, 20))
        self.LineEdit_prominence.setMaximumSize(QtCore.QSize(73, 20))
        self.LineEdit_prominence.setObjectName("LineEdit_prominence")
        self.FormLayout_peak.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.LineEdit_prominence)
        # 1.5 width label
        self.Label_width = QtWidgets.QLabel(self.GroupBox_peak)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_width.sizePolicy().hasHeightForWidth())
        self.Label_width.setSizePolicy(sizePolicy)
        self.Label_width.setMinimumSize(QtCore.QSize(97, 20))
        self.Label_width.setMaximumSize(QtCore.QSize(97, 20))
        self.Label_width.setObjectName("Label_width")
        self.FormLayout_peak.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.Label_width)
        # 1.5 width lineedit
        self.LineEdit_width = QtWidgets.QLineEdit(self.GroupBox_peak)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LineEdit_width.sizePolicy().hasHeightForWidth())
        self.LineEdit_width.setSizePolicy(sizePolicy)
        self.LineEdit_width.setMinimumSize(QtCore.QSize(73, 20))
        self.LineEdit_width.setMaximumSize(QtCore.QSize(73, 20))
        self.LineEdit_width.setObjectName("LineEdit_width")
        self.FormLayout_peak.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.LineEdit_width)
        # 1.6 wlen label
        self.Label_wlen = QtWidgets.QLabel(self.GroupBox_peak)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_wlen.sizePolicy().hasHeightForWidth())
        self.Label_wlen.setSizePolicy(sizePolicy)
        self.Label_wlen.setMinimumSize(QtCore.QSize(97, 20))
        self.Label_wlen.setMaximumSize(QtCore.QSize(97, 20))
        self.Label_wlen.setObjectName("Label_wlen")
        self.FormLayout_peak.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.Label_wlen)
        # 1.6 wlen lineedit
        self.LineEdit_wlen = QtWidgets.QLineEdit(self.GroupBox_peak)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LineEdit_wlen.sizePolicy().hasHeightForWidth())
        self.LineEdit_wlen.setSizePolicy(sizePolicy)
        self.LineEdit_wlen.setMinimumSize(QtCore.QSize(73, 20))
        self.LineEdit_wlen.setMaximumSize(QtCore.QSize(73, 20))
        self.LineEdit_wlen.setObjectName("LineEdit_wlen")
        self.FormLayout_peak.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.LineEdit_wlen)
        # 1.7 rel label
        self.Label_rel = QtWidgets.QLabel(self.GroupBox_peak)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_rel.sizePolicy().hasHeightForWidth())
        self.Label_rel.setSizePolicy(sizePolicy)
        self.Label_rel.setMinimumSize(QtCore.QSize(97, 20))
        self.Label_rel.setMaximumSize(QtCore.QSize(97, 20))
        self.Label_rel.setObjectName("Label_rel")
        self.FormLayout_peak.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.Label_rel)
        # 1.7 rel lineedit
        self.LineEdit_rel = QtWidgets.QLineEdit(self.GroupBox_peak)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LineEdit_rel.sizePolicy().hasHeightForWidth())
        self.LineEdit_rel.setSizePolicy(sizePolicy)
        self.LineEdit_rel.setMinimumSize(QtCore.QSize(73, 20))
        self.LineEdit_rel.setMaximumSize(QtCore.QSize(73, 20))
        self.LineEdit_rel.setObjectName("LineEdit_rel")
        self.FormLayout_peak.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.LineEdit_rel)
        # 1.8 plateau label
        self.Label_plateau = QtWidgets.QLabel(self.GroupBox_peak)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_plateau.sizePolicy().hasHeightForWidth())
        self.Label_plateau.setSizePolicy(sizePolicy)
        self.Label_plateau.setMinimumSize(QtCore.QSize(97, 20))
        self.Label_plateau.setMaximumSize(QtCore.QSize(97, 20))
        self.Label_plateau.setObjectName("Label_plateau")
        self.FormLayout_peak.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.Label_plateau)
        # 1.8 plateau lineedit
        self.LineEdit_plateau = QtWidgets.QLineEdit(self.GroupBox_peak)
        self.LineEdit_plateau.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LineEdit_plateau.sizePolicy().hasHeightForWidth())
        self.LineEdit_plateau.setSizePolicy(sizePolicy)
        self.LineEdit_plateau.setMinimumSize(QtCore.QSize(73, 20))
        self.LineEdit_plateau.setMaximumSize(QtCore.QSize(73, 20))
        self.LineEdit_plateau.setObjectName("LineEdit_plateau")
        self.FormLayout_peak.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.LineEdit_plateau)
        # 1.9 help label (Added by RNZ 11/06/2021)
        self.Label_help_find_peak = QtWidgets.QLabel(self.GroupBox_peak)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_help_find_peak.sizePolicy().hasHeightForWidth())
        self.Label_help_find_peak.setSizePolicy(sizePolicy)
        self.Label_help_find_peak.setMinimumSize(QtCore.QSize(73, 20))
        self.Label_help_find_peak.setMaximumSize(QtCore.QSize(73, 20))
        self.Label_help_find_peak.setObjectName("Label_help_find_peak")
        self.FormLayout_peak.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.Label_help_find_peak)
        
        # Add to vertical layout `peak`
        self.VerticalLayout_peak.addLayout(self.FormLayout_peak)
        
        # Button `Find`
        self.Button_find = QtWidgets.QPushButton(self.GroupBox_peak)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Button_find.sizePolicy().hasHeightForWidth())
        self.Button_find.setSizePolicy(sizePolicy)
        self.Button_find.setMinimumSize(QtCore.QSize(180, 20))
        self.Button_find.setMaximumSize(QtCore.QSize(180, 20))
        self.Button_find.setObjectName("Button_find")
        # Add to vertical layout `peak`
        self.VerticalLayout_peak.addWidget(self.Button_find)
        
        # Add to horizontal layout 1
        self.HorizontalLayout_1.addLayout(self.VerticalLayout_peak)
        self.HorizontalLayout_1.setStretch(0, 1)
        
        # Add to the grid layout
        self.gridLayout.addWidget(self.GroupBox_peak, 0, 0, 1, 1)

        # Group box `line`
        self.GroupBox_line = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GroupBox_line.sizePolicy().hasHeightForWidth())
        self.GroupBox_line.setSizePolicy(sizePolicy)
        self.GroupBox_line.setMinimumSize(QtCore.QSize(230, 700))
        self.GroupBox_line.setMaximumSize(QtCore.QSize(230, 16777215))
        self.GroupBox_line.setObjectName("GroupBox_line")

        # Vertical layout 2
        self.VerticalLayout_2 = QtWidgets.QVBoxLayout(self.GroupBox_line)
        self.VerticalLayout_2.setContentsMargins(5, -1, 5, -1)
        self.VerticalLayout_2.setSpacing(10)
        self.VerticalLayout_2.setObjectName("VerticalLayout_2")

        # Table widget `line`
        self.TableWidget_line = QtWidgets.QTableWidget(self.GroupBox_line)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TableWidget_line.sizePolicy().hasHeightForWidth())
        self.TableWidget_line.setSizePolicy(sizePolicy)
        self.TableWidget_line.setMinimumSize(QtCore.QSize(210, 600))
        self.TableWidget_line.setMaximumSize(QtCore.QSize(210, 16777215))
        self.TableWidget_line.setObjectName("TableWidget_line")
        self.TableWidget_line.setColumnCount(2)
        self.TableWidget_line.setRowCount(0)

        # Header 0
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFont(table_font)
        self.TableWidget_line.setHorizontalHeaderItem(0, item)

        # Header 1
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFont(table_font)
        self.TableWidget_line.setHorizontalHeaderItem(1, item)
        
        # Resize mode
        self.TableWidget_line.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.TableWidget_line.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

        # Add to vertical layout 2
        self.VerticalLayout_2.addWidget(self.TableWidget_line)

        # Form layout `unit`
        self.FormLayout_unit = QtWidgets.QFormLayout()
        self.FormLayout_unit.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.FormLayout_unit.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.FormLayout_unit.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.FormLayout_unit.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.FormLayout_unit.setContentsMargins(2, -1, 0, -1)
        self.FormLayout_unit.setHorizontalSpacing(10)
        self.FormLayout_unit.setObjectName("FormLayout_unit")

        # unit label
        self.Label_unit = QtWidgets.QLabel(self.GroupBox_line)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_unit.sizePolicy().hasHeightForWidth())
        self.Label_unit.setSizePolicy(sizePolicy)
        self.Label_unit.setMinimumSize(QtCore.QSize(108, 20))
        self.Label_unit.setMaximumSize(QtCore.QSize(108, 20))
        self.Label_unit.setObjectName("Label_unit")
        self.FormLayout_unit.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.Label_unit)
        # unit lineedit
        self.LineEdit_unit = QtWidgets.QLineEdit(self.GroupBox_line)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LineEdit_unit.sizePolicy().hasHeightForWidth())
        self.LineEdit_unit.setSizePolicy(sizePolicy)
        self.LineEdit_unit.setMinimumSize(QtCore.QSize(90, 20))
        self.LineEdit_unit.setMaximumSize(QtCore.QSize(90, 20))
        self.LineEdit_unit.setObjectName("LineEdit_unit")
        self.FormLayout_unit.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.LineEdit_unit)

        # Add to vertical layout 2
        self.VerticalLayout_2.addLayout(self.FormLayout_unit)
        self.VerticalLayout_2.setStretch(0, 1)

        # Add to the grid layout
        self.gridLayout.addWidget(self.GroupBox_line, 0, 1, 2, 1)

        # Group box `disp`
        self.GroupBox_disp = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GroupBox_disp.sizePolicy().hasHeightForWidth())
        self.GroupBox_disp.setSizePolicy(sizePolicy)
        self.GroupBox_disp.setMinimumSize(QtCore.QSize(100, 276))
        self.GroupBox_disp.setObjectName("GroupBox_disp")
        
        # Horizontal layout 3
        self.HorizontalLayout_3 = QtWidgets.QHBoxLayout(self.GroupBox_disp)
        self.HorizontalLayout_3.setObjectName("HorizontalLayout_3")

        # Vertical layout `fit`
        self.VerticalLayout_fit = QtWidgets.QVBoxLayout()
        self.VerticalLayout_fit.setObjectName("VerticalLayout_fit")

        # Canvas `fit`
        self.Figure_fit = plt.figure()
        self.FigureCanvas_fit = FigureCanvas(self.Figure_fit)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FigureCanvas_fit.sizePolicy().hasHeightForWidth())
        self.FigureCanvas_fit.setSizePolicy(sizePolicy)
        self.FigureCanvas_fit.setMinimumSize(QtCore.QSize(100, 276))
        self.FigureCanvas_fit.setObjectName("FigureCanvas_fit")

        # Tool bar `fit`
        self.ToolBar_fit = NavigationToolbar(self.FigureCanvas_fit, MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ToolBar_fit.sizePolicy().hasHeightForWidth())
        self.ToolBar_fit.setSizePolicy(sizePolicy)
        self.ToolBar_fit.setMinimumSize(QtCore.QSize(100, 30))
        self.ToolBar_fit.setMaximumSize(QtCore.QSize(16777215, 30))
        self.ToolBar_fit.setObjectName("ToolBar_fit")
        
        # Add to Vertical layout `fit`
        self.VerticalLayout_fit.addWidget(self.ToolBar_fit)
        self.VerticalLayout_fit.addWidget(self.FigureCanvas_fit)
        
        # Add to horizontal layout 3
        self.HorizontalLayout_3.addLayout(self.VerticalLayout_fit)

        # Vertical layout `disp`
        self.VerticalLayout_disp = QtWidgets.QVBoxLayout()
        self.VerticalLayout_disp.setSpacing(5)
        self.VerticalLayout_disp.setContentsMargins(5, -1, 5, -1)
        self.VerticalLayout_disp.setObjectName("VerticalLayout_disp")

        # Label `disp`
        self.Label_disp = QtWidgets.QLabel(self.GroupBox_disp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_disp.sizePolicy().hasHeightForWidth())
        self.Label_disp.setSizePolicy(sizePolicy)
        self.Label_disp.setMinimumSize(QtCore.QSize(180, 25))
        self.Label_disp.setMaximumSize(QtCore.QSize(180, 25))
        self.Label_disp.setObjectName("Label_disp")
        # Add to vertical layout `disp`
        self.VerticalLayout_disp.addWidget(self.Label_disp)
        
        # Line `disp`
        self.Line_disp = QtWidgets.QFrame(self.GroupBox_disp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Line_disp.sizePolicy().hasHeightForWidth())
        self.Line_disp.setSizePolicy(sizePolicy)
        self.Line_disp.setMinimumSize(QtCore.QSize(180, 0))
        self.Line_disp.setMaximumSize(QtCore.QSize(180, 16777215))
        self.Line_disp.setFrameShape(QtWidgets.QFrame.HLine)
        self.Line_disp.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Line_disp.setObjectName("Line_disp")
        # Add to vertical layout `disp`
        self.VerticalLayout_disp.addWidget(self.Line_disp)

        # Form layout `disp`
        self.FormLayout_disp = QtWidgets.QFormLayout()
        self.FormLayout_disp.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.FormLayout_disp.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.FormLayout_disp.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.FormLayout_disp.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.FormLayout_disp.setContentsMargins(0, -1, 0, -1)
        self.FormLayout_disp.setHorizontalSpacing(17)
        self.FormLayout_disp.setObjectName("FormLayout_disp")
        # 1.1 npieces label
        self.Label_npieces = QtWidgets.QLabel(self.GroupBox_disp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_npieces.sizePolicy().hasHeightForWidth())
        self.Label_npieces.setSizePolicy(sizePolicy)
        self.Label_npieces.setMinimumSize(QtCore.QSize(90, 20))
        self.Label_npieces.setMaximumSize(QtCore.QSize(90, 20))
        self.Label_npieces.setObjectName("Label_npieces")
        self.FormLayout_disp.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.Label_npieces)
        # 1.1 npieces lineedit
        self.LineEdit_npieces = QtWidgets.QLineEdit(self.GroupBox_disp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LineEdit_npieces.sizePolicy().hasHeightForWidth())
        self.LineEdit_npieces.setSizePolicy(sizePolicy)
        self.LineEdit_npieces.setMinimumSize(QtCore.QSize(73, 20))
        self.LineEdit_npieces.setMaximumSize(QtCore.QSize(73, 20))
        self.LineEdit_npieces.setObjectName("LineEdit_npieces")
        self.FormLayout_disp.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.LineEdit_npieces)
        # # 1.2 sig_lower label
        # self.Label_sig_lower = QtWidgets.QLabel(self.GroupBox_disp)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.Label_sig_lower.sizePolicy().hasHeightForWidth())
        # self.Label_sig_lower.setSizePolicy(sizePolicy)
        # self.Label_sig_lower.setMinimumSize(QtCore.QSize(90, 20))
        # self.Label_sig_lower.setMaximumSize(QtCore.QSize(90, 20))
        # self.Label_sig_lower.setObjectName("Label_sig_lower")
        # self.FormLayout_disp.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.Label_sig_lower)
        # # 1.2 sig_lower lineedit
        # self.LineEdit_sig_lower = QtWidgets.QLineEdit(self.GroupBox_disp)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.LineEdit_sig_lower.sizePolicy().hasHeightForWidth())
        # self.LineEdit_sig_lower.setSizePolicy(sizePolicy)
        # self.LineEdit_sig_lower.setMinimumSize(QtCore.QSize(73, 20))
        # self.LineEdit_sig_lower.setMaximumSize(QtCore.QSize(73, 20))
        # self.LineEdit_sig_lower.setObjectName("LineEdit_sig_lower")
        # self.FormLayout_disp.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.LineEdit_sig_lower)
        # # 1.3 sig_upper label
        # self.Label_sig_upper = QtWidgets.QLabel(self.GroupBox_disp)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.Label_sig_upper.sizePolicy().hasHeightForWidth())
        # self.Label_sig_upper.setSizePolicy(sizePolicy)
        # self.Label_sig_upper.setMinimumSize(QtCore.QSize(90, 20))
        # self.Label_sig_upper.setMaximumSize(QtCore.QSize(90, 20))
        # self.Label_sig_upper.setObjectName("Label_sig_upper")
        # self.FormLayout_disp.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.Label_sig_upper)
        # # 1.3 sig_upper lineedit
        # self.LineEdit_sig_upper = QtWidgets.QLineEdit(self.GroupBox_disp)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.LineEdit_sig_upper.sizePolicy().hasHeightForWidth())
        # self.LineEdit_sig_upper.setSizePolicy(sizePolicy)
        # self.LineEdit_sig_upper.setMinimumSize(QtCore.QSize(73, 20))
        # self.LineEdit_sig_upper.setMaximumSize(QtCore.QSize(73, 20))
        # self.LineEdit_sig_upper.setObjectName("LineEdit_sig_upper")
        # self.FormLayout_disp.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.LineEdit_sig_upper)
        # # 1.4 maxiter label
        # self.Label_maxiter = QtWidgets.QLabel(self.GroupBox_disp)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.Label_maxiter.sizePolicy().hasHeightForWidth())
        # self.Label_maxiter.setSizePolicy(sizePolicy)
        # self.Label_maxiter.setMinimumSize(QtCore.QSize(90, 20))
        # self.Label_maxiter.setMaximumSize(QtCore.QSize(90, 20))
        # self.Label_maxiter.setObjectName("Label_maxiter")
        # self.FormLayout_disp.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.Label_maxiter)
        # # 1.4 maxiter lineedit
        # self.LineEdit_maxiter = QtWidgets.QLineEdit(self.GroupBox_disp)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.LineEdit_maxiter.sizePolicy().hasHeightForWidth())
        # self.LineEdit_maxiter.setSizePolicy(sizePolicy)
        # self.LineEdit_maxiter.setMinimumSize(QtCore.QSize(73, 20))
        # self.LineEdit_maxiter.setMaximumSize(QtCore.QSize(73, 20))
        # self.LineEdit_maxiter.setObjectName("LineEdit_maxiter")
        # self.FormLayout_disp.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.LineEdit_maxiter)
        # 1.5 the switch label
        self.Label_switch = QtWidgets.QLabel(self.GroupBox_disp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_switch.sizePolicy().hasHeightForWidth())
        self.Label_switch.setSizePolicy(sizePolicy)
        self.Label_switch.setMinimumSize(QtCore.QSize(90, 20))
        self.Label_switch.setMaximumSize(QtCore.QSize(90, 20))
        self.Label_switch.setObjectName("Label_switch")
        self.FormLayout_disp.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.Label_switch)
        # 1.5 the switch
        self.RectSwitch = RectSwitch(self.GroupBox_disp, margin=-9, thumb_width=0.4, duration=150)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RectSwitch.sizePolicy().hasHeightForWidth())
        self.RectSwitch.setSizePolicy(sizePolicy)
        self.RectSwitch.setMinimumSize(QtCore.QSize(73, 20))
        self.RectSwitch.setMaximumSize(QtCore.QSize(73, 20))
        self.RectSwitch.setObjectName("RectSwitch")
        self.FormLayout_disp.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.RectSwitch)

        # Add to vertical layout `disp`
        self.VerticalLayout_disp.addLayout(self.FormLayout_disp)
        
        # Button `fit`
        self.Button_fit = QtWidgets.QPushButton(self.GroupBox_disp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Button_fit.sizePolicy().hasHeightForWidth())
        self.Button_fit.setSizePolicy(sizePolicy)
        self.Button_fit.setMinimumSize(QtCore.QSize(180, 20))
        self.Button_fit.setMaximumSize(QtCore.QSize(180, 20))
        self.Button_fit.setObjectName("Button_fit")
        # Add to vertical layout `disp`
        self.VerticalLayout_disp.addWidget(self.Button_fit)
        
        # Add to horizontal layout 3
        self.HorizontalLayout_3.addLayout(self.VerticalLayout_disp)
        self.HorizontalLayout_3.setStretch(0, 1)
        
        # Add to the grid layout
        self.gridLayout.addWidget(self.GroupBox_disp, 1, 0, 1, 1)
        self.gridLayout.setRowMinimumHeight(0, 1)
        self.gridLayout.setRowMinimumHeight(1, 1)
        self.gridLayout.setColumnStretch(0, 1)

        # Add to the main window
        MainWindow.setCentralWidget(self.centralwidget)
        
        # The status bar
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        # Add to the main window
        MainWindow.setStatusBar(self.statusBar)

        # Retranslate
        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Wavelength Calibrator"))
        self.GroupBox_peak.setTitle(_translate("MainWindow", "Peak Detection"))
        self.Label_peak.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Peak parameters</span></p></body></html>"))
        self.Label_height.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">height</span></p></body></html>"))
        self.Label_threshold.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">threshold</span></p></body></html>"))
        self.Label_distance.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">distance</span></p></body></html>"))
        self.Label_prominence.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">prominence</span></p></body></html>"))
        self.Label_width.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">width</span></p></body></html>"))
        self.Label_wlen.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">wlen</span></p></body></html>"))
        self.Label_rel.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">rel_height</span></p></body></html>"))
        self.Label_plateau.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">plateau_size</span></p></body></html>"))
        self.Label_help_find_peak.setText(_translate("MainWindow", "<a href=\"https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html\">help</a>"))
        self.Label_help_find_peak.setOpenExternalLinks(True)
        self.Button_find.setText(_translate("MainWindow", "Find"))
        
        self.GroupBox_line.setTitle(_translate("MainWindow", "Line Identification"))
        self.Label_unit.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">wavelength unit</span></p></body></html>"))
        item = self.TableWidget_line.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "WAVELENGTH"))
        item = self.TableWidget_line.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "MASK"))
        
        self.GroupBox_disp.setTitle(_translate("MainWindow", "Dispersion Solution"))
        self.Label_disp.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Fit parameters</span></p></body></html>"))
        self.Label_npieces.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">npieces</span></p></body></html>"))
        # self.Label_sig_lower.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">sigma_lower</span></p></body></html>"))
        # self.Label_sig_upper.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">sigma_upper</span></p></body></html>"))
        # self.Label_maxiter.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">maxiter</span></p></body></html>"))
        self.Label_switch.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">show_residual</span></p></body></html>"))
        self.Button_fit.setText(_translate("MainWindow", "Fit"))
    