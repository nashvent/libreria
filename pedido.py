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

#print(len(productos))
def actualizarListaProductos():
    productos=[]
    with open('productos/productos.csv') as csvarchivo:
        entrada = csv.DictReader(csvarchivo)
        for reg in entrada:
            productos.append(reg)
        return productos


class Lista(QDialog): 
    productos=actualizarListaProductos()
    def __init__(self):
        self.listaTitulo.setStyleSheet("background: #98dc12")
        pedido=Pedido(self)
        QDialog.__init__(self)
        uic.loadUi("ui/lista_productos.ui", self)
        self.initUI()
    def initUI(self):
        self.tableWidget.doubleClicked.connect(self.on_click)
        #self.tableWidget.setItem(0,0, QTableWidgetItem("Cell (1,1)"))
        self.actualizarLista()
    def productoElegido(self):
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            self.agregarCodigo(currentQTableWidgetItem.row())

    def agregarCodigo(self,pos):
        self.pedido.lineaCodigo.setText(self.productos[pos]['codigo'])
        self.pedido.cantidadPedido.setMaximum(int(self.productos[pos]['stock']))
        self.hide()
    def actualizarLista(self):
        productos=[]
        with open('productos/productos.csv') as csvarchivo:
            entrada = csv.DictReader(csvarchivo)
            for reg in entrada:
                productos.append(reg)
        i=0
        self.tableWidget.setRowCount(len(productos))
        while(len(productos)>i):
            self.tableWidget.setItem(i,0, QTableWidgetItem(productos[i]['codigo']))
            self.tableWidget.setItem(i,1, QTableWidgetItem(productos[i]['nombre']))
            self.tableWidget.setItem(i,2, QTableWidgetItem(productos[i]['precio_venta']))
            self.tableWidget.setItem(i,3, QTableWidgetItem(productos[i]['stock']))
            i=i+1
    @pyqtSlot()
    def on_click(self):
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            self.agregarCodigo(currentQTableWidgetItem.row())
    
        
class Pedido(QMainWindow):
    productos=actualizarListaProductos()
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
        self.lista.actualizarLista()
        self.lista.show()

    def PosPorCodigo(self,cod):
        pos=0
        for i in self.productos:
            if i['codigo']==cod :
                break
            pos=pos+1
        if pos==len(self.productos):
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
        if(self.productos[pos]['stock']=='0'):
            QMessageBox.warning(self, "ALERTA", "Ya no hay stock de "+self.productos[pos]['nombre']+'.', QMessageBox.Ok)
            self.lineaCodigo.setText('')
            return
        else:
            self.tablePedido.setRowCount(self.tamPedido+1)
            self.tablePedido.setItem(self.tamPedido,0,QTableWidgetItem(self.productos[pos]['codigo']))
            self.tablePedido.setItem(self.tamPedido,1,QTableWidgetItem(self.productos[pos]['nombre']))
            self.tablePedido.setItem(self.tamPedido,2,QTableWidgetItem(self.productos[pos]['precio_venta']))
            self.tablePedido.setItem(self.tamPedido,3,QTableWidgetItem(str(cantidad)))
            total=str(float(self.productos[pos]['precio_venta'])*cantidad)
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
            QMessageBox.warning(self, "ALERTA", "No agregaste ningun producto.", QMessageBox.Ok)
        
