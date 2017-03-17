
import sys
import csv
import os
from PyQt5.QtWidgets import QMessageBox,QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout, QPushButton,QHBoxLayout,QDialog
from PyQt5 import uic
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDate
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui, QtCore

class Interfaz(object):
    def closeEvent(self, event):
        resultado = QMessageBox.question(self, "Salir...", "¿Seguro que quiere salir del Administrador?", QMessageBox.Yes | QMessageBox.No)
        if resultado == QMessageBox.Yes: event.accept()
        else: event.ignore()

class Administrador(QMainWindow,Interfaz):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("admin.ui", self)
        
        self.tipo_bolefac.currentTextChanged.connect(self.itemChanged)
        self.btn_agregar.clicked.connect(self.agregar_producto)
        self.btn_buscar.clicked.connect(self.ver_productos)
        self.tabla_productos.doubleClicked.connect(self.on_click)
        self.btn_editar.clicked.connect(self.cambio_datos)
        self.btn_eliminar.clicked.connect(self.eliminar)
        self.ini_fecha.setDate(QDate.currentDate())
        self.fin_fecha.setDate(QDate.currentDate())
        self.btn_bolefac.clicked.connect(self.ver_bolefac)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tabla_productos.selectedItems():
            self.select_producto(currentQTableWidgetItem.row())
    #Agregar Productos
    def agregar_producto(self):
        p2=[]
        with open('../productos/productos.csv') as csvarchivo:
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
          QMessageBox.critical(self, "ALERTA", "Este código de producto ya está usado.", QMessageBox.Ok)
          return

        toCSV = p2
        keys = toCSV[0].keys()
        with open('../productos/productos.csv', 'w') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(toCSV)
        QMessageBox.question(self, "Agregar Producto", "Se agrego con Exito", QMessageBox.Ok)
   
    #Edicion del Producto
    def limpiar(self):
        self.e_codigo.setText('')
        self.e_nombre.setText('')
        self.e_stock.setValue(0)
        self.sumar_stock.setValue(0)
        self.e_precio_compra.setValue(0)
        self.e_precio_venta.setValue(0)
        self.e_descripcion.setText('')

    def cambio_datos(self,fila):
        p2=[]
        with open('../productos/productos.csv') as csvarchivo:
          entrada  = csv.DictReader(csvarchivo)
          for reg in entrada:
              p2.append(reg)
        for currentQTableWidgetItem in self.tabla_productos.selectedItems():
            fila=currentQTableWidgetItem.row()

        e_codigo=(self.e_codigo.text())
        e_nombre=(self.e_nombre.text())
        e_stock=(self.e_stock.value())
        e_sumar=(self.sumar_stock.value())
        e_precio_compra=(self.e_precio_compra.value())
        e_precio_venta=(self.e_precio_venta.value())
        e_descripcion=(self.e_descripcion.text())
        if (e_codigo!='' or e_nombre!=''):
          cod=self.tabla_productos.item(fila,0).text()
          ind=True
          for r in p2:
            if  r['codigo'] ==  e_codigo:
              ind=False
              break

          if (ind or e_codigo==cod):
            for r in p2:
              if  r['codigo'] == cod:
                r['codigo']=e_codigo
                r['nombre']=e_nombre
                r['stock']=e_stock + e_sumar
                r['precio_compra']=e_precio_compra
                r['precio_venta']=e_precio_venta
                r['descripcion']=e_descripcion
                break
            toCSV = p2
            keys = toCSV[0].keys()
            with open('../productos/productos.csv', 'w') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(toCSV)
            QMessageBox.question(self, "Editó el Producto "+cod, "Se guardo con Exito", QMessageBox.Ok)
            self.limpiar()
            self.b_producto.setText(e_codigo)
            self.ver_productos()
          else:
            QMessageBox.critical(self, "ALERTA", "Este código de producto ya esta usado.", QMessageBox.Ok)
        else:
            QMessageBox.critical(self, "ALERTA", "Datos del producto sin llenar", QMessageBox.Ok)

    def select_producto(self,fila):
        self.e_codigo.setText(self.tabla_productos.item(fila,0).text())
        self.e_nombre.setText(self.tabla_productos.item(fila,1).text())
        self.e_stock.setValue(int(self.tabla_productos.item(fila,2).text()))
        self.e_precio_compra.setValue(float(self.tabla_productos.item(fila,3).text()))
        self.e_precio_venta.setValue(float(self.tabla_productos.item(fila,4).text()))
        self.e_descripcion.setText(self.tabla_productos.item(fila,5).text())
    
    #Busqueda
    def filtro_busqueda(self,x,y):
        if(len(x)>len(y)):
          tmin=len(y)
          x=x[:tmin]
        else:
          tmin=len(x)
          y=y[:tmin]
        if (x==y):
          return True
        return False
    
    def busqueda(self,busca):
        i=0
        temp=True
        with open('../productos/productos.csv') as csvarchivo:
          cpd_product  = csv.DictReader(csvarchivo)
          for r in cpd_product:
            if(self.filtro_busqueda(r[busca],self.b_producto.text())):
              if(r['codigo']!=''):
                self.tabla_productos.setRowCount(i+1)
                self.tabla_productos.setItem(i,0, QTableWidgetItem(r['codigo']))
                self.tabla_productos.setItem(i,1, QTableWidgetItem(r['nombre']))
                self.tabla_productos.setItem(i,2, QTableWidgetItem(r['stock']))
                self.tabla_productos.setItem(i,3, QTableWidgetItem(r['precio_compra']))
                self.tabla_productos.setItem(i,4, QTableWidgetItem(r['precio_venta']))
                self.tabla_productos.setItem(i,5, QTableWidgetItem(r['descripcion']))
                i=i+1
                temp=False
          if(temp):
              self.tabla_productos.setRowCount(0)

    def ver_productos(self):
        tipo_buscar=(self.b_codigo.currentText())
        if (tipo_buscar=='Código'):
          self.busqueda('codigo')
        else:
          self.busqueda('nombre')

    #Eliminar Productos
    def borrar_producto(self,cod_borrar):
        p2=[]
        with open('../productos/productos.csv') as csvarchivo:
          entrada  = csv.DictReader(csvarchivo)
          for reg in entrada:
              p2.append(reg)
        for r in p2:
          if  r['codigo'] ==  cod_borrar:
            p2.remove(r)
            toCSV = p2
            keys = toCSV[0].keys()
            with open('../productos/productos.csv', 'w') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(toCSV)
            QMessageBox.question(self, "Elimino Producto "+cod_borrar, "Se elimino con Exito", QMessageBox.Ok)
            self.limpiar()
            self.b_producto.setText('')
            self.ver_productos()
            break

    def eliminar(self):
        for currentQTableWidgetItem in self.tabla_productos.selectedItems():
          fila=currentQTableWidgetItem.row()
          cod_borrar=self.tabla_productos.item(fila,0).text()
          self.tabla_productos.removeRow(fila)
          self.borrar_producto(cod_borrar)
    
    #Buscar Boletas y Facturas
    def compara_fechas(self,x,y):
        diax=x[1:3]
        mesx=x[4:-5]
        añox=x[-4:]

        diay=y[1:3]
        mesy=y[4:-5]
        añoy=y[-4:]

        if añox<añoy:
          return True
        elif añox==añoy:
          if mesx<mesy:
            return True
          elif mesx==mesy:
            if diax<=diay:
              return True
        return False

    def busca_por_fecha(self,tipo):
        i=0
        temp=True
        fecha_ini='/'+self.ini_fecha.date().toString('dd/MM/yyyy')
        fecha_fin='/'+self.fin_fecha.date().toString('dd/MM/yyyy')
        
        if (self.compara_fechas(fecha_ini,fecha_fin)):
         with open('../productos/boletas_y_facturas.csv') as csvarchivo:
            cpd_product  = csv.DictReader(csvarchivo)
            for r in cpd_product:
              if( (r['tipo']==tipo or tipo=='Ambos') and self.compara_fechas(fecha_ini,r['fecha']) and self.compara_fechas(r['fecha'],fecha_fin)):
                  self.tabla_bolefac.setRowCount(i+1)
                  self.tabla_bolefac.setItem(i,0, QTableWidgetItem(r['fecha']))
                  self.tabla_bolefac.setItem(i,1, QTableWidgetItem(r['hora']))
                  self.tabla_bolefac.setItem(i,2, QTableWidgetItem(r['nombre']))
                  self.tabla_bolefac.setItem(i,3, QTableWidgetItem(r['dni_ruc']))
                  self.tabla_bolefac.setItem(i,4, QTableWidgetItem(r['direccion']))
                  self.tabla_bolefac.setItem(i,5, QTableWidgetItem(r['total']))
                  i=i+1
                  temp=False
            if(temp):
                self.tabla_bolefac.setRowCount(0)
        else:
          QMessageBox.critical(self, "ALERTA", "Ingrese correctamente la fecha", QMessageBox.Ok)
    
    def busca_por_dni_ruc(self,tipo):
        i=0
        temp=True
        with open('../productos/boletas_y_facturas.csv') as csvarchivo:
          cpd_product  = csv.DictReader(csvarchivo)
          for r in cpd_product:
            if( r['tipo']==tipo and self.filtro_busqueda(r['dni_ruc'],self.b_dato.text())):
                self.tabla_bolefac.setRowCount(i+1)
                self.tabla_bolefac.setItem(i,0, QTableWidgetItem(r['fecha']))
                self.tabla_bolefac.setItem(i,1, QTableWidgetItem(r['hora']))
                self.tabla_bolefac.setItem(i,2, QTableWidgetItem(r['nombre']))
                self.tabla_bolefac.setItem(i,3, QTableWidgetItem(r['dni_ruc']))
                self.tabla_bolefac.setItem(i,4, QTableWidgetItem(r['direccion']))
                self.tabla_bolefac.setItem(i,5, QTableWidgetItem(r['total']))
                i=i+1
                temp=False
          if(temp):
              self.tabla_bolefac.setRowCount(0)
    def itemChanged(self):
        self.tipo_busco.clear()

        list1 = [self.tr('Fecha')]
        list2 = [self.tr('Fecha'),self.tr('DNI')]
        list3 = [self.tr('Fecha'),self.tr('RUC')]

        if(self.tipo_bolefac.currentText()=='Ambos'):
            self.tipo_busco.addItems(list1)
        elif(self.tipo_bolefac.currentText()=='Boletas'):
            self.tipo_busco.addItems(list2)
        else:
            self.tipo_busco.addItems(list3)

    def ver_bolefac(self):
        bolefac=(self.tipo_bolefac.currentText())
        tipo_b=(self.tipo_busco.currentText())
        if(bolefac =='Boletas' and tipo_b=='Fecha'):
          self.tabla_bolefac.horizontalHeaderItem(3).setText("DNI");
          self.busca_por_fecha('b')
        elif(bolefac =='Facturas' and tipo_b=='Fecha'):
          self.tabla_bolefac.horizontalHeaderItem(3).setText("RUC");
          self.busca_por_fecha('f')
        elif(bolefac =='Boletas' and tipo_b=='DNI'):
          self.tabla_bolefac.horizontalHeaderItem(3).setText("DNI");
          self.busca_por_dni_ruc('b')
        elif(bolefac =='Facturas' and tipo_b=='RUC'):
          self.tabla_bolefac.horizontalHeaderItem(3).setText("RUC");
          self.busca_por_dni_ruc('f')
        elif(bolefac =='Ambos' and tipo_b=='Fecha'):
          self.busca_por_fecha('Ambos')

#Instancia para iniciar una aplicación
app = QApplication(sys.argv)
_ventana = Administrador()
_ventana.show()
app.exec_()
