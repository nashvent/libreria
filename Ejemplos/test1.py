import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5 import uic


class Main(QMainWindow):
    def __init__(self, parent = None):
        super(Main, self).__init__(parent)

        # main button
        self.addButton = QPushButton('button to add other widgets')
        self.addButton.clicked.connect(self.addWidget)

        # scroll area widget contents - layout
        self.scrollLayout = QtGui.QFormLayout()

        # scroll area widget contents
        self.scrollWidget = QtGui.QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)

        # scroll area
        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)

        # main layout
        self.mainLayout = QtGui.QVBoxLayout()

        # add all main to the main vLayout
        self.mainLayout.addWidget(self.addButton)
        self.mainLayout.addWidget(self.scrollArea)

        # central widget
        self.centralWidget = QtGui.QWidget()
        self.centralWidget.setLayout(self.mainLayout)

        # set central widget
        self.setCentralWidget(self.centralWidget)

    def addWidget(self):
        self.scrollLayout.addRow(Test())


class Test(QWidget):
  def __init__( self, parent=None):
      super(Test, self).__init__(parent)

      self.pushButton = QtGui.QPushButton('I am in Test widget')

      layout = QtGui.QHBoxLayout()
      layout.addWidget(self.pushButton)
      self.setLayout(layout)



app = QApplication(sys.argv)
myWidget = Main()
myWidget.show()
app.exec_()
