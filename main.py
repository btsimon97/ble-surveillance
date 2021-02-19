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
        # save zones config
        print("Zones saved")
    def saveSettings(self):
        # save settings config
        print("Settings saved")
    def onChange(self,index):
        # update the new page
        if(index == 0):
            print("on page 1")
        elif(index == 1):
            print("on page 2")
        elif(index == 2):
            print("on page 3")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())