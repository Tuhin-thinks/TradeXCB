# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Raw/api_inp_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1122, 612)
        Dialog.setMinimumSize(QtCore.QSize(1122, 0))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 214, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 70, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(77, 77, 77))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(68, 68, 68))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(212, 212, 212))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 214, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(77, 77, 77))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 44, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(43, 43, 43))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(81, 81, 81))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 214, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(77, 77, 77))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(109, 109, 109))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 57, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(145, 145, 145))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        Dialog.setPalette(palette)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_bg_gradient_frame = QtWidgets.QFrame(Dialog)
        palette = QtGui.QPalette()
        gradient = QtGui.QLinearGradient(0.0, 0.0, 1.0, 1.0)
        gradient.setSpread(QtGui.QGradient.ReflectSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(0, 255, 0))
        gradient.setColorAt(1.0, QtGui.QColor(0, 70, 0))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        gradient = QtGui.QLinearGradient(0.0, 0.0, 1.0, 1.0)
        gradient.setSpread(QtGui.QGradient.ReflectSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(0, 255, 0))
        gradient.setColorAt(1.0, QtGui.QColor(0, 70, 0))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        gradient = QtGui.QLinearGradient(0.0, 0.0, 1.0, 1.0)
        gradient.setSpread(QtGui.QGradient.ReflectSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(0, 255, 0))
        gradient.setColorAt(1.0, QtGui.QColor(0, 70, 0))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        gradient = QtGui.QLinearGradient(0.0, 0.0, 1.0, 1.0)
        gradient.setSpread(QtGui.QGradient.ReflectSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(0, 255, 0))
        gradient.setColorAt(1.0, QtGui.QColor(0, 70, 0))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        gradient = QtGui.QLinearGradient(0.0, 0.0, 1.0, 1.0)
        gradient.setSpread(QtGui.QGradient.ReflectSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(0, 255, 0))
        gradient.setColorAt(1.0, QtGui.QColor(0, 70, 0))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        gradient = QtGui.QLinearGradient(0.0, 0.0, 1.0, 1.0)
        gradient.setSpread(QtGui.QGradient.ReflectSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(0, 255, 0))
        gradient.setColorAt(1.0, QtGui.QColor(0, 70, 0))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        gradient = QtGui.QLinearGradient(0.0, 0.0, 1.0, 1.0)
        gradient.setSpread(QtGui.QGradient.ReflectSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(0, 255, 0))
        gradient.setColorAt(1.0, QtGui.QColor(0, 70, 0))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        gradient = QtGui.QLinearGradient(0.0, 0.0, 1.0, 1.0)
        gradient.setSpread(QtGui.QGradient.ReflectSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(0, 255, 0))
        gradient.setColorAt(1.0, QtGui.QColor(0, 70, 0))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        gradient = QtGui.QLinearGradient(0.0, 0.0, 1.0, 1.0)
        gradient.setSpread(QtGui.QGradient.ReflectSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(0, 255, 0))
        gradient.setColorAt(1.0, QtGui.QColor(0, 70, 0))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.frame_bg_gradient_frame.setPalette(palette)
        self.frame_bg_gradient_frame.setStyleSheet("#frame_bg_gradient_frame{\n"
                                                   "    background-color:qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:1, stop:0 #00ff00, stop:1 #004600); \n"
                                                   "    border:2px outset transparent;\n"
                                                   "    border-radius: 15px 15px 15px 5px;\n"
                                                   "    background-repeat: 0;\n"
                                                   "    background-position: center;\n"
                                                   "}")
        self.frame_bg_gradient_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_bg_gradient_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_bg_gradient_frame.setObjectName("frame_bg_gradient_frame")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.frame_bg_gradient_frame)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.frame_api_details_inp = QtWidgets.QFrame(self.frame_bg_gradient_frame)
        self.frame_api_details_inp.setMaximumSize(QtCore.QSize(550, 16777215))
        self.frame_api_details_inp.setStyleSheet("#frame_api_details_inp{\n"
                                                 "border:2px outset transparent;\n"
                                                 "    border-radius: 15px 15px 15px 5px;\n"
                                                 "}\n"
                                                 "#frame_api_details_inp QLabel{\n"
                                                 "    color: black;\n"
                                                 "    \n"
                                                 "    font: 10pt \"Serif\";\n"
                                                 "}\n"
                                                 "#frame_api_details_inp::hover{\n"
                                                 "    background-color: rgba(254, 254, 254, 30); \n"
                                                 "    border:2px outset transparent;\n"
                                                 "    border-radius: 15px 15px 15px 5px;\n"
                                                 "}\n"
                                                 ".QLineEdit{\n"
                                                 "    border: 1px solid gray;\n"
                                                 "    border-radius: 5px;\n"
                                                 "    padding: 0.6ex;\n"
                                                 "    font-weight: bold;\n"
                                                 "    font: 10pt \"Serif\";\n"
                                                 "}")
        self.frame_api_details_inp.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_api_details_inp.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_api_details_inp.setObjectName("frame_api_details_inp")
        self.gridLayout_20 = QtWidgets.QGridLayout(self.frame_api_details_inp)
        self.gridLayout_20.setContentsMargins(-1, 0, -1, 0)
        self.gridLayout_20.setVerticalSpacing(2)
        self.gridLayout_20.setObjectName("gridLayout_20")
        self.frame_api_buttons = QtWidgets.QFrame(self.frame_api_details_inp)
        self.frame_api_buttons.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_api_buttons.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_api_buttons.setObjectName("frame_api_buttons")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_api_buttons)
        self.horizontalLayout_2.setContentsMargins(0, 5, 0, 5)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton_submit_api_details = QtWidgets.QPushButton(self.frame_api_buttons)
        self.pushButton_submit_api_details.setMaximumSize(QtCore.QSize(179, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/submit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_submit_api_details.setIcon(icon)
        self.pushButton_submit_api_details.setObjectName("pushButton_submit_api_details")
        self.horizontalLayout_2.addWidget(self.pushButton_submit_api_details)
        self.pushButton_edit_api_details = QtWidgets.QPushButton(self.frame_api_buttons)
        self.pushButton_edit_api_details.setMaximumSize(QtCore.QSize(179, 30))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_edit_api_details.setIcon(icon1)
        self.pushButton_edit_api_details.setObjectName("pushButton_edit_api_details")
        self.horizontalLayout_2.addWidget(self.pushButton_edit_api_details)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.gridLayout_20.addWidget(self.frame_api_buttons, 2, 0, 1, 1)
        self.frame_api_inp_fields = QtWidgets.QFrame(self.frame_api_details_inp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_api_inp_fields.sizePolicy().hasHeightForWidth())
        self.frame_api_inp_fields.setSizePolicy(sizePolicy)
        self.frame_api_inp_fields.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_api_inp_fields.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_api_inp_fields.setObjectName("frame_api_inp_fields")
        self.gridLayout_23 = QtWidgets.QGridLayout(self.frame_api_inp_fields)
        self.gridLayout_23.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_23.setSpacing(0)
        self.gridLayout_23.setObjectName("gridLayout_23")
        self.frame_25 = QtWidgets.QFrame(self.frame_api_inp_fields)
        self.frame_25.setMinimumSize(QtCore.QSize(0, 70))
        self.frame_25.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_25.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_25.setObjectName("frame_25")
        self.gridLayout_22 = QtWidgets.QGridLayout(self.frame_25)
        self.gridLayout_22.setContentsMargins(-1, 5, -1, 5)
        self.gridLayout_22.setVerticalSpacing(2)
        self.gridLayout_22.setObjectName("gridLayout_22")
        self.label_7 = QtWidgets.QLabel(self.frame_25)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_22.addWidget(self.label_7, 0, 0, 1, 1)
        self.comboBox_stock_broker_name = QtWidgets.QComboBox(self.frame_25)
        self.comboBox_stock_broker_name.setMinimumSize(QtCore.QSize(0, 28))
        self.comboBox_stock_broker_name.setMaximumSize(QtCore.QSize(200, 16777215))
        self.comboBox_stock_broker_name.setObjectName("comboBox_stock_broker_name")
        self.gridLayout_22.addWidget(self.comboBox_stock_broker_name, 1, 0, 1, 1)
        self.gridLayout_23.addWidget(self.frame_25, 0, 0, 1, 1)
        self.frame_6 = QtWidgets.QFrame(self.frame_api_inp_fields)
        self.frame_6.setMinimumSize(QtCore.QSize(0, 70))
        self.frame_6.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.gridLayout_14 = QtWidgets.QGridLayout(self.frame_6)
        self.gridLayout_14.setContentsMargins(-1, 5, -1, 5)
        self.gridLayout_14.setVerticalSpacing(2)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.label = QtWidgets.QLabel(self.frame_6)
        self.label.setMinimumSize(QtCore.QSize(150, 0))
        self.label.setObjectName("label")
        self.gridLayout_14.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_api_key = QtWidgets.QLineEdit(self.frame_6)
        self.lineEdit_api_key.setMinimumSize(QtCore.QSize(0, 22))
        self.lineEdit_api_key.setMaximumSize(QtCore.QSize(16777215, 24))
        self.lineEdit_api_key.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.lineEdit_api_key.setObjectName("lineEdit_api_key")
        self.gridLayout_14.addWidget(self.lineEdit_api_key, 0, 1, 1, 1)
        self.gridLayout_23.addWidget(self.frame_6, 1, 0, 1, 1)
        self.frame_20 = QtWidgets.QFrame(self.frame_api_inp_fields)
        self.frame_20.setMinimumSize(QtCore.QSize(0, 70))
        self.frame_20.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_20.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_20.setObjectName("frame_20")
        self.gridLayout_15 = QtWidgets.QGridLayout(self.frame_20)
        self.gridLayout_15.setContentsMargins(-1, 5, -1, 5)
        self.gridLayout_15.setVerticalSpacing(2)
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.label_2 = QtWidgets.QLabel(self.frame_20)
        self.label_2.setMinimumSize(QtCore.QSize(150, 0))
        self.label_2.setObjectName("label_2")
        self.gridLayout_15.addWidget(self.label_2, 0, 0, 1, 1)
        self.lineEdit_api_secret = QtWidgets.QLineEdit(self.frame_20)
        self.lineEdit_api_secret.setMinimumSize(QtCore.QSize(0, 22))
        self.lineEdit_api_secret.setMaximumSize(QtCore.QSize(16777215, 24))
        self.lineEdit_api_secret.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.lineEdit_api_secret.setObjectName("lineEdit_api_secret")
        self.gridLayout_15.addWidget(self.lineEdit_api_secret, 0, 1, 1, 1)
        self.gridLayout_23.addWidget(self.frame_20, 2, 0, 1, 1)
        self.frame_21 = QtWidgets.QFrame(self.frame_api_inp_fields)
        self.frame_21.setMinimumSize(QtCore.QSize(0, 70))
        self.frame_21.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_21.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_21.setObjectName("frame_21")
        self.gridLayout_16 = QtWidgets.QGridLayout(self.frame_21)
        self.gridLayout_16.setContentsMargins(-1, 5, -1, 5)
        self.gridLayout_16.setVerticalSpacing(2)
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.label_3 = QtWidgets.QLabel(self.frame_21)
        self.label_3.setMinimumSize(QtCore.QSize(150, 0))
        self.label_3.setObjectName("label_3")
        self.gridLayout_16.addWidget(self.label_3, 0, 0, 1, 1)
        self.lineEdit_account_userName = QtWidgets.QLineEdit(self.frame_21)
        self.lineEdit_account_userName.setMinimumSize(QtCore.QSize(0, 22))
        self.lineEdit_account_userName.setMaximumSize(QtCore.QSize(16777215, 24))
        self.lineEdit_account_userName.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.lineEdit_account_userName.setObjectName("lineEdit_account_userName")
        self.gridLayout_16.addWidget(self.lineEdit_account_userName, 0, 1, 1, 1)
        self.gridLayout_23.addWidget(self.frame_21, 3, 0, 1, 1)
        self.frame_22 = QtWidgets.QFrame(self.frame_api_inp_fields)
        self.frame_22.setMinimumSize(QtCore.QSize(0, 70))
        self.frame_22.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_22.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_22.setObjectName("frame_22")
        self.gridLayout_17 = QtWidgets.QGridLayout(self.frame_22)
        self.gridLayout_17.setContentsMargins(-1, 5, -1, 5)
        self.gridLayout_17.setVerticalSpacing(2)
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.label_4 = QtWidgets.QLabel(self.frame_22)
        self.label_4.setMinimumSize(QtCore.QSize(150, 0))
        self.label_4.setObjectName("label_4")
        self.gridLayout_17.addWidget(self.label_4, 0, 0, 1, 1)
        self.lineEdit_account_password = QtWidgets.QLineEdit(self.frame_22)
        self.lineEdit_account_password.setMinimumSize(QtCore.QSize(0, 22))
        self.lineEdit_account_password.setMaximumSize(QtCore.QSize(16777215, 24))
        self.lineEdit_account_password.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.lineEdit_account_password.setObjectName("lineEdit_account_password")
        self.gridLayout_17.addWidget(self.lineEdit_account_password, 0, 1, 1, 1)
        self.gridLayout_23.addWidget(self.frame_22, 4, 0, 1, 1)
        self.frame_23 = QtWidgets.QFrame(self.frame_api_inp_fields)
        self.frame_23.setMinimumSize(QtCore.QSize(0, 70))
        self.frame_23.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_23.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_23.setObjectName("frame_23")
        self.gridLayout_18 = QtWidgets.QGridLayout(self.frame_23)
        self.gridLayout_18.setContentsMargins(-1, 5, -1, 5)
        self.gridLayout_18.setVerticalSpacing(2)
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.label_5 = QtWidgets.QLabel(self.frame_23)
        self.label_5.setMinimumSize(QtCore.QSize(150, 0))
        self.label_5.setObjectName("label_5")
        self.gridLayout_18.addWidget(self.label_5, 0, 0, 1, 1)
        self.lineEdit_account_sec_pin = QtWidgets.QLineEdit(self.frame_23)
        self.lineEdit_account_sec_pin.setMinimumSize(QtCore.QSize(0, 22))
        self.lineEdit_account_sec_pin.setMaximumSize(QtCore.QSize(16777215, 24))
        self.lineEdit_account_sec_pin.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.lineEdit_account_sec_pin.setObjectName("lineEdit_account_sec_pin")
        self.gridLayout_18.addWidget(self.lineEdit_account_sec_pin, 0, 1, 1, 1)
        self.gridLayout_23.addWidget(self.frame_23, 5, 0, 1, 1)
        self.frame_24 = QtWidgets.QFrame(self.frame_api_inp_fields)
        self.frame_24.setMinimumSize(QtCore.QSize(0, 70))
        self.frame_24.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_24.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_24.setObjectName("frame_24")
        self.gridLayout_19 = QtWidgets.QGridLayout(self.frame_24)
        self.gridLayout_19.setContentsMargins(-1, 5, -1, 5)
        self.gridLayout_19.setVerticalSpacing(2)
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.label_6 = QtWidgets.QLabel(self.frame_24)
        self.label_6.setMinimumSize(QtCore.QSize(150, 0))
        self.label_6.setObjectName("label_6")
        self.gridLayout_19.addWidget(self.label_6, 0, 0, 1, 1)
        self.lineEdit_totp_secret = QtWidgets.QLineEdit(self.frame_24)
        self.lineEdit_totp_secret.setMinimumSize(QtCore.QSize(0, 22))
        self.lineEdit_totp_secret.setMaximumSize(QtCore.QSize(16777215, 24))
        self.lineEdit_totp_secret.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.lineEdit_totp_secret.setObjectName("lineEdit_totp_secret")
        self.gridLayout_19.addWidget(self.lineEdit_totp_secret, 0, 1, 1, 1)
        self.gridLayout_23.addWidget(self.frame_24, 6, 0, 1, 1)
        self.gridLayout_20.addWidget(self.frame_api_inp_fields, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.frame_api_details_inp, 1, 0, 1, 1)
        self.frame_logo = QtWidgets.QFrame(self.frame_bg_gradient_frame)
        self.frame_logo.setMinimumSize(QtCore.QSize(430, 0))
        self.frame_logo.setStyleSheet("#frame_logo{\n"
                                      "    border: 5px solid transparent;\n"
                                      "    border-radius: 10px;\n"
                                      "}")
        self.frame_logo.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_logo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_logo.setObjectName("frame_logo")
        self.gridLayout_21 = QtWidgets.QGridLayout(self.frame_logo)
        self.gridLayout_21.setObjectName("gridLayout_21")
        self.gridLayout_5.addWidget(self.frame_logo, 1, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.frame_bg_gradient_frame)
        font = QtGui.QFont()
        font.setFamily("URW Bookman [urw]")
        font.setPointSize(19)
        font.setBold(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_5.addWidget(self.label_8, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.frame_bg_gradient_frame, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "TrendMyFriend - API Details Window"))
        self.pushButton_submit_api_details.setText(_translate("Dialog", "Submit"))
        self.pushButton_edit_api_details.setText(_translate("Dialog", "Edit"))
        self.label_7.setText(_translate("Dialog", "Stock Broker Name"))
        self.label.setText(_translate("Dialog", "API Key"))
        self.label_2.setText(_translate("Dialog", "API Secret"))
        self.label_3.setText(_translate("Dialog", "Account User Name"))
        self.label_4.setText(_translate("Dialog", "Account Password"))
        self.label_5.setText(_translate("Dialog", "Security PIN"))
        self.label_6.setText(_translate("Dialog", "TOTP Secret"))
        self.label_8.setText(_translate("Dialog", "USER API DETAILS"))


from . import icons_rc
