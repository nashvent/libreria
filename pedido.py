import sys
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout, QPushButton,QHBoxLayout,QDialog
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QDate
import csv, operator
import time
import pdfkit
import os
import pandas as pd

productos=[]
with open('productos/productos.csv') as csvarchivo:
    entrada = csv.DictReader(csvarchivo)
    for reg in entrada:
        productos.append(reg)
#print(len(productos))

class Lista(QDialog): 
    def __init__(self):
        pedido=Pedido(self)
        QDialog.__init__(self)
        uic.loadUi("ui/lista_productos.ui", self)
        self.initUI()
    def initUI(self):
        self.tableWidget.doubleClicked.connect(self.on_click)
        #self.tableWidget.setItem(0,0, QTableWidgetItem("Cell (1,1)"))
        i=0
        self.tableWidget.setRowCount(len(productos))
        while(len(productos)>i):
            self.tableWidget.setItem(i,0, QTableWidgetItem(productos[i]['codigo']))
            self.tableWidget.setItem(i,1, QTableWidgetItem(productos[i]['nombre']))
            self.tableWidget.setItem(i,2, QTableWidgetItem(productos[i]['precio_venta']))
            self.tableWidget.setItem(i,3, QTableWidgetItem(productos[i]['stock']))
            i=i+1

    def productoElegido(self):
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            self.agregarCodigo(currentQTableWidgetItem.row())

    def agregarCodigo(self,pos):
        self.pedido.lineaCodigo.setText(productos[pos]['codigo'])
        self.hide()
        
    @pyqtSlot()
    def on_click(self):
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            self.agregarCodigo(currentQTableWidgetItem.row())
    
        
class Pedido(QMainWindow):
    def __init__(self,lista):
        self.documento=Documento(self)
        self.tamPedido=0
        self.TotalPedido=0
        self.lista=lista
        QMainWindow.__init__(self)
        uic.loadUi("ui/pedido.ui", self)
        self.botonLista.clicked.connect(self.mostrarLista)
        self.botonAgregar.clicked.connect(self.agregarProducto)
        self.quitarProducto.clicked.connect(self.productoRemovido)
        self.cancelarPedido.clicked.connect(self.limpiarPedido)
        self.enviarPedido.clicked.connect(self.generarPedido)
        self.lb_titulo.setStyleSheet("background: #98dc12")

    def mostrarLista(self):
        self.lista.show()

    def PosPorCodigo(self,cod):
        pos=0
        for i in productos:
            if i['codigo']==cod:
                break
            pos=pos+1
        if pos==len(productos):
            pos=-1
        return pos
    
    def agregarProducto(self):
        pos1=self.PosPorCodigo(self.lineaCodigo.text())
        pos=pos1
        cantidad=self.cantidadPedido.value()
        if(pos==-1):
            QMessageBox.warning(self, "ALERTA", "Este codigo de producto no existe.", QMessageBox.Ok)
            self.lineaCodigo.setText('')
            return
        else:
            self.tablePedido.setRowCount(self.tamPedido+1)
            self.tablePedido.setItem(self.tamPedido,0,QTableWidgetItem(productos[pos]['codigo']))
            self.tablePedido.setItem(self.tamPedido,1,QTableWidgetItem(productos[pos]['nombre']))
            self.tablePedido.setItem(self.tamPedido,2,QTableWidgetItem(productos[pos]['precio_venta']))
            self.tablePedido.setItem(self.tamPedido,3,QTableWidgetItem(str(cantidad)))
            total=str(float(productos[pos]['precio_venta'])*cantidad);
            self.TotalPedido=self.TotalPedido+float(total)
            self.tablePedido.setItem(self.tamPedido,4,QTableWidgetItem(total))
            self.tamPedido=self.tamPedido+1
            self.TotalPedidoLabel.setText('S/.'+str(self.TotalPedido))

    def productoRemovido(self):
        for currentQTableWidgetItem in self.tablePedido.selectedItems():
            self.TotalPedido=self.TotalPedido-float(self.tablePedido.item(currentQTableWidgetItem.row(),4).text())
            self.TotalPedidoLabel.setText('S/.'+str(self.TotalPedido))
            self.tablePedido.removeRow(currentQTableWidgetItem.row())
            self.tamPedido=self.tamPedido-1
            #print (self.tamPedido)
    def limpiarPedido(self):
        self.lineaCodigo.setText('')
        self.TotalPedido=0;
        self.TotalPedidoLabel.setText('S/.'+str(self.TotalPedido))
        self.tamPedido=0
        self.tablePedido.setRowCount(self.tamPedido)
        self.cantidadPedido.setValue(1)
    def generarPedido(self):
        if(self.tamPedido>0):
            self.documento.actualizarTabla(self.tablePedido,self.TotalPedidoLabel.text())
            self.hide()
        else:
            QMessageBox.question(self, "ALERTA", "No agregaste ningun producto.", QMessageBox.Ok)
        
