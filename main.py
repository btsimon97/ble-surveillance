import sys
import configparser
import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from menu import Ui_MainWindow
from dotenv import load_dotenv, set_key, find_dotenv


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("BLE Bluetooth Surveillance")
        # load .env for email/phone
        load_dotenv()
        # render zones page since its first and onChange not called yet
        self.loadZones()
        # on page change call onChange
        self.ui.stackedWidget.currentChanged.connect(self.onChange)
        # on zone switch load respective settings
        self.ui.comboBox.currentIndexChanged.connect(self.indexChanged)
        # when selected device changed
        self.ui.listWidget_1.currentItemChanged.connect(self.displayDetails)
        # on tab button click switch to respective tab
        self.ui.btn_page_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_1))
        self.ui.btn_page_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_2))
        self.ui.btn_page_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_3))
        # view unknown devices
        self.ui.pushButton_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_4))
        # go back to known devices
        self.ui.pushButton_4.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_3))
        # make unkown device known
        self.ui.pushButton_3.clicked.connect(self.makeKnown)
        # on save button click save config
        self.ui.save_1.clicked.connect(self.saveZones)
        self.ui.save_2.clicked.connect(self.saveSettings)
        self.show()

    def indexChanged(self, idx):
        # zone name
        zoneConfig = configparser.ConfigParser()
        zoneConfig.read('zones.conf.example')
        # zone / config section name
        section = self.ui.comboBox.currentText()
        # can't rename default zone or set uuid
        if section == "DEFAULT":
            self.ui.lineEdit_1.setEnabled(False)
            self.ui.lineEdit_4.setEnabled(False)
            self.ui.lineEdit_4.clear()
        else:
            self.ui.lineEdit_1.setEnabled(True)
            self.ui.lineEdit_4.setEnabled(True)
            # create new section if user just added a zone
            if not zoneConfig.has_section(section):
                zoneConfig.add_section(section.lower())
                zoneConfig.set(section, 'zone_name', section.lower())
                zoneConfig.set(section, 'zone_uuid', 'XXXXXXXX-0000-0000-0000-XXXXXXXXXXXX')
                with open('zones.conf.example', 'w') as configFile:
                    zoneConfig.write(configFile)
            else:  # display uuid
                self.ui.lineEdit_4.setText(zoneConfig.get(section, 'zone_uuid'))
        # display section name
        self.ui.lineEdit_1.setText(section)
        # keep original name as placeholder in case of edit
        self.ui.lineEdit_1.setPlaceholderText(section)
        # alert known
        self.ui.checkBox_1.setChecked(zoneConfig.getboolean(section, 'alert_on_recognized'))
        # alert unknown
        self.ui.checkBox_2.setChecked(zoneConfig.getboolean(section, 'alert_on_unrecognized'))
        # track BTLE
        self.ui.checkBox_3.setChecked(zoneConfig.getboolean(section, 'monitor_btle_devices'))
        # track BT
        self.ui.checkBox_4.setChecked(zoneConfig.getboolean(section, 'monitor_bt_devices'))
        # display notification options
        channels = zoneConfig.get(section, 'notification_channels')
        if channels.find('email') == -1:
            self.ui.checkBox_5.setChecked(False)
        else:
            self.ui.checkBox_5.setChecked(True)
        if channels.find('sms') == -1:
            self.ui.checkBox_6.setChecked(False)
        else:
            self.ui.checkBox_6.setChecked(True)

    def loadZones(self):
        self.ui.comboBox.clear()
        zoneConfig = configparser.ConfigParser()
        zoneConfig.read('zones.conf.example')
        self.ui.comboBox.addItem('DEFAULT')
        self.ui.comboBox.addItems(zoneConfig.sections())
        self.indexChanged(0)

    def loadSettings(self):
        email = os.environ.get('EMAIL_USERNAME')
        self.ui.lineEdit_2.setText(email)
        phone = os.environ.get('TWILIO_PHONE')
        self.ui.lineEdit_3.setText(phone)
        # read config file, add dummy header so configparser works
        config = configparser.ConfigParser()
        with open("kismet_site.conf.example") as stream:
            config.read_string("[top]\n" + stream.read())
        # max devices
        self.ui.spinBox_1.setValue(config.getint('top', 'tracker_max_devices'))
        # timeout
        self.ui.spinBox_2.setValue(config.getint('top', 'tracker_device_timeout'))

    def displayDetails(self):  # details of select device in list
        self.ui.listWidget_2.clear()
        devices = configparser.ConfigParser()
        devices.read('devices.conf.example')
        section = devices.sections()[self.ui.listWidget_1.currentRow()]
        self.ui.listWidget_2.addItem("Device: " + devices.get(section, 'device_name'))
        self.ui.listWidget_2.addItem("MAC address: " + devices.get(section, 'device_macaddr'))

    def displayDevices(self):  # get list of devices and display nicknames that can be selected
        self.ui.listWidget_1.clear()
        devices = configparser.ConfigParser()
        devices.read('devices.conf.example')
        for section in devices.sections():
            self.ui.listWidget_1.addItem(devices.get(section, 'device_nickname'))

    def unknownDevices(self):  # display unknown devices in list
        self.ui.listWidget_3.clear()
        devices = configparser.ConfigParser()
        devices.read('unknown.conf.example')
        for section in devices.sections():
            self.ui.listWidget_3.addItem(devices.get(section, 'device_name')+' | '+devices.get(section, 'device_macaddr'))

    def makeKnown(self):  # make selected device known and remove from unknown
        devices = configparser.ConfigParser()
        devices.read('devices.conf.example')
        unknown = configparser.ConfigParser()
        unknown.read('unknown.conf.example')
        # new nickname
        nickname = self.ui.lineEdit_5.text()
        self.ui.lineEdit_5.clear()
        # if device selected and nickname specified
        if(nickname and self.ui.listWidget_3.currentItem()):
            # selected section
            unknownSection = unknown.sections()[self.ui.listWidget_3.currentRow()]
            # update known device file to include unknown device
            devices.add_section(nickname)
            devices.set(nickname, 'device_nickname', nickname.lower())
            devices.set(nickname, 'device_name', unknown.get(unknownSection, 'device_name'))
            devices.set(nickname, 'device_macaddr', unknown.get(unknownSection, 'device_macaddr'))
            # remove section from unknown
            unknown.remove_section(unknown.sections()[self.ui.listWidget_3.currentRow()])
            # save changes to files
            with open('devices.conf.example', 'w') as configFile:
                    devices.write(configFile)
            with open('unknown.conf.example', 'w') as configFile:
                    unknown.write(configFile)
            # update current unknown device display
            self.unknownDevices()

    def saveZones(self):
        # inputted preferences to save
        currentZone = self.ui.lineEdit_1.text()
        oldZone = self.ui.lineEdit_1.placeholderText()
        alertKnown = self.ui.checkBox_1.isChecked()
        alertUnknown = self.ui.checkBox_2.isChecked()
        trackBle = self.ui.checkBox_3.isChecked()
        trackStandard = self.ui.checkBox_4.isChecked()
        emailNotif = self.ui.checkBox_5.isChecked()
        smsNotif = self.ui.checkBox_6.isChecked()
        uuid = self.ui.lineEdit_4.text()
        # write inputs to zone config file
        zoneConfig = configparser.ConfigParser()
        zoneConfig.read('zones.conf.example')
        # section renamed, update name
        if currentZone != oldZone:
            items = zoneConfig.items(oldZone)
            zoneConfig.add_section(currentZone)
            for item in items:
                zoneConfig.set(currentZone, item[0], item[1])
            zoneConfig.remove_section(oldZone)
        # alert known device
        if zoneConfig.getboolean("DEFAULT", 'alert_on_recognized') != alertKnown:
            zoneConfig.set(currentZone, 'alert_on_recognized', str(alertKnown).lower())
        # alert unkown device
        if zoneConfig.getboolean("DEFAULT", 'alert_on_unrecognized') != alertUnknown:
            zoneConfig.set(currentZone, 'alert_on_unrecognized', str(alertUnknown).lower())
        # track ble
        if zoneConfig.getboolean("DEFAULT", 'monitor_btle_devices') != trackBle:
            zoneConfig.set(currentZone, 'monitor_btle_devices', str(trackBle).lower())
        # track standard bt
        if zoneConfig.getboolean("DEFAULT", 'monitor_bt_devices') != trackStandard:
            zoneConfig.set(currentZone, 'monitor_bt_devices', str(trackStandard).lower())
        # notification settings
        channels = []
        if emailNotif:
            channels.append("email")
        if smsNotif:
            channels.append("sms")
        zoneConfig.set(currentZone, 'notification_channels', str(channels).replace("'", "\""))
        # uuid
        if currentZone != "DEFAULT":
            zoneConfig.set(currentZone, 'zone_uuid', uuid)
        # save changes
        with open('zones.conf.example', 'w') as configFile:
                    zoneConfig.write(configFile)
        print("Zones saved")

    def saveSettings(self):
        # inputted preferences to save
        email = self.ui.lineEdit_2.text()
        phone = self.ui.lineEdit_3.text()
        maxDevices = self.ui.spinBox_1.value()
        devTimeout = self.ui.spinBox_2.value()
        # write inputs to settings config file (phone needs error handling)
        os.environ['EMAIL_USERNAME'] = email
        os.environ['TWILIO_PHONE'] = phone
        set_key(find_dotenv(), 'EMAIL_USERNAME', email)
        set_key(find_dotenv(), 'TWILIO_PHONE', phone)

        # read and then write over kismet settings, replacing with new info
        with open("kismet_site.conf.example", "r+") as stream:
            kismetConfig = stream.read()
            stream.seek(0)
            # device timeout
            timeoutIdx = kismetConfig.index("tracker_d")+23
            kismetConfig = kismetConfig[:timeoutIdx] + str(devTimeout) + kismetConfig[kismetConfig.index('\n', timeoutIdx):]
            # max devices
            maxdevIdx = kismetConfig.index("tracker_m")+20
            kismetConfig = kismetConfig[:maxdevIdx] + str(maxDevices) + kismetConfig[kismetConfig.index('\n', maxdevIdx):]
            # update config file
            stream.write(kismetConfig)
            stream.truncate()

        print("Settings saved")

    def onChange(self, index):
        # update the current page
        if(index == 0):
            self.indexChanged(0)  # load zone
        elif(index == 1):
            self.loadSettings()
        elif(index == 2):
            self.displayDevices()
        elif(index == 3):
            self.unknownDevices()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
