import sys
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout, QPushButton,QHBoxLayout,QDialog
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QDate
import csv, operator
import time
import webbrowser
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
        self.elegirProducto.clicked.connect(self.productoElegido)
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
        self.documento=Documento()
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
            QMessageBox.question(self, "ALERTA", "Este codigo de producto no existe.", QMessageBox.Ok)
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
            print (self.tamPedido)
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
        else:
            QMessageBox.question(self, "ALERTA", "No agregaste ningun producto.", QMessageBox.Ok)
        
class Documento(QMainWindow): 
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/documento.ui", self)
        #self.initUI()
        self.tipoDocumento.currentTextChanged.connect(self.itemChanged)
        #print (time.strftime("%I:%M:%S"))
        #print (time.strftime("%d/%m/%y"))
        self.fechaDocumento.setDate(QDate.currentDate())
        self.generarDocumento.clicked.connect(self.generarDoc)
    def initUI(self):
        self.show()
        

    def actualizarTabla(self,lista,total):
        self.tablaVenta.setRowCount(lista.rowCount())
        for i in range(lista.rowCount()):
            for j in range(5):
                self.tablaVenta.setItem(i,j,QTableWidgetItem(lista.item(i,j).text()))
        self.totalCobro.setText(total)
        self.show()

    def itemChanged(self):
        #print("Seleccionado: ", self.tipoDocumento.currentText())
        if(self.tipoDocumento.currentText()=='Factura'):
            self.documentoLabel.setText('RUC:')
        else:
            self.documentoLabel.setText('DNI:')

    def generarDoc(self):
        #archi=open('datos.html','w')
        archi=open('datos.html','a')
        archi.write(self.nombreDocumento.text())
        archi.write(self.numeroDocumento.text())
        archi.write(self.direccionDocumento.text())
        archi.close()
        webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open("file:///C:/Users/Nash/Documents/NACHO FINAL/datos.html")

        
app = QApplication(sys.argv)
lista=Lista()
documento=Documento()
pedido = Pedido(lista)
lista.pedido=pedido
pedido.documento=documento
pedido.show()
app.exec_()