class Documento(QMainWindow): 
    def __init__(self,pedido):
        QMainWindow.__init__(self)
        uic.loadUi("ui/documento.ui", self)
        self.pedido=pedido
        #self.initUI()
        self.tipoDocumento.currentTextChanged.connect(self.itemChanged)
        #print (time.strftime("%I:%M:%S"))
        #print (time.strftime("%d/%m/%y"))
        self.fechaDocumento.setDate(QDate.currentDate())
        self.generarDocumento.clicked.connect(self.generarDoc)
        self.editarPedido.clicked.connect(self.mostrarPedido)
        self.igv=0
        self.totalDocumento=0
        self.actualizarStock()
    def initUI(self):
        self.show()

    def actualizarTabla(self,lista,total):
        self.tablaVenta.setRowCount(lista.rowCount())
        for i in range(lista.rowCount()):
            for j in range(5):
                self.tablaVenta.setItem(i,j,QTableWidgetItem(lista.item(i,j).text()))
        
        self.igv=self.pedido.TotalPedido*0.18
        self.totalDocumento=self.pedido.TotalPedido
        if(self.tipoDocumento.currentText()=='Factura'):
            self.totalDocumento=self.totalDocumento+self.igv
        self.totalCobro.setText('S/.'+str(self.totalDocumento))
        self.show()

    def itemChanged(self):
        #print("Seleccionado: ", self.tipoDocumento.currentText())
        if(self.tipoDocumento.currentText()=='Factura'):
            self.documentoLabel.setText('RUC:')
            self.igvLabel.setText('S/.'+str(round(self.igv,9)))
            self.totalDocumento=self.totalDocumento+self.igv
            self.totalCobro.setText('S/.'+str(round(self.totalDocumento,9)))
        else:
            self.documentoLabel.setText('DNI:')
            self.totalDocumento=self.totalDocumento-self.igv
            self.totalCobro.setText('S/.'+str(self.totalDocumento))
            self.igvLabel.setText('S/.0.0')

    def generarDoc(self):    
        #archi=open('datos.html','w')
        archivoActual=''
        archivoRegistro=''
        datos=''
        htmlDoc=''
        pdfDoc=''
        pdf2Doc=''
        if(self.documentoLabel.text()=='RUC:'):
            archivoActual='documentos/facturas/template/actual.txt'
            archivoRegistro='documentos/facturas/'
        else:
            archivoActual='documentos/boletas/template/actual.txt'
            archivoRegistro='documentos/boletas/'
        archivoRegistro=archivoRegistro+self.fechaDocumento.date().toString("dd-MM-yyyy")+'-'+time.strftime('%H-%M-%S')+'.txt'
        registro=open(archivoRegistro,'w')
        
        #print(archivoRegistro)
        archi=open(archivoActual,'w')
        datos=datos+(self.nombreDocumento.text())
        datos=datos+(',')
        datos=datos+(self.direccionDocumento.text())
        datos=datos+(',')
        datos=datos+(self.numeroDocumento.text())
        datos=datos+(',')
        datos=datos+(self.fechaDocumento.date().toString("dd/MM/yyyy"))
        datos=datos+(',')
        datos=datos+(str(self.pedido.TotalPedido))
        datos=datos+(',')
        if(self.documentoLabel.text()=='RUC:'):
            infile = open('documentos/facturas/template/nro_factura.txt', 'r')
            contadorFact=infile.read()
            datos=datos+(contadorFact)
            datos=datos+(',')
            datos=datos+(str(self.igv))
            htmlDoc='documentos/facturas/template/factura.html'
            pdfDoc='documentos/facturas/template/factura.pdf'
            pdf2Doc='documentos\\facturas\\template\\factura.pdf'
            
        else:
            infile = open('documentos/boletas/template/nro_boleta.txt', 'r')
            contadorBol=infile.read()
            datos=datos+(contadorBol)
            htmlDoc='documentos/boletas/template/boleta.html'
            pdfDoc='documentos/boletas/template/boleta.pdf'
            pdf2Doc='documentos\\boletas\\template\\boleta.pdf'
            
        for i in range(self.tablaVenta.rowCount()):
            datos=datos+(',')
            datos=datos+(self.tablaVenta.item(i,1).text())
            datos=datos+(',')
            datos=datos+(self.tablaVenta.item(i,2).text())
            datos=datos+(',')
            datos=datos+(self.tablaVenta.item(i,3).text())
            datos=datos+(',')
            datos=datos+(self.tablaVenta.item(i,4).text())

        archi.write(datos)
        registro.write(datos)
        archi.close()
        registro.close()
        pdfkit.from_file(htmlDoc,pdfDoc )
        os.startfile(pdf2Doc)
    def mostrarPedido(self):
        self.pedido.show()
        self.hide()
    def actualizarStock(self):
        print('paseeeeeee')
        productosCSV = 'productos/productos.csv'
        f = open(productosCSV,'rU')
        products = pd.read_csv(f)
        #p3=products[products.codigo==20]['codigo']
        products[products.codigo==20].ix['codigo']=100
        #products.ix[2,'codigo']=1000
        print(products)
        

