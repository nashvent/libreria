#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from pedido import *
from admin import *
import pandas as pd
import time

class inicio(QMainWindow):
 #Metodo constructor de la clase
    boletasFacturas = 'productos/boletas_y_facturas.csv'
    productosCSV = 'productos/productos.csv'
    def hideAdmin(self):
        self.show()
        self.admin.hide()
        self.reportes_totales()
    def hidePedido(self):
        self.show()
        self.pedido.hide()
        self.reportes_totales()
            
    def __init__(self,pedido,admin):
        self.pedido=pedido
        self.admin=admin
        QMainWindow.__init__(self)
        uic.loadUi("ui/inicio.ui", self)
        self.reportes_totales()
        self.lb_p.setStyleSheet("background: #98dc12")
        self.lb_vr.setStyleSheet("background: #FACC2E")
        self.lb_titulo.setStyleSheet("background: #1298dc ; color: white")
        self.btn_pedido.clicked.connect(self.mostrarPedido)
        self.btn_admi.clicked.connect(self.mostrarAdmin)
        self.admin.btn_atras.clicked.connect(self.hideAdmin)
        self.pedido.btn_atras.clicked.connect(self.hidePedido)
    def mostrarPedido(self):
        lista.productos=actualizarListaProductos()
        pedido.show()
        self.hide() 

    def mostrarAdmin(self):
        admin.show()
        self.hide() 

    def reportes_totales(self):
        f = open(self.boletasFacturas,'rU')
        bf = pd.read_csv(f)
        hoy =time.strftime('/%d/%m/%Y')
        nv=len(bf[bf.fecha==hoy])
        f = open(self.productosCSV,'rU')
        bf = pd.read_csv(f)
        cp=len(bf)
        self.lb_vr.setText('               Ventas del Día: '+str(nv))
        self.lb_p.setText('               N° de Productos: '+str(cp))

#Instancia para iniciar una aplicación
app = QApplication(sys.argv)

lista=Lista()
pedido = Pedido(lista)
documento=Documento(pedido)

#pedido.show()
admin = Administrador()

_ventana = inicio(pedido,admin)
_ventana.show()
app.exec_()
