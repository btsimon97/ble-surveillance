# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'blue_menu.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 500)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 500))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("bt_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("background-color: rgb(45, 45, 45);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Content = QtWidgets.QFrame(self.centralwidget)
        self.Content.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Content.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Content.setObjectName("Content")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.Content)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_left_menu = QtWidgets.QFrame(self.Content)
        self.frame_left_menu.setMinimumSize(QtCore.QSize(70, 0))
        self.frame_left_menu.setMaximumSize(QtCore.QSize(70, 16777215))
        self.frame_left_menu.setStyleSheet("background-color: rgb(35, 35, 35);")
        self.frame_left_menu.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_left_menu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_left_menu.setObjectName("frame_left_menu")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_left_menu)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_top_menus = QtWidgets.QFrame(self.frame_left_menu)
        self.frame_top_menus.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_top_menus.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_top_menus.setObjectName("frame_top_menus")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_top_menus)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.zones_tab = QtWidgets.QPushButton(self.frame_top_menus)
        self.zones_tab.setMinimumSize(QtCore.QSize(0, 40))
        self.zones_tab.setStyleSheet("QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(35, 35, 35);\n"
"    border: 0px solid;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.zones_tab.setObjectName("zones_tab")
        self.verticalLayout_4.addWidget(self.zones_tab)
        self.settings_tab = QtWidgets.QPushButton(self.frame_top_menus)
        self.settings_tab.setMinimumSize(QtCore.QSize(0, 40))
        self.settings_tab.setStyleSheet("QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(35, 35, 35);\n"
"    border: 0px solid;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.settings_tab.setObjectName("settings_tab")
        self.verticalLayout_4.addWidget(self.settings_tab)
        self.devices_tab = QtWidgets.QPushButton(self.frame_top_menus)
        self.devices_tab.setMinimumSize(QtCore.QSize(0, 40))
        self.devices_tab.setStyleSheet("QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(35, 35, 35);\n"
"    border: 0px solid;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.devices_tab.setObjectName("devices_tab")
        self.verticalLayout_4.addWidget(self.devices_tab)
        self.verticalLayout_3.addWidget(self.frame_top_menus, 0, QtCore.Qt.AlignTop)
        self.horizontalLayout_2.addWidget(self.frame_left_menu)
        self.frame_pages = QtWidgets.QFrame(self.Content)
        self.frame_pages.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_pages.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_pages.setObjectName("frame_pages")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_pages)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.stackedWidget = QtWidgets.QStackedWidget(self.frame_pages)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setObjectName("page_1")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.page_1)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.zone_label = QtWidgets.QLabel(self.page_1)
        self.zone_label.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zone_label.sizePolicy().hasHeightForWidth())
        self.zone_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(28)
        self.zone_label.setFont(font)
        self.zone_label.setStyleSheet("color: #FFF;")
        self.zone_label.setAlignment(QtCore.Qt.AlignCenter)
        self.zone_label.setObjectName("zone_label")
        self.verticalLayout_7.addWidget(self.zone_label)
        self.zones_dropdown = QtWidgets.QComboBox(self.page_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zones_dropdown.sizePolicy().hasHeightForWidth())
        self.zones_dropdown.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.zones_dropdown.setFont(font)
        self.zones_dropdown.setStyleSheet("color: #FFF;")
        self.zones_dropdown.setEditable(True)
        self.zones_dropdown.setCurrentText("")
        self.zones_dropdown.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.zones_dropdown.setPlaceholderText("")
        self.zones_dropdown.setObjectName("zones_dropdown")
        self.verticalLayout_7.addWidget(self.zones_dropdown, 0, QtCore.Qt.AlignHCenter)
        self.zone_edit = QtWidgets.QLineEdit(self.page_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zone_edit.sizePolicy().hasHeightForWidth())
        self.zone_edit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.zone_edit.setFont(font)
        self.zone_edit.setStyleSheet("color: #FFF;")
        self.zone_edit.setText("")
        self.zone_edit.setObjectName("zone_edit")
        self.verticalLayout_7.addWidget(self.zone_edit, 0, QtCore.Qt.AlignHCenter)
        self.known_check = QtWidgets.QCheckBox(self.page_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.known_check.sizePolicy().hasHeightForWidth())
        self.known_check.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.known_check.setFont(font)
        self.known_check.setStyleSheet("color: #FFF;")
        self.known_check.setChecked(True)
        self.known_check.setTristate(False)
        self.known_check.setObjectName("known_check")
        self.verticalLayout_7.addWidget(self.known_check, 0, QtCore.Qt.AlignHCenter)
        self.unknown_check = QtWidgets.QCheckBox(self.page_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.unknown_check.sizePolicy().hasHeightForWidth())
        self.unknown_check.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.unknown_check.setFont(font)
        self.unknown_check.setStyleSheet("color: #FFF;")
        self.unknown_check.setChecked(True)
        self.unknown_check.setTristate(False)
        self.unknown_check.setObjectName("unknown_check")
        self.verticalLayout_7.addWidget(self.unknown_check, 0, QtCore.Qt.AlignHCenter)
        self.ble_check = QtWidgets.QCheckBox(self.page_1)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ble_check.setFont(font)
        self.ble_check.setStyleSheet("color: #FFF;")
        self.ble_check.setChecked(True)
        self.ble_check.setObjectName("ble_check")
        self.verticalLayout_7.addWidget(self.ble_check, 0, QtCore.Qt.AlignHCenter)
        self.bl_check = QtWidgets.QCheckBox(self.page_1)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.bl_check.setFont(font)
        self.bl_check.setStyleSheet("color: #FFF;")
        self.bl_check.setChecked(True)
        self.bl_check.setObjectName("bl_check")
        self.verticalLayout_7.addWidget(self.bl_check, 0, QtCore.Qt.AlignHCenter)
        self.email_check = QtWidgets.QCheckBox(self.page_1)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.email_check.setFont(font)
        self.email_check.setStyleSheet("color: #FFF;")
        self.email_check.setChecked(True)
        self.email_check.setObjectName("email_check")
        self.verticalLayout_7.addWidget(self.email_check, 0, QtCore.Qt.AlignHCenter)
        self.sms_check = QtWidgets.QCheckBox(self.page_1)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sms_check.setFont(font)
        self.sms_check.setStyleSheet("color: #FFF;")
        self.sms_check.setChecked(True)
        self.sms_check.setObjectName("sms_check")
        self.verticalLayout_7.addWidget(self.sms_check, 0, QtCore.Qt.AlignHCenter)
        self.uuid_edit = QtWidgets.QLineEdit(self.page_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uuid_edit.sizePolicy().hasHeightForWidth())
        self.uuid_edit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.uuid_edit.setFont(font)
        self.uuid_edit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.uuid_edit.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.uuid_edit.setStyleSheet("color: #FFF;")
        self.uuid_edit.setObjectName("uuid_edit")
        self.verticalLayout_7.addWidget(self.uuid_edit, 0, QtCore.Qt.AlignHCenter)
        self.save_1 = QtWidgets.QPushButton(self.page_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_1.sizePolicy().hasHeightForWidth())
        self.save_1.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.save_1.setFont(font)
        self.save_1.setStyleSheet("QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(35, 35, 35);\n"
"    border: 0px solid;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.save_1.setIconSize(QtCore.QSize(16, 16))
        self.save_1.setObjectName("save_1")
        self.verticalLayout_7.addWidget(self.save_1)
        self.stackedWidget.addWidget(self.page_1)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.page_2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.settings_label = QtWidgets.QLabel(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settings_label.sizePolicy().hasHeightForWidth())
        self.settings_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(28)
        self.settings_label.setFont(font)
        self.settings_label.setStyleSheet("color: #FFF;")
        self.settings_label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.settings_label.setObjectName("settings_label")
        self.verticalLayout_6.addWidget(self.settings_label, 0, QtCore.Qt.AlignHCenter)
        self.smtp_btn = QtWidgets.QPushButton(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.smtp_btn.sizePolicy().hasHeightForWidth())
        self.smtp_btn.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.smtp_btn.setFont(font)
        self.smtp_btn.setStyleSheet("QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(35, 35, 35);\n"
"    border: 0px solid;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.smtp_btn.setObjectName("smtp_btn")
        self.verticalLayout_6.addWidget(self.smtp_btn, 0, QtCore.Qt.AlignHCenter)
        self.email_edit = QtWidgets.QLineEdit(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.email_edit.sizePolicy().hasHeightForWidth())
        self.email_edit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.email_edit.setFont(font)
        self.email_edit.setStyleSheet("color: #FFF;")
        self.email_edit.setObjectName("email_edit")
        self.verticalLayout_6.addWidget(self.email_edit, 0, QtCore.Qt.AlignHCenter)
        self.subject_edit = QtWidgets.QLineEdit(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subject_edit.sizePolicy().hasHeightForWidth())
        self.subject_edit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.subject_edit.setFont(font)
        self.subject_edit.setStyleSheet("color: #FFF;")
        self.subject_edit.setObjectName("subject_edit")
        self.verticalLayout_6.addWidget(self.subject_edit, 0, QtCore.Qt.AlignHCenter)
        self.phone_edit = QtWidgets.QLineEdit(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.phone_edit.sizePolicy().hasHeightForWidth())
        self.phone_edit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.phone_edit.setFont(font)
        self.phone_edit.setStyleSheet("color: #FFF;")
        self.phone_edit.setInputMask("")
        self.phone_edit.setText("")
        self.phone_edit.setFrame(True)
        self.phone_edit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.phone_edit.setObjectName("phone_edit")
        self.verticalLayout_6.addWidget(self.phone_edit, 0, QtCore.Qt.AlignHCenter)
        self.sid_edit = QtWidgets.QLineEdit(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sid_edit.sizePolicy().hasHeightForWidth())
        self.sid_edit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sid_edit.setFont(font)
        self.sid_edit.setStyleSheet("color: #FFF;")
        self.sid_edit.setText("")
        self.sid_edit.setObjectName("sid_edit")
        self.verticalLayout_6.addWidget(self.sid_edit, 0, QtCore.Qt.AlignHCenter)
        self.token_edit = QtWidgets.QLineEdit(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.token_edit.sizePolicy().hasHeightForWidth())
        self.token_edit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.token_edit.setFont(font)
        self.token_edit.setStyleSheet("color: #FFF;")
        self.token_edit.setObjectName("token_edit")
        self.verticalLayout_6.addWidget(self.token_edit, 0, QtCore.Qt.AlignHCenter)
        self.maxdev_spin = QtWidgets.QSpinBox(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.maxdev_spin.sizePolicy().hasHeightForWidth())
        self.maxdev_spin.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.maxdev_spin.setFont(font)
        self.maxdev_spin.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.maxdev_spin.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.maxdev_spin.setStyleSheet("color: #FFF;")
        self.maxdev_spin.setSpecialValueText("")
        self.maxdev_spin.setSuffix("")
        self.maxdev_spin.setMinimum(1)
        self.maxdev_spin.setMaximum(1000)
        self.maxdev_spin.setSingleStep(10)
        self.maxdev_spin.setObjectName("maxdev_spin")
        self.verticalLayout_6.addWidget(self.maxdev_spin, 0, QtCore.Qt.AlignHCenter)
        self.timeout_spin = QtWidgets.QSpinBox(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timeout_spin.sizePolicy().hasHeightForWidth())
        self.timeout_spin.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.timeout_spin.setFont(font)
        self.timeout_spin.setStyleSheet("color: #FFF;")
        self.timeout_spin.setMinimum(0)
        self.timeout_spin.setMaximum(1000)
        self.timeout_spin.setSingleStep(50)
        self.timeout_spin.setProperty("value", 500)
        self.timeout_spin.setObjectName("timeout_spin")
        self.verticalLayout_6.addWidget(self.timeout_spin, 0, QtCore.Qt.AlignHCenter)
        self.save_2 = QtWidgets.QPushButton(self.page_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.save_2.setFont(font)
        self.save_2.setStyleSheet("QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(35, 35, 35);\n"
"    border: 0px solid;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.save_2.setObjectName("save_2")
        self.verticalLayout_6.addWidget(self.save_2)
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.page_3)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.known_label = QtWidgets.QLabel(self.page_3)
        font = QtGui.QFont()
        font.setPointSize(28)
        self.known_label.setFont(font)
        self.known_label.setStyleSheet("color: #FFF;")
        self.known_label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.known_label.setObjectName("known_label")
        self.verticalLayout_8.addWidget(self.known_label)
        self.listWidget_1 = QtWidgets.QListWidget(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget_1.sizePolicy().hasHeightForWidth())
        self.listWidget_1.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.listWidget_1.setFont(font)
        self.listWidget_1.setStyleSheet("color: #FFF;")
        self.listWidget_1.setObjectName("listWidget_1")
        self.verticalLayout_8.addWidget(self.listWidget_1)
        self.listWidget_2 = QtWidgets.QListWidget(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget_2.sizePolicy().hasHeightForWidth())
        self.listWidget_2.setSizePolicy(sizePolicy)
        self.listWidget_2.setMinimumSize(QtCore.QSize(0, 50))
        self.listWidget_2.setMaximumSize(QtCore.QSize(16777215, 65))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.listWidget_2.setFont(font)
        self.listWidget_2.setStyleSheet("color: #FFF;")
        self.listWidget_2.setObjectName("listWidget_2")
        self.verticalLayout_8.addWidget(self.listWidget_2)
        self.unknown_dev = QtWidgets.QPushButton(self.page_3)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.unknown_dev.setFont(font)
        self.unknown_dev.setStyleSheet("QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(35, 35, 35);\n"
"    border: 0px solid;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.unknown_dev.setObjectName("unknown_dev")
        self.verticalLayout_8.addWidget(self.unknown_dev)
        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.page_4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.unknown_label = QtWidgets.QLabel(self.page_4)
        font = QtGui.QFont()
        font.setPointSize(28)
        self.unknown_label.setFont(font)
        self.unknown_label.setStyleSheet("color: #FFF;")
        self.unknown_label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.unknown_label.setObjectName("unknown_label")
        self.verticalLayout_2.addWidget(self.unknown_label)
        self.listWidget_3 = QtWidgets.QListWidget(self.page_4)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.listWidget_3.setFont(font)
        self.listWidget_3.setStyleSheet("color: #FFF;")
        self.listWidget_3.setObjectName("listWidget_3")
        self.verticalLayout_2.addWidget(self.listWidget_3)
        self.nickname_edit = QtWidgets.QLineEdit(self.page_4)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.nickname_edit.setFont(font)
        self.nickname_edit.setStyleSheet("color: #FFF;")
        self.nickname_edit.setObjectName("nickname_edit")
        self.verticalLayout_2.addWidget(self.nickname_edit)
        self.make_known = QtWidgets.QPushButton(self.page_4)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.make_known.setFont(font)
        self.make_known.setStyleSheet("QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(35, 35, 35);\n"
"    border: 0px solid;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.make_known.setObjectName("make_known")
        self.verticalLayout_2.addWidget(self.make_known)
        self.known_dev = QtWidgets.QPushButton(self.page_4)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.known_dev.setFont(font)
        self.known_dev.setStyleSheet("QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(35, 35, 35);\n"
"    border: 0px solid;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.known_dev.setObjectName("known_dev")
        self.verticalLayout_2.addWidget(self.known_dev)
        self.stackedWidget.addWidget(self.page_4)
        self.page_5 = QtWidgets.QWidget()
        self.page_5.setObjectName("page_5")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.page_5)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.smtp_label = QtWidgets.QLabel(self.page_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.smtp_label.sizePolicy().hasHeightForWidth())
        self.smtp_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(28)
        self.smtp_label.setFont(font)
        self.smtp_label.setStyleSheet("color: #FFF;")
        self.smtp_label.setObjectName("smtp_label")
        self.verticalLayout_10.addWidget(self.smtp_label, 0, QtCore.Qt.AlignHCenter)
        self.server_edit = QtWidgets.QLineEdit(self.page_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.server_edit.sizePolicy().hasHeightForWidth())
        self.server_edit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.server_edit.setFont(font)
        self.server_edit.setStyleSheet("color: #FFF;")
        self.server_edit.setObjectName("server_edit")
        self.verticalLayout_10.addWidget(self.server_edit, 0, QtCore.Qt.AlignHCenter)
        self.port_spin = QtWidgets.QSpinBox(self.page_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.port_spin.sizePolicy().hasHeightForWidth())
        self.port_spin.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.port_spin.setFont(font)
        self.port_spin.setStyleSheet("color: #FFF;")
        self.port_spin.setMaximum(65536)
        self.port_spin.setSingleStep(0)
        self.port_spin.setProperty("value", 25)
        self.port_spin.setObjectName("port_spin")
        self.verticalLayout_10.addWidget(self.port_spin, 0, QtCore.Qt.AlignHCenter)
        self.method_dropdown = QtWidgets.QComboBox(self.page_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.method_dropdown.sizePolicy().hasHeightForWidth())
        self.method_dropdown.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.method_dropdown.setFont(font)
        self.method_dropdown.setStyleSheet("color: #FFF;")
        self.method_dropdown.setObjectName("method_dropdown")
        self.verticalLayout_10.addWidget(self.method_dropdown, 0, QtCore.Qt.AlignHCenter)
        self.auth_check = QtWidgets.QCheckBox(self.page_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.auth_check.sizePolicy().hasHeightForWidth())
        self.auth_check.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.auth_check.setFont(font)
        self.auth_check.setStyleSheet("color: #FFF;")
        self.auth_check.setObjectName("auth_check")
        self.verticalLayout_10.addWidget(self.auth_check, 0, QtCore.Qt.AlignHCenter)
        self.username_edit = QtWidgets.QLineEdit(self.page_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.username_edit.sizePolicy().hasHeightForWidth())
        self.username_edit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.username_edit.setFont(font)
        self.username_edit.setStyleSheet("color: #FFF;")
        self.username_edit.setObjectName("username_edit")
        self.verticalLayout_10.addWidget(self.username_edit, 0, QtCore.Qt.AlignHCenter)
        self.pass_edit = QtWidgets.QLineEdit(self.page_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pass_edit.sizePolicy().hasHeightForWidth())
        self.pass_edit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pass_edit.setFont(font)
        self.pass_edit.setStyleSheet("color: #FFF;")
        self.pass_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pass_edit.setObjectName("pass_edit")
        self.verticalLayout_10.addWidget(self.pass_edit, 0, QtCore.Qt.AlignHCenter)
        self.settings_btn = QtWidgets.QPushButton(self.page_5)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.settings_btn.setFont(font)
        self.settings_btn.setStyleSheet("QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(35, 35, 35);\n"
"    border: 0px solid;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.settings_btn.setObjectName("settings_btn")
        self.verticalLayout_10.addWidget(self.settings_btn)
        self.save_3 = QtWidgets.QPushButton(self.page_5)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.save_3.setFont(font)
        self.save_3.setStyleSheet("QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(35, 35, 35);\n"
"    border: 0px solid;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.save_3.setObjectName("save_3")
        self.verticalLayout_10.addWidget(self.save_3)
        self.stackedWidget.addWidget(self.page_5)
        self.verticalLayout_5.addWidget(self.stackedWidget)
        self.horizontalLayout_2.addWidget(self.frame_pages)
        self.verticalLayout.addWidget(self.Content)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.zones_tab.setText(_translate("MainWindow", "Zones"))
        self.settings_tab.setText(_translate("MainWindow", "Settings"))
        self.devices_tab.setText(_translate("MainWindow", "Devices"))
        self.zone_label.setText(_translate("MainWindow", "Zone Configuration"))
        self.zone_edit.setPlaceholderText(_translate("MainWindow", "Zone Name"))
        self.known_check.setText(_translate("MainWindow", "Alert On Known Device"))
        self.unknown_check.setText(_translate("MainWindow", "Alert On Unknown Device"))
        self.ble_check.setText(_translate("MainWindow", "Track Bluetooth Low Energy"))
        self.bl_check.setText(_translate("MainWindow", "Track Standard Bluetooth Devices"))
        self.email_check.setText(_translate("MainWindow", "Email Notifications"))
        self.sms_check.setText(_translate("MainWindow", "SMS Notifications"))
        self.uuid_edit.setPlaceholderText(_translate("MainWindow", "UUID"))
        self.save_1.setText(_translate("MainWindow", "Save"))
        self.settings_label.setText(_translate("MainWindow", "Settings"))
        self.smtp_btn.setText(_translate("MainWindow", "SMTP Settings"))
        self.email_edit.setPlaceholderText(_translate("MainWindow", "Email"))
        self.subject_edit.setPlaceholderText(_translate("MainWindow", "Email Subject Line"))
        self.phone_edit.setPlaceholderText(_translate("MainWindow", "Phone Number X-X-X"))
        self.sid_edit.setPlaceholderText(_translate("MainWindow", "Twilio Account SID"))
        self.token_edit.setPlaceholderText(_translate("MainWindow", "Twilio Auth Token"))
        self.maxdev_spin.setPrefix(_translate("MainWindow", "Maximum # Of Devices To Track: "))
        self.timeout_spin.setPrefix(_translate("MainWindow", "Tracker Device Timeout: "))
        self.save_2.setText(_translate("MainWindow", "Save"))
        self.known_label.setText(_translate("MainWindow", "Known Devices"))
        self.unknown_dev.setText(_translate("MainWindow", "See Unknown Devices"))
        self.unknown_label.setText(_translate("MainWindow", "Unkown Devices"))
        self.nickname_edit.setPlaceholderText(_translate("MainWindow", "Device Nickname"))
        self.make_known.setText(_translate("MainWindow", "Make Device Known"))
        self.known_dev.setText(_translate("MainWindow", "See Known Devices"))
        self.smtp_label.setText(_translate("MainWindow", "SMTP Settings"))
        self.server_edit.setPlaceholderText(_translate("MainWindow", "SMTP Servername"))
        self.port_spin.setPrefix(_translate("MainWindow", "SMTP Port #: "))
        self.method_dropdown.setPlaceholderText(_translate("MainWindow", "SMTP Connection Method"))
        self.auth_check.setText(_translate("MainWindow", "SMTP Auth Required"))
        self.username_edit.setPlaceholderText(_translate("MainWindow", "SMTP Username"))
        self.pass_edit.setPlaceholderText(_translate("MainWindow", "SMTP Password"))
        self.settings_btn.setText(_translate("MainWindow", "Go Back to Settings"))
        self.save_3.setText(_translate("MainWindow", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
