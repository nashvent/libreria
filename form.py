#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QMessageBox
from PyQt5 import uic
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class Interfaz(object):
    def closeEvent(self, event):
        resultado = QMessageBox.question(self, "Salir ...", "¿Seguro que quiere eliminar lo nuestrooooo?", QMessageBox.Yes | QMessageBox.No)
        if resultado == QMessageBox.Yes: event.accept()
        else: event.ignore()


edad=""        
class Pedido(QMainWindow,Interfaz):
    def __init__(self,objeto):
        self.obj=objeto
        QMainWindow.__init__(self)
        uic.loadUi("form.ui", self)
        self.setMaximumSize(300,300)
        qfont=QFont("Arial",9,QFont.Bold)
        self.setFont(qfont)
        #self.setStyleSheet("background-color:#012033;")
        #self.enviar.setStyleSheet("background-color: #000; color: #fff; font-size: 14px;")
        self.enviar.clicked.connect(self.enviar_datos)
    def enviar_datos(self):
        nombre=(self.nombreEdit.text())
        edad=self.edadEdit.text()
        self.obj.actualizar(nombre)
        self.hide()
        
    
        
class Datos(QMainWindow,Interfaz):
    def __init__(self):
        self.anterior=Pedido(self)
        QMainWindow.__init__(self)
        uic.loadUi("formR.ui", self)
        self.setMaximumSize(300,300)
        qfont=QFont("Arial",9,QFont.Bold)
        self.setFont(qfont)
    def actualizar(self,nombre):
        self.nombreR.setText(nombre)
        print (nombre)
        self.show()
    def closeEvent(self, event):
        resultado = QMessageBox.question(self, "Salir ...", "¿Seguro que quiere eliminar lo nuestrooooo?", QMessageBox.Yes | QMessageBox.No)
        if resultado == QMessageBox.Yes: event.accept()
        else: event.ignore()
        self.anterior.show()
    
app = QApplication(sys.argv)
_obj=Datos()
_ventana1 = Pedido(_obj)
_obj.anterior=_ventana1
_ventana1.show()


app.exec_()
    
