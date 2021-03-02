import sys, configparser, os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from menu import Ui_MainWindow
from dotenv import load_dotenv,set_key,find_dotenv

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
        # on tab button click switch to respective tab
        self.ui.btn_page_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_1))
        self.ui.btn_page_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_2))
        self.ui.btn_page_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_3))
        # on save button click save config
        self.ui.save_1.clicked.connect(self.saveZones)
        self.ui.save_2.clicked.connect(self.saveSettings)
        self.show()

    def indexChanged(self,idx):
        # zone name
        zoneConfig = configparser.ConfigParser()
        zoneConfig.read('zones.conf.example')
        # zone / config section name
        section = self.ui.comboBox.currentText()
        # can't rename default
        if section == "DEFAULT":
            self.ui.lineEdit_1.setEnabled(False)
        else:
            self.ui.lineEdit_1.setEnabled(True)
            ### NOTE: create new section if user just added a zone, it wouldnt have uuid so do what? ###
            if not zoneConfig.has_section(section):
                zoneConfig.add_section(section)
        # display section name
        self.ui.lineEdit_1.setText(section)
        # keep original name as placeholder in case of edit
        self.ui.lineEdit_1.setPlaceholderText(section)
        # alert known
        self.ui.checkBox_1.setChecked(zoneConfig.getboolean(section,'alert_on_recognized'))
        # alert unknown
        self.ui.checkBox_2.setChecked(zoneConfig.getboolean(section,'alert_on_unrecognized'))
        # track BTLE
        self.ui.checkBox_3.setChecked(zoneConfig.getboolean(section,'monitor_btle_devices'))
        # track BT
        self.ui.checkBox_4.setChecked(zoneConfig.getboolean(section,'monitor_bt_devices'))
        # display notification options
        channels = zoneConfig.get(section,'notification_channels')
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
        self.indexChanged(self.ui.comboBox.currentIndex())

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
        self.ui.spinBox_1.setValue(config.getint('top','tracker_max_devices'))
        # timeout
        self.ui.spinBox_2.setValue(config.getint('top','tracker_device_timeout'))
        

    def displayDevices(self):
        # should this read from devices.conf? what about unknown dev
        # deviceConfig = configparser.ConfigParser()
        # deviceConfig.read('devices.conf.example')
        print('devices displayed')

    def saveZones(self):
        # inputted preferences to save
        zoneName = self.ui.lineEdit_1.text()
        alertKnown = self.ui.checkBox_1.isChecked()
        alertUnkown = self.ui.checkBox_2.isChecked()
        trackBle = self.ui.checkBox_3.isChecked()
        trackStandard = self.ui.checkBox_4.isChecked()
        emailNotif = self.ui.checkBox_5.isChecked()
        smsNotif = self.ui.checkBox_6.isChecked()
        # write inputs to zone config file
        # if zoneName != placeholder text then rename section
        """
        def rename_section(cp, section_from, section_to):

            items = cp.items(section_from)

            cp.add_section(section_to)

            for item in items:
                cp.set(section_to, item[0], item[1])

            cp.remove_section(section_from)
        """
        # make a change, can use deviceConfig.sections(), and can use devicecConfig.get(section, option)
        # deviceConfig.set('phone','device_name','Samsung Galaxy S21')
        # save change
        # with open('devices.conf.example','w') as configFile:
        #   config.write(deviceConfig)
        #
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
        set_key(find_dotenv(),'EMAIL_USERNAME',email)
        set_key(find_dotenv(),'TWILIO_PHONE',phone)

        print("Settings saved")

    def onChange(self,index):
        # update the current page
        if(index == 0):
            print("on zones page")
            self.loadZones()
        elif(index == 1):
            print("on settings page")
            self.loadSettings()
        elif(index == 2):
            print("on display page")
            self.displayDevices()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())