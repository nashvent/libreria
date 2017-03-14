
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

class Ventana(QMainWindow):
 #Método constructor de la clase
 def __init__(self):
  #Iniciar el objeto QMainWindow
  QMainWindow.__init__(self)
  #Cargar la configuración del archivo .ui en el objeto
  uic.loadUi("nuevo.ui", self)
  self.setWindowTitle("Cambiando el título de la ventana")
  self.btn_CtoF.clicked.connect(self.btn_CtoF_clicked)
  self.btn_FtoC.clicked.connect(self.btn_FtoC_clicked)
 # Evento del boton btn_CtoF
 def btn_CtoF_clicked(self):
  cel = float(self.editCel.text())
  fahr = cel * 9 / 5.0 + 32
  self.spinFar.setValue(int(fahr + 0.5))
 
 # Evento del boton btn_FtoC
 def btn_FtoC_clicked(self):
  fahr = self.spinFar.value()
  cel = ((fahr - 32) * 5) / 9
  self.editCel.setText(str(cel))
  
  
#Instancia para iniciar una aplicación
app = QApplication(sys.argv)


_ventana = Ventana()
_ventana.show()
app.exec_()
