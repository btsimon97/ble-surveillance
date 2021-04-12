import sys
import configparser
import os
import argparse

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from menu import Ui_MainWindow


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config-file", type=str,
                    help="Specify the bluemon config file to use. Default is /etc/bluemon/bluemon.conf",
                    default="/etc/bluemon/bluemon.conf")
parser.add_argument("-n", "--notification-file", type=str,
                    help="Specify the notification config file to use. Default is /etc/bluemon/notifications.conf",
                    default="/etc/bluemon/notifications.conf")
parser.add_argument("-d", "--device-file", type=str,
                    help="Specify the file with the list of known devices to use. Default is /etc/bluemon/devices.conf",
                    default="/etc/bluemon/devices.conf")
parser.add_argument("-u", "--unknown-file", type=str,
                    help="Specify the file with the list of unknown devices to use. Default is /etc/bluemon/unknown.conf",
                    default="/etc/bluemon/unknown.conf")
parser.add_argument("-z", "--zone-file", type=str,
                    help="Specify the file with the list of zones to use. Default is /etc/bluemon/zones.conf",
                    default="/etc/bluemon/zones.conf")
args = parser.parse_args()
SITE_PATH = "/etc/kismet/kismet_site.conf"

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("BLE Bluetooth Surveillance")
        # render zones page since its first and onChange not called yet
        self.loadZones()
        # on page change call onChange
        self.ui.stackedWidget.currentChanged.connect(self.onChange)
        # on zone switch load respective settings
        self.ui.zones_dropdown.currentIndexChanged.connect(self.indexChanged)
        # when selected device changed
        self.ui.listWidget_1.currentItemChanged.connect(self.displayDetails)
        # on tab button click switch to respective tab
        self.ui.zones_tab.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_1))
        self.ui.settings_tab.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_2))
        self.ui.devices_tab.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_3))
        # go to smtp settings
        self.ui.smtp_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_5))
        # go back to settings
        self.ui.settings_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_2))
        # view unknown devices
        self.ui.unknown_dev.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_4))
        # go back to known devices
        self.ui.known_dev.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_3))
        # make unkown device known
        self.ui.make_known.clicked.connect(self.makeKnown)
        # on save button click save config
        self.ui.save_1.clicked.connect(self.saveZones)
        self.ui.save_2.clicked.connect(self.saveSettings)
        self.ui.save_3.clicked.connect(self.saveSmtp)
        self.show()

    def indexChanged(self, idx):
        # zone name
        zoneConfig = configparser.ConfigParser()
        zoneConfig.read(args.zone_file)
        # zone / config section name
        section = self.ui.zones_dropdown.currentText()
        # can't rename default zone or set uuid
        if section == "DEFAULT":
            self.ui.zone_edit.setEnabled(False)
            self.ui.uuid_edit.setEnabled(False)
            self.ui.uuid_edit.clear()
        else:
            self.ui.zone_edit.setEnabled(True)
            self.ui.uuid_edit.setEnabled(True)
            # create new section if user just added a zone
            if not zoneConfig.has_section(section):
                zoneConfig.add_section(section.lower())
                zoneConfig.set(section, 'zone_name', section.lower())
                zoneConfig.set(section, 'zone_uuid', 'XXXXXXXX-0000-0000-0000-XXXXXXXXXXXX')
                with open(args.zone_file, 'w') as configFile:
                    zoneConfig.write(configFile)
            else:  # display uuid
                self.ui.uuid_edit.setText(zoneConfig.get(section, 'zone_uuid'))
        # display section name
        self.ui.zone_edit.setText(section)
        # keep original name as placeholder in case of edit
        self.ui.zone_edit.setPlaceholderText(section)
        # alert known
        self.ui.known_check.setChecked(zoneConfig.getboolean(section, 'alert_on_recognized'))
        # alert unknown
        self.ui.unknown_check.setChecked(zoneConfig.getboolean(section, 'alert_on_unrecognized'))
        # track BTLE
        self.ui.ble_check.setChecked(zoneConfig.getboolean(section, 'monitor_btle_devices'))
        # track BT
        self.ui.bl_check.setChecked(zoneConfig.getboolean(section, 'monitor_bt_devices'))
        # display notification options
        channels = zoneConfig.get(section, 'notification_channels')
        if channels.find('email') == -1:
            self.ui.email_check.setChecked(False)
        else:
            self.ui.email_check.setChecked(True)
        if channels.find('sms') == -1:
            self.ui.sms_check.setChecked(False)
        else:
            self.ui.sms_check.setChecked(True)
        emailList = zoneConfig.get(section, 'email_recipients')
        smsList = zoneConfig.get(section,'sms_recipients')
        strippedEmail = ''.join( c for c in emailList if  c not in '[]" ')
        strippedSms = ''.join( c for c in smsList if  c not in '[]" ')
        self.ui.erecipt_edit.setText(strippedEmail)
        self.ui.srecipt_edit.setText(strippedSms)

    def loadZones(self):
        self.ui.zones_dropdown.clear()
        zoneConfig = configparser.ConfigParser()
        zoneConfig.read(args.zone_file)
        self.ui.zones_dropdown.addItem('DEFAULT')
        self.ui.zones_dropdown.addItems(zoneConfig.sections())
        self.indexChanged(0)

    def loadSettings(self):
        settingsConfig = configparser.ConfigParser()
        settingsConfig.read(args.notification_file)
        email = settingsConfig.get('email', 'email_address')
        subject = settingsConfig.get('email', 'email_subject')
        phone = settingsConfig.get('sms', 'sender_phone_number')
        sid = settingsConfig.get('sms', 'twilio_account_sid')
        token = settingsConfig.get('sms', 'twilio_auth_token')
        self.ui.email_edit.setText(email)
        self.ui.subject_edit.setText(subject)
        self.ui.phone_edit.setText(phone)
        self.ui.sid_edit.setText(sid)
        self.ui.token_edit.setText(token)
        kismetConfig = configparser.ConfigParser()
        kismetConfig.read(SITE_PATH)
        # max devices
        self.ui.maxdev_spin.setValue(kismetConfig.getint('DEFAULT', 'tracker_max_devices'))
        # timeout
        self.ui.timeout_spin.setValue(kismetConfig.getint('DEFAULT', 'tracker_device_timeout'))

    def displayDetails(self):  # details of select device in list
        self.ui.listWidget_2.clear()
        devices = configparser.ConfigParser()
        devices.read(args.device_file)
        section = devices.sections()[self.ui.listWidget_1.currentRow()]
        self.ui.listWidget_2.addItem("Device: " + devices.get(section, 'device_name'))
        self.ui.listWidget_2.addItem("MAC address: " + devices.get(section, 'device_macaddr'))

    def displayDevices(self):  # get list of devices and display nicknames that can be selected
        self.ui.listWidget_1.clear()
        devices = configparser.ConfigParser()
        devices.read(args.device_file)
        for section in devices.sections():
            self.ui.listWidget_1.addItem(devices.get(section, 'device_nickname'))

    def unknownDevices(self):  # display unknown devices in list
        self.ui.listWidget_3.clear()
        devices = configparser.ConfigParser()
        devices.read(args.unknown_file)
        for section in devices.sections():
            self.ui.listWidget_3.addItem(devices.get(section, 'device_name')+' | '+devices.get(section, 'device_macaddr'))

    def makeKnown(self):  # make selected device known and remove from unknown
        devices = configparser.ConfigParser()
        devices.read(args.device_file)
        unknown = configparser.ConfigParser()
        unknown.read(args.unknown_file)
        # new nickname
        nickname = self.ui.nickname_edit.text()
        self.ui.nickname_edit.clear()
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
            with open(args.device_file, 'w') as configFile:
                    devices.write(configFile)
            with open(args.unknown_file, 'w') as configFile:
                    unknown.write(configFile)
            # update current unknown device display
            self.unknownDevices()

    def saveZones(self):
        # inputted preferences to save
        currentZone = self.ui.zone_edit.text()
        oldZone = self.ui.zone_edit.placeholderText()
        alertKnown = self.ui.known_check.isChecked()
        alertUnknown = self.ui.unknown_check.isChecked()
        trackBle = self.ui.ble_check.isChecked()
        trackStandard = self.ui.bl_check.isChecked()
        emailNotif = self.ui.email_check.isChecked()
        smsNotif = self.ui.sms_check.isChecked()
        uuid = self.ui.uuid_edit.text()
        emailRecip = self.ui.erecipt_edit.text().split(',')
        smsRecip = self.ui.srecipt_edit.text().split(',')
        # write inputs to zone config file
        zoneConfig = configparser.ConfigParser()
        zoneConfig.read(args.zone_file)
        # section renamed, update name
        if currentZone != oldZone:
            self.ui.zone_edit.setPlaceholderText(currentZone)
            items = zoneConfig.items(oldZone)
            zoneConfig.add_section(currentZone)
            for item in items:
                zoneConfig.set(currentZone, item[0], item[1])
            zoneConfig.set(currentZone,'zone_name',currentZone.lower())
            zoneConfig.remove_section(oldZone)
            self.ui.zones_dropdown.setItemText(self.ui.zones_dropdown.currentIndex(),currentZone)
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
        zoneConfig.set(currentZone, 'email_recipients', str(emailRecip).replace("'", "\""))
        zoneConfig.set(currentZone, 'sms_recipients', str(smsRecip).replace("'", "\""))
        # uuid
        if currentZone != "DEFAULT":
            zoneConfig.set(currentZone, 'zone_uuid', uuid)
        # save changes
        with open(args.zone_file, 'w') as configFile:
            zoneConfig.write(configFile)

    def saveSettings(self):
        settingsConfig = configparser.ConfigParser()
        settingsConfig.read(args.notification_file)
        # inputted preferences to save
        email = self.ui.email_edit.text()
        subject = self.ui.subject_edit.text()
        phone = self.ui.phone_edit.text()
        sid = self.ui.sid_edit.text()
        token = self.ui.token_edit.text()
        maxDevices = self.ui.maxdev_spin.value()
        devTimeout = self.ui.timeout_spin.value()
        # write inputs to settings config file
        settingsConfig.set('email','email_address', email)
        settingsConfig.set('email','email_subject', subject)
        settingsConfig.set('sms','twilio_account_sid', sid)
        settingsConfig.set('sms','twilio_auth_token', token)
        settingsConfig.set('sms','sender_phone_number', phone)
        with open(args.notification_file, 'w') as configFile:
            settingsConfig.write(configFile)
        # write inputs to kismet config file
        kismetConfig = configparser.ConfigParser()
        kismetConfig.read(SITE_PATH)
        kismetConfig.set('DEFAULT', 'tracker_device_timeout', str(devTimeout))
        kismetConfig.set('DEFAULT', 'tracker_max_devices', str(maxDevices))
        with open(SITE_PATH, 'w') as configFile:
            kismetConfig.write(configFile)

    def loadSmtp(self):
        settingsConfig = configparser.ConfigParser()
        settingsConfig.read(args.notification_file)
        servername = settingsConfig.get('email', 'smtp_servername')
        port = settingsConfig.getint('email', 'smtp_portnumber')
        auth = settingsConfig.getboolean('email', 'smtp_authentication_required')
        self.ui.method_dropdown.clear()
        self.ui.method_dropdown.addItem("plain")
        self.ui.method_dropdown.addItem("STARTTLS")
        self.ui.method_dropdown.addItem("SSL")
        self.ui.method_dropdown.setCurrentIndex(0)
        username = settingsConfig.get('email', 'smtp_username')
        pasw = settingsConfig.get('email', 'smtp_password')
        self.ui.server_edit.setText(servername)
        self.ui.port_spin.setValue(port)
        self.ui.auth_check.setChecked(auth)
        self.ui.username_edit.setText(username)
        self.ui.pass_edit.setText(pasw)

    def saveSmtp(self):
        settingsConfig = configparser.ConfigParser()
        settingsConfig.read(args.notification_file)
        servername = self.ui.server_edit.text()
        port = self.ui.port_spin.value()
        method = self.ui.method_dropdown.currentText()
        auth = self.ui.auth_check.isChecked()
        user = self.ui.username_edit.text()
        passwd = self.ui.pass_edit.text()

        # write inputs to settings config file
        settingsConfig.set('email', 'smtp_servername', servername)
        settingsConfig.set('email', 'smtp_portnumber', str(port))
        settingsConfig.set('email', 'smtp_connection_method', method)
        settingsConfig.set('email', 'smtp_authentication_required', str(auth).lower())
        settingsConfig.set('email', 'smtp_username', user)
        settingsConfig.set('email', 'smtp_password', passwd)

        with open(args.notification_file, 'w') as configFile:
            settingsConfig.write(configFile)
        
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
        elif(index == 4):
            self.loadSmtp()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