class Documento(QMainWindow): 
    boletasFacturas = 'productos/boletas_y_facturas.csv'
    productosCSV = 'productos/productos.csv'

    def __init__(self,pedido):
        QMainWindow.__init__(self)
        uic.loadUi("ui/documento.ui", self)
        self.pedido=pedido
        #self.initUI()
        self.tipoDocumento.currentTextChanged.connect(self.itemChanged)
        #print (time.strftime("%I:%M:%S"))
        #print (time.strftime("%d/%m/%y"))
        self.fechaDocumento.setDate(QDate.currentDate())
        self.generarDocumento.clicked.connect(self.confirmarDocumento)
        self.editarPedido.clicked.connect(self.mostrarPedido)
        self.igv=0
        self.totalDocumento=0
        #self.actualizarStock()
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
        tipo=''
        archivoActual=''
        archivoRegistro=''
        datos=''
        htmlDoc=''
        pdfDoc=''
        pdf2Doc=''
        ganancia=0
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
            tipo='f'
            
        else:
            infile = open('documentos/boletas/template/nro_boleta.txt', 'r')
            contadorBol=infile.read()
            datos=datos+(contadorBol)
            htmlDoc='documentos/boletas/template/boleta.html'
            pdfDoc='documentos/boletas/template/boleta.pdf'
            pdf2Doc='documentos\\boletas\\template\\boleta.pdf'
            tipo='b'
        listaActualizar=[]    
        for i in range(self.tablaVenta.rowCount()):
            datos=datos+(',')
            datos=datos+(self.tablaVenta.item(i,1).text())
            datos=datos+(',')
            datos=datos+(self.tablaVenta.item(i,2).text())
            datos=datos+(',')
            datos=datos+(self.tablaVenta.item(i,3).text())
            datos=datos+(',')
            datos=datos+(self.tablaVenta.item(i,4).text())
            listaActualizar.append([self.tablaVenta.item(i,0).text(),self.tablaVenta.item(i,3).text()])
            ganancia=ganancia+self.busGanancia(self.tablaVenta.item(i,0).text(),self.tablaVenta.item(i,3).text())
        archi.write(datos)
        registro.write(datos)
        archi.close()
        registro.close()
        pdfkit.from_file(htmlDoc,pdfDoc )
        os.startfile(pdf2Doc)

        BoleFactu=[]
        with open(self.boletasFacturas) as csvarchivo:
            cpd_product  = csv.DictReader(csvarchivo)
            for reg in cpd_product:
                BoleFactu.append(reg)

        BoleFactu.append({'fecha':self.fechaDocumento.date().toString("dd/MM/yyyy"), 'hora':time.strftime('%H-%M-%S'),'tipo':tipo,'nombre':self.nombreDocumento.text(),'dni_ruc':self.numeroDocumento.text(),'direccion':self.direccionDocumento.text(),'total':str(self.pedido.TotalPedido),'ganancia':str(ganancia),'ubicacion':archivoRegistro});
        toCSV = BoleFactu 
        keys = toCSV[0].keys()
        with open(self.boletasFacturas, 'w') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(toCSV)

        
        self.actualizarStock(listaActualizar)
        self.pedido.limpiarPedido()
        self.mostrarPedido()
        
    def mostrarPedido(self):
        self.pedido.show()
        self.hide()

    def actualizarStock(self,listaVenta):
        #print(listaVenta)
        productos=[]
        with open(self.productosCSV) as csvarchivo:
            entrada  = csv.DictReader(csvarchivo)
            for reg in entrada:
                productos.append(reg)
        for i in range(len(listaVenta)):
            for j in productos:
                if(listaVenta[i][0]==j['codigo']):
                    #print(type(j['stock']))
                    j['stock']=str(int(j['stock'])-(int(listaVenta[i][1])))
                    j['contador']=str(int(j['contador'])+(int(listaVenta[i][1])))
                    break
        toCSV = productos
        keys = toCSV[0].keys()
        with open(self.productosCSV, 'w') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(toCSV)
        self.pedido.productos=productos
        self.pedido.lista.productos=productos
        self.pedido.lista.actualizarLista()
        
    def confirmarDocumento(self):
        resultado = QMessageBox.question(self, "Aceptar Compra", "Esta Seguro que quiere registrar la compra", QMessageBox.Yes | QMessageBox.No)
        if resultado == QMessageBox.Yes: self.generarDoc()
        
    def busGanancia(self,cod,cant):
        productosGanancia=self.pedido.productos
        for i in productosGanancia:
            if(cod==i['codigo']):
                return float(i['precio_compra'])*float(cant)
        
