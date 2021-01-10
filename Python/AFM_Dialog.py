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
            file = open(text+'.csv','w', newline='')
            writer = csv.writer(file)
            print(self.x1)
            writer.writerow([self.dat[0]])
            writer.writerow([self.dat[1]])
            writer.writerow([self.dat[2]])
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
            reader = csv.reader(file)
            self.x1 = file.readline()
            self.y1 = file.readline()
            self.z1 = file.readline()
            print(self.x1)
        except:
            print("Error #0004")                
