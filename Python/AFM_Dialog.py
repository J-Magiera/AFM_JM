from PyQt5.QtWidgets import QLineEdit, QFormLayout
from PyQt5 import QtWidgets


class FileDialog(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        super(FileDialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("Enter filename")
        self.layout = QFormLayout()
        self.e4 = QLineEdit()
        self.text = 'Confirm'
        self.layout.addRow("Filename: ", self.e4)
        self.button_ex = QtWidgets.QPushButton(
            text=self.text,
            clicked=  self.closeDlg

        )
        self.layout.addRow(self.button_ex)
        self.setLayout(self.layout)

    def closeDlg(self):
        self.close()
        pass