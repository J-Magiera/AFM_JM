import sys
import serial

from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QFileDialog
)
from PyQt5 import QtWidgets, QtCore

import AFM_Dialog, AFM_Graph


# Subclass QMainWindow to customise your application's main window
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ser = serial.Serial(None, 115200, timeout=0)
        self.setWindowTitle("AFM app")
        self.graphWidget = AFM_Graph.GraphWindow()

        Vlayout = QVBoxLayout()
        Hlayout = QHBoxLayout()

        self.z = []
        self.x = []
        self.y = []
        self.data_stream = []


        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.readArd)
        
        self.button_calibrate = QtWidgets.QPushButton(
            text="Calibrate",
            enabled=False,
            clicked=lambda: self.onChar(1)
            # checkable=True,
            # toggled = self.onMyToolBarButtonClick
        )
        
        self.button_R = QtWidgets.QPushButton(
            text="Show",
            #enabled = False,
            clicked=self.updatePlotData
            # checkable=True,
        )
        self.button_read = QtWidgets.QPushButton(
            text="Read",
            enabled=False,
            clicked=self.onRead
        )

        self.button_Test = QtWidgets.QPushButton(
            text="Test",
            enabled=False,
            clicked=lambda x: self.onChar(8)
        )

        self.button_save = QtWidgets.QPushButton(
            text="Save",
            enabled = True,
            clicked=self.saveMeasurement
        )
        
        self.button_load= QtWidgets.QPushButton(
            text="Load",
            enabled = True,
            clicked=self.loadMeasurement
        )

        self.button_connect = QtWidgets.QPushButton(
           text="Connect",
           enabled = True,
           checkable = True,
           clicked = self.connectUART
        )

        #Vlayout
        Hlayout.addWidget(self.button_calibrate)
        Hlayout.addWidget(self.button_read)
        Hlayout.addWidget(self.button_Test)
        Hlayout.addWidget(self.button_R)
        Hlayout.addWidget(self.button_save)
        Hlayout.addWidget(self.button_load)
        Hlayout.addWidget(self.button_connect)
        #hLaout
        Vlayout.addLayout(Hlayout)
        Vlayout.addWidget(self.graphWidget)
        widget = QtWidgets.QWidget()
        widget.setLayout(Vlayout)
        self.setCentralWidget(widget)

    def readArd(self):
        while self.ser.read_until():
            self.data_stream = self.ser.readline()
            self.ser.write(b'6')
            print(self.data_stream)
            if self.data_stream != b'':
                self.operate()
            

    def operate(self):
        self.data_stream = self.data_stream.decode()
        self.data_stream = self.data_stream.split(" ")
        self.data_stream.pop(-1)
        print(self.data_stream)
        self.x.append(self.data_stream[0])
        self.y.append(self.data_stream[1])
        self.z.append(self.data_stream[2])
       
     

    def onRead(self):
        self.ser.flushInput()
        self.ser.write(b'0')
        self.timer.start()

    def updatePlotData(self):
     #   print(self.x)
      #  print(len(self.x))
       # print(self.y)
       # print(len(self.y))
        #print(self.z)
        #print(len(self.z))
        x = []
        y = []
        z = []
        for item in self.x:
            x.append(float(item))
        for item in self.y:
            y.append(float(item))
        for item in self.z:
            z.append(float(item))

        self.graphWidget.DrawGraph(x, y, z)

    def onChar(self, c):
        self.ser.write(bytes(str(c), encoding="ascii"))

    def saveMeasurement(self):
        dlg = AFM_Dialog.saveDialog(self)
        dlg.x1 = self.x
        dlg.y1 = self.y
        dlg.z1 = self.z
        self.dlg.exec_()
    
    def loadMeasurement(self):
        dlg = AFM_Dialog.loadDialog(self)
        dlg.exec_()
        self.x = dlg.x1
        self.y = dlg.y1
        self.z = dlg.z1
        print(self.x)
        print(self.y)
        print(self.z)
        
    def connectUART(self, s):
        if s and not (self.ser.isOpen()):
            try:
                self.ser.port = '/dev/ttyUSB0'
                self.ser.open()
                self.button_connect.setChecked(True)
                self.enableButtons()
            except:
                self.button_connect.setChecked(False)
                print("Error #0001")
        else:
            try:
                self.ser.close()
                self.button_connect.setChecked(False)
                self.disableButtons()
            except:
                self.button_connect.setChecked(True)
                print("Error #0002")
                    

    def enableButtons(self):
        self.button_calibrate.setEnabled(True)
        self.button_read.setEnabled(True)
        self.button_Test.setEnabled(True)
        
    def disableButtons(self):
        self.button_calibrate.setEnabled(False)
        self.button_read.setEnabled(False)
        self.button_Test.setEnabled(False)


app = QApplication(sys.argv)
app.setStyle('Breeze')
window = MainWindow()
window.show()

app.exec_()
