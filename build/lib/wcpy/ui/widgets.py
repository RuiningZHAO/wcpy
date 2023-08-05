# -*- coding: utf-8 -*-
# PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets


class TableItemCompleter(QtWidgets.QStyledItemDelegate):

    def createEditor(self, parent, option, index):

        editor = QtWidgets.QLineEdit(parent)
        # Positive integer or float
        editor.setValidator(
            QtGui.QRegExpValidator(
                QtCore.QRegExp("^([1-9]\d*)|([1-9]\d*\.\d*)|(0\.\d*[1-9]\d*)|()$")
            )
        )
        # Auto-completion
        completion_list = index.data(QtCore.Qt.UserRole)
        completer = QtWidgets.QCompleter(completion_list, parent)
        editor.setCompleter(completer)

        return editor


class FormLayout(QtWidgets.QFormLayout):

    def __init__(self, object_name=None):

        super().__init__()

        if object_name is not None:
            self.setObjectName(object_name)

        self.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.setLabelAlignment(
            QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.setFormAlignment(
            QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.setContentsMargins(0, -1, 0, -1)
        self.setHorizontalSpacing(10)


class InformationBox(QtWidgets.QMessageBox):

    def __init__(self, window_title=None, text=None):

        super().__init__()

        self.setIcon(QtWidgets.QMessageBox.Information)
        self.setWindowTitle(window_title)
        self.setText(text)


class CheckBoxFileDialog(QtWidgets.QFileDialog):

    def __init__(self, checkBox_text=None):

        super().__init__()

        self.setOption(QtWidgets.QFileDialog.DontUseNativeDialog)
        if checkBox_text is not None:
            self.checkBox = QtWidgets.QCheckBox(text=checkBox_text)
            self.layout().addWidget(self.checkBox)


# Deprecated in 0.0.2.0 (RNZ 07/20/2023)
class RectSwitch(QtWidgets.QAbstractButton):

    def __init__(self, parent=None, margin=2, thumb_width=0.6, duration=150):

        super().__init__(parent=parent)

        self._margin = margin
        self._thumb_width = thumb_width
        self._duration = duration
        self.setColor()
        self.setCheckable(True)
        self.setFixedSize(self.sizeHint())


    def setColor(self):

        palette = self.palette()
        # Border color
        self._light_border_color = palette.light().color() # QColor
        self._dark_border_color = palette.shadow().color() # QColor
        # Face brush
        if self._margin < 0:
            self._track_brush = palette.shadow()  # QBrush
        else:
            self._track_brush = palette.light()   # QBrush
        self._thumb_brush = palette.button()      # QBrush
        # Opacity
        self._track_opacity = 1
        self._thumb_opacity = 1
        # Text
        self._text = {
            True: 'on',
            False: 'off',
        }
        self._text_color = {
            True: QtCore.Qt.black,             # QColor
            False: palette.mid().color()       # QColor
        }
        self._text_opacity = 1


    def sizeHint(self):

        return QtCore.QSize(80, 20)


    def setGeometry(self):

        self._track_width = min(self.width(), self.width() + 2 * self._margin)
        self._track_height = min(self.height(), self.height() + 2 * self._margin)
        self._thumb_width *= self.width()
        self._thumb_height = self._track_height - 2 * self._margin

        if self._margin > 0:
            self._base_offset = self._margin + self._thumb_width / 2
        else:
            self._base_offset = self._thumb_width / 2
        self._end_offset = {
            True: lambda: self.width() - self._base_offset,
            False: lambda: self._base_offset,
        }
        self._offset = self._base_offset


    def resizeEvent(self, event):

        super().resizeEvent(event)
        self.setGeometry()
        self.offset = self._end_offset[self.isChecked()]()


    @QtCore.Property(int)
    def offset(self):

        return self._offset


    @offset.setter
    def offset(self, value):

        self._offset = value
        self.update()

    # def setChecked(self, checked):
    # 
    #     super().setChecked(checked)
    #     self.offset = self._end_offset[checked]()

    def paintEvent(self, event):

        light_border_color = self._light_border_color
        dark_border_color = self._dark_border_color
        track_brush = self._track_brush
        thumb_brush = self._thumb_brush
        text_color = self._text_color[self.isEnabled()]
        track_opacity = self._track_opacity
        thumb_opacity = self._thumb_opacity
        text_opacity = self._text_opacity

        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing, True)

        p.setBrush(track_brush)
        p.setOpacity(track_opacity)
        p.setPen(QtCore.Qt.NoPen)
        p.drawRect(
            self._base_offset - self._thumb_width / 2 - self._margin,
            self.height() / 2 - self._thumb_height / 2 - self._margin,
            self._track_width,
            self._track_height,
        )
        p.setBrush(thumb_brush)
        p.setOpacity(thumb_opacity)
        p.setPen(QtGui.QPen(light_border_color, 1.2, QtCore.Qt.SolidLine))
        p.drawRect(
            self.offset - self._thumb_width / 2,
            self.height() / 2 - self._thumb_height / 2,
            self._thumb_width,
            self._thumb_height,
        )
        p.setPen(QtGui.QPen(dark_border_color, 1.5, QtCore.Qt.SolidLine))
        p.drawLine(
            self.offset - self._thumb_width / 2 + 1.2,
            self.height() / 2 + self._thumb_height / 2 - 1,
            self.offset + self._thumb_width / 2 - 0.5,
            self.height() / 2 + self._thumb_height / 2 - 1,
        )
        p.drawLine(
            self.offset + self._thumb_width / 2,
            self.height() / 2 - self._thumb_height / 2 + 1.2,
            self.offset + self._thumb_width / 2,
            self.height() / 2 + self._thumb_height / 2 - 0.5,
        )
        p.setPen(text_color)
        p.setOpacity(text_opacity)
        font = p.font()
        font.setPixelSize(0.65 * self._thumb_height)
        p.setFont(font)
        p.drawText(
            QtCore.QRectF(
                self.offset - self._thumb_width / 2,
                self.height() / 2 - self._thumb_height / 2,
                self._thumb_width,
                self._thumb_height,
            ),
            QtCore.Qt.AlignCenter,
            self._text[self.isChecked()],
        )


    def mouseReleaseEvent(self, event):

        super().mouseReleaseEvent(event)

        if event.button() == QtCore.Qt.LeftButton:
            anim = QtCore.QPropertyAnimation(self, b'offset', self)
            anim.setDuration(self._duration)
            anim.setStartValue(self.offset)
            anim.setEndValue(self._end_offset[self.isChecked()]())
            anim.start()


    def enterEvent(self, event):
        
        self.setCursor(QtCore.Qt.PointingHandCursor)
        super().enterEvent(event)


if __name__ == '__main__':

    app = QtWidgets.QApplication([])

    # Thumb size < track size (Gitlab style)
    rs1 = RectSwitch(margin=2, thumb_width=0.6)
    rs1.toggled.connect(lambda c: print('toggled', c))
    rs1.clicked.connect(lambda c: print('clicked', c))
    rs1.pressed.connect(lambda: print('pressed'))
    rs1.released.connect(lambda: print('released'))
    rs2 = RectSwitch(margin=2, thumb_width=0.6)
    rs2.setEnabled(False)

    layout = QtWidgets.QHBoxLayout()
    layout.addWidget(rs1)
    layout.addWidget(rs2)
    widget = QtWidgets.QWidget()
    widget.setLayout(layout)
    widget.show()

    app.exec()