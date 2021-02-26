from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from menu import Ui_MainWindow
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("BLE Bluetooth Surveillance")
        # render zones page
        ### copy code from index == 0 onChange ###
        # on page change call onChange
        self.ui.stackedWidget.currentChanged.connect(self.onChange)
        # on tab button click switch to respective tab
        self.ui.btn_page_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_1))
        self.ui.btn_page_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_2))
        self.ui.btn_page_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_3))
        # on save button click save config
        self.ui.save_1.clicked.connect(self.saveZones)
        self.ui.save_2.clicked.connect(self.saveSettings)
        self.show()
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
        #
        print("Zones saved")
    def saveSettings(self):
        # inputted preferences to save
        email = self.ui.lineEdit_2.text()
        phone = self.ui.lineEdit_3.text()
        maxDevices = self.ui.spinBox_1.value()
        devTimeout = self.ui.spinBox_2.value()
        # write inputs to settings config file (phone needs error handling)
        #
        print("Settings saved")
    def onChange(self,index):
        # update the new page
        if(index == 0):
            print("on page 1")
            #loadZones()
        elif(index == 1):
            print("on page 2")
            #loadSettings()
        elif(index == 2):
            print("on page 3")
            #displayDevices()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())