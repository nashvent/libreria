import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from pedido import *
from admin import *

class inicio(QMainWindow):
 #Método constructor de la clase
  def __init__(self,pedido,admin):
    self.pedido=pedido
    self.admin=admin
    #Iniciar el objeto QMainWindow
    QMainWindow.__init__(self)
    #Cargar la configuración del archivo .ui en el objeto
    uic.loadUi("ui/inicio.ui", self)
    self.lb_p.setStyleSheet("background: #98dc12")
    self.lb_vr.setStyleSheet("background: #FACC2E")
    self.lb_titulo.setStyleSheet("background: #1298dc ; color: white")
    self.btn_pedido.clicked.connect(self.mostrarPedido)
    self.btn_admi.clicked.connect(self.mostrarAdmin)
  def mostrarPedido(self):
    pedido.show()
    self.hide() 

  def mostrarAdmin(self):
    admin.show()
    self.hide() 


#Instancia para iniciar una aplicación
app = QApplication(sys.argv)
lista=Lista()
pedido = Pedido(lista)
documento=Documento(pedido)

lista.pedido=pedido
pedido.documento=documento
#pedido.show()
admin = Administrador()

_ventana = inicio(pedido,admin)
_ventana.show()
app.exec_()
