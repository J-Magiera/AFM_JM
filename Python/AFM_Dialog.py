from PyQt5.QtWidgets import QLineEdit, QFormLayout, QDialog
from PyQt5 import QtWidgets
import csv

class saveDialog(QtWidgets.QDialog):

    def __init__(self,  *args, **kwargs):
        super(saveDialog, self).__init__(*args, **kwargs)
        self.x1 = []
        self.y1 = []
        self.z1 = []
       
        self.setWindowTitle("Enter filename")
        self.layout = QFormLayout()
        self.e4 = QLineEdit()
        self.layout.addRow("Filename: ", self.e4)
        self.button_sav = QtWidgets.QPushButton(
            text="Save",
            clicked= lambda: self.saveAs(self.e4.text())

        )
        self.layout.addRow(self.button_sav)
        self.setLayout(self.layout)

    def saveAs(self, text):
        try:
            file = open(text+'.csv','w', newline='', quoting=csv.QUOTE_NONE)
            writer = csv.writer(file)
            print(self.x1)
            writer.writerow([self.x1])
            writer.writerow([self.y1])
            writer.writerow([self.z1])
            #This function will save all gathered data into .csv file with name from textbox
        except:
            print("Error #0003")
            
            
class loadDialog(QtWidgets.QDialog):

    def __init__(self,  *args, **kwargs):
        super(loadDialog, self).__init__(*args, **kwargs)
        self.x1 = []
        self.y1 = []
        self.z1 = []
       
        self.setWindowTitle("Enter filename")
        self.layout = QFormLayout()
        self.e4 = QLineEdit()
        self.layout.addRow("Filename: ", self.e4)
        self.button_lod = QtWidgets.QPushButton(
            text="Load",
            clicked= lambda: self.readFile(self.e4.text())

        )
        self.layout.addRow(self.button_lod)
        self.setLayout(self.layout)
            
            
    def readFile(self, text):
        try:
            file = open(text+'.csv','r')
            data = []
            reader = csv.reader(file)
            for i, row in reader:
                data[i] = row
            self.x1 = data[0]
            self.y1 = data[1]
            self.z1 = data[2]

        except:
            print("Error #0004")                