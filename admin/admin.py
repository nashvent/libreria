
import sys
import csv
import os
import pandas as pd
IB = os.environ.get('INSTABASE_URI',None) is not None
open = ib.open if IB else open

from PyQt5.QtWidgets import QApplication, QMainWindow,QMessageBox
from PyQt5 import uic
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5 import QtGui, QtCore

class Interfaz(object):
    def closeEvent(self, event):
        resultado = QMessageBox.question(self, "Salir...", "¿Seguro que quiere salir del Administrador?", QMessageBox.Yes | QMessageBox.No)
        if resultado == QMessageBox.Yes: event.accept()
        else: event.ignore()

productos=[]
with open('productos.csv') as csvarchivo:
    entrada = csv.DictReader(csvarchivo)
    for reg in entrada:
        productos.append(reg)

class Administrador(QMainWindow,Interfaz):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("admin.ui", self)
        
        self.btn_agregar.clicked.connect(self.agregar_producto)
    def agregar_producto(self):
        p2=[]
        with open('productos.csv') as csvarchivo:
          entrada  = csv.DictReader(csvarchivo)
          for reg in entrada:
              p2.append(reg)

        a_codigo=(self.a_codigo.text())
        a_nombre=(self.a_nombre.text())
        a_stock=(self.a_stock.value())
        a_precio_compra=(self.a_precio_compra.value())
        a_precio_venta=(self.a_precio_venta.value())
        a_descripcion=(self.a_descripcion.text())
        ind=0
        for r in p2:
          if  r['codigo'] ==  a_codigo:
            ind=1
            break
        if(ind==0):
          p2.append({'codigo':a_codigo, 'nombre':a_nombre,'stock':str(a_stock),'precio_compra':str(a_precio_compra),'precio_venta':str(a_precio_venta),'descripcion':a_descripcion});
        else:
          QMessageBox.question(self, "Alerta!", "Este codigo de producto ya esta usado.", QMessageBox.Ok)
          
        toCSV = p2
        keys = toCSV[0].keys()
        with open('productos.csv', 'w') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(toCSV)

    def editar_producto(self):
        e_codigo=(self.e_codigo.text())
        e_nombre=(self.e_nombre.text())
        e_stock=(self.e_stock.value())
        e_precio_compra=(self.e_precio_compra.value())
        e_precio_venta=(self.e_precio_venta.value())
        e_descripcion=(self.e_descripcion.text())
        print (e_codigo,e_nombre,e_stock,e_precio_compra,e_precio_venta,e_descripcion)
        
    def tabla_productos(self)
        for r in productos
          

#Instancia para iniciar una aplicación
app = QApplication(sys.argv)
_ventana = Administrador()
_ventana.show()
app.exec_()
