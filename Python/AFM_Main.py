import sys
import serial
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QSlider,
    QProgressBar,
    QLabel,
)
from PyQt5 import QtWidgets, QtCore
import AFM_Dialog, AFM_Graph


# Subclass QMainWindow to customise your application's main window
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ser = serial.Serial(None, 115200, timeout=0)
        self.setWindowTitle("AFM app")
        self.setWindowIcon(QIcon('logo.png'))
        self.graphWidget = AFM_Graph.GraphWindow()

        Vlayout = QVBoxLayout()

        Hlayout = QHBoxLayout()
        Hlayout2 = QHBoxLayout()

        self.z = []
        self.x = []
        self.y = []
        self.data_stream = []

        self.sp = QSlider()
        self.sp.setMaximum(92)
        self.sp.setMinimum(0)
        self.sp.setSingleStep(1)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.readArd)

        self.button_graphX = QtWidgets.QPushButton(
            clicked = lambda: self.setAngle(0, 90),
            icon=QIcon('x.png')
        )
        self.button_graphY = QtWidgets.QPushButton(
            clicked= lambda: self.setAngle(0, 0),
            icon=QIcon('y.png')
        )
        self.button_graphZ = QtWidgets.QPushButton(
            clicked=lambda: self.setAngle(90, 0),
            icon=QIcon('z.png')
        )
        self.button_graphDef = QtWidgets.QPushButton(
            clicked=lambda: self.setAngle(45, 45),
            icon=QIcon('def.png')
        )

        self.xLabel = QLabel("X position:")
        self.xText = QtWidgets.QLineEdit(text = '0', enabled = True)
        self.xText.setFixedSize(30, 25)
        self.yLabel = QLabel("X position:")
        self.yText = QtWidgets.QLineEdit(text = '0',  enabled = True)
        self.yText.setFixedSize(30, 25)
        self.x1Label = QLabel("X field:")
        self.x1Text = QtWidgets.QLineEdit(text = '96',  enabled = True)
        self.x1Text.setFixedSize(30, 25)
        self.y1Label = QLabel("Y field:")
        self.y1Text = QtWidgets.QLineEdit(text = '96',  enabled = True)
        self.y1Text.setFixedSize(30, 25)

        self.button_graphX.setFixedSize(25, 25)
        self.button_graphY.setFixedSize(25, 25)
        self.button_graphZ.setFixedSize(25, 25)
        self.button_graphDef.setFixedSize(25, 25)

        self.prgbar = QProgressBar()
        self.prgbar.setFixedSize(200, 25)

        self.button_calibrate = QtWidgets.QPushButton(
            text="Calibrate",
            enabled=False,
            clicked=lambda: self.onChar(1)


        )
        
        self.button_R = QtWidgets.QPushButton(
            text="Show",
            #enabled = False,
            clicked=self.updatePlotData
            # checkable=True,
        )
        self.button_pause = QtWidgets.QPushButton(
            text="Pause",
            enabled = False,
            checkable = True,
            clicked = self.pause

        )
        self.button_setParameters = QtWidgets.QPushButton(
             text="Set params",
             enabled = False,
             clicked = self.setParams
             )
        self.button_read = QtWidgets.QPushButton(
            text="Read",
            enabled=False,
            clicked=self.onRead
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

        #Hlayout
        Hlayout.addWidget(self.button_calibrate)
        Hlayout.addWidget(self.button_read)
        Hlayout.addWidget(self.button_pause)
        Hlayout.addWidget(self.button_R)
        Hlayout.addWidget(self.button_save)
        Hlayout.addWidget(self.button_load)
        Hlayout.addWidget(self.button_connect)


        #VLaout
        Vlayout.addLayout(Hlayout)

        Hlayout2.addWidget(self.button_graphDef)
        Hlayout2.addWidget(self.button_graphX)
        Hlayout2.addWidget(self.button_graphY)
        Hlayout2.addWidget(self.button_graphZ)
       # Hlayout2.addStretch(0)
        Hlayout2.addWidget(self.xLabel)
        Hlayout2.addWidget(self.xText)

        Hlayout2.addWidget(self.yLabel)
        Hlayout2.addWidget(self.yText)

        Hlayout2.addWidget(self.x1Label)
        Hlayout2.addWidget(self.x1Text)

        Hlayout2.addWidget(self.y1Label)
        Hlayout2.addWidget(self.y1Text)
        Hlayout2.addWidget(self.button_setParameters)
        Hlayout2.addStretch(0)
        Hlayout2.addWidget(self.prgbar)

        Vlayout.addLayout(Hlayout2)

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
        d = int(self.x[-1])*100/92
        self.prgbar.setValue(d)
       
     

    def onRead(self):
        self.ser.flushInput()
        self.ser.write(b'0')
        self.timer.start()
        self.button_pause.setEnabled(True)

    def updatePlotData(self):
        x = []
        y = []
        z = []
        for item in self.x:
            x.append(float(item))
        for item in self.y:
            y.append(float(item))
        for item in self.z:
            z.append(float(item))
        print(x)
        self.graphWidget.DrawGraph(x, y, z)

    def onChar(self, c):
        self.ser.write(bytes(str(c), encoding="ascii"))

    def saveMeasurement(self):
        dlg = AFM_Dialog.saveDialog(self)
        dlg.x1 = self.x
        dlg.y1 = self.y
        dlg.z1 = self.z
        dlg.exec_()
    
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
                self.ser.port = 'COM3'
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
        self.button_setParameters.setEnabled(True)


    def disableButtons(self):
        self.button_calibrate.setEnabled(False)
        self.button_read.setEnabled(False)
        self.button_pause.setEnabled(False)
        self.button_setParameters.setEnabled(False)

    def setAngle(self, el, az):
        self.graphWidget.axes.view_init(elev=el,azim=az)
        self.graphWidget.draw()

    def pause(self, s):
        if s:
            self.timer.stop()
        else:
            self.timer.start()

    def setParams(self):
        self.ser.write(b'2')
        x =bytes(str(self.xText.text()), encoding= 'ascii')
        y = bytes(str(self.yText.text()), encoding='ascii')
        x1 = bytes(str(self.x1Text.text()), encoding='ascii')
        y1 = bytes(str(self.y1Text.text()), encoding='ascii')
        self.ser.write(b'<')
        self.ser.write(x)
        self.ser.write(b',')
        self.ser.write(y)
        self.ser.write(b',')
        self.ser.write(x1)
        self.ser.write(b',')
        self.ser.write(y1)
        self.ser.write(b',')
        self.ser.write(b'>')

        self.button_setParameters.setEnabled(False)
        self.xText.setEnabled(False)
        self.yText.setEnabled(False)
        self.x1Text.setEnabled(False)
        self.y1Text.setEnabled(False)

app = QApplication(sys.argv)
app.setStyle('Breeze')
window = MainWindow()
window.show()

app.exec_()
