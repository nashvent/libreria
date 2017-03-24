import sys
import csv
import os
from PyQt5.QtWidgets import QFileDialog,QFileDialog,QMessageBox,QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout, QPushButton,QHBoxLayout,QDialog
from PyQt5 import uic
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDate
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui, QtCore
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pdfkit
import time

class Interfaz(object):
    def closeEvent(self, event):
        resultado = QMessageBox.question(self, "Salir...", "¿Seguro que quiere salir del Administrador?", QMessageBox.Yes | QMessageBox.No)
        if resultado == QMessageBox.Yes: event.accept()
        else: event.ignore()

class Administrador(QMainWindow,Interfaz):
    ruta = ""
    fichero_actual = ""
    boletasFacturas = 'productos/boletas_y_facturas.csv'
    productosCSV = 'productos/productos.csv'

    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("ui/admin.ui", self)
        self.reportes_totales()
        self.lb_titulo.setStyleSheet("background: #FACC2E")
        self.btn_act.clicked.connect(self.reportes_totales)
        self.tipo_bolefac.currentTextChanged.connect(self.itemChanged)
        self.btn_agregar.clicked.connect(self.agregar_producto)
        self.btn_buscar.clicked.connect(self.ver_productos)
        self.tabla_productos.doubleClicked.connect(self.on_click)
        self.btn_editar.clicked.connect(self.cambio_datos)
        self.btn_eliminar.clicked.connect(self.eliminar)
        self.ini_fecha.setDate(QDate.currentDate())
        self.fin_fecha.setDate(QDate.currentDate())
        self.fi_fecha.setDate(QDate.currentDate())
        self.ff_fecha.setDate(QDate.currentDate())
        self.btn_bolefac.clicked.connect(self.ver_bolefac)
        self.btn_graficar_fd.clicked.connect(self.facturas_por_dia)
        self.btn_totalvg.clicked.connect(self.venta_vs_ganan)
        self.btn_mv.clicked.connect(self.mas_vendidos)
        self.btn_mev.clicked.connect(self.menos_vendidos)
        self.btn_agotados.clicked.connect(self.mas_agotados)
        self.btn_abrir.clicked.connect(self.abrir)
        self.btn_pdf.clicked.connect(self.generarDoc)
        self.btn_ver.clicked.connect(self.ver)
        self.btn_guardarc.clicked.connect(self.configuracion)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tabla_productos.selectedItems():
            self.select_producto(currentQTableWidgetItem.row())
    #Agregar Productos
    def agregar_producto(self):
        p2=[]
        with open(self.productosCSV) as csvarchivo:
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
          p2.append({'codigo':a_codigo, 'nombre':a_nombre,'stock':str(a_stock),
            'precio_compra':str(a_precio_compra),'precio_venta':str(a_precio_venta),
            'descripcion':a_descripcion,'ganancia':str(float(a_precio_venta)-float(a_precio_compra)),'contador':'0'});
        else:
          QMessageBox.critical(self, "ALERTA", "Este código de producto ya está usado.", QMessageBox.Ok)
          return

        toCSV = p2
        keys = toCSV[0].keys()
        with open(self.productosCSV, 'w') as output_file:
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
        with open(self.productosCSV) as csvarchivo:
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
                r['ganancia']=e_precio_venta- e_precio_compra
                break
            toCSV = p2
            keys = toCSV[0].keys()
            with open(self.productosCSV, 'w') as output_file:
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
        self.e_descripcion.setText(self.tabla_productos.item(fila,6).text())
    
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
        with open(self.productosCSV) as csvarchivo:
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
                self.tabla_productos.setItem(i,5, QTableWidgetItem(r['ganancia']))
                self.tabla_productos.setItem(i,6, QTableWidgetItem(r['descripcion']))
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
        with open(self.productosCSV) as csvarchivo:
          entrada  = csv.DictReader(csvarchivo)
          for reg in entrada:
              p2.append(reg)
        for r in p2:
          if  r['codigo'] ==  cod_borrar:
            p2.remove(r)
            toCSV = p2
            keys = toCSV[0].keys()
            with open(self.productosCSV, 'w') as output_file:
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
        aniox=x[-4:]

        diay=y[1:3]
        mesy=y[4:-5]
        anioy=y[-4:]

        if aniox<anioy:
          return True
        elif aniox==anioy:
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
         with open(self.boletasFacturas) as csvarchivo:
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
        with open(self.boletasFacturas) as csvarchivo:
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
    
    #Reportes
    def sacar_fecha(self,fechas):
      i=0
      while i<len(fechas):
        fechas[i]=fechas[i][1:7]+fechas[i][-2:]
        i=i+1
      return fechas

    def graficar(self,fechas,cantidad):
      numbars = len(fechas)
      width = .75
      fechas=self.sacar_fecha(fechas)
      plt.barh(range(numbars), cantidad, width, align='center')
      plt.xlabel('N° de Ventas')
      plt.yticks(range(numbars), fechas)
      plt.grid()
      plt.show()

    def graficar2(self,fechas,cantidad,ganan):
      numbars = len(fechas)
      width = .75
      fechas=self.sacar_fecha(fechas)
      plt.barh(range(numbars), cantidad, width, align='center')
      plt.barh(range(numbars), ganan, width, align='center')
      plt.xlabel('Azul: Total de Venta         Naranja: Total de Ganancia')
      plt.yticks(range(numbars), fechas)
      plt.grid()
      plt.show()

    def numero_veces(self,fecha):
      cont=0
      cant=0
      gan=0
      with open(self.boletasFacturas) as archivo:
        product  = csv.DictReader(archivo)
        for n in product:
          if fecha==n['fecha']:
            cont=cont+1
            cant=cant+float(n['total'])
            gan=gan+float(n['ganancia'])
      return cont,cant,gan
    def ver(self):
        i=0
        temp_fecha=''
        nuevo=True
        fecha_ini='/'+self.fi_fecha.date().toString('dd/MM/yyyy')
        fecha_fin='/'+self.ff_fecha.date().toString('dd/MM/yyyy')
        if (self.compara_fechas(fecha_ini,fecha_fin)):
          with open(self.boletasFacturas) as csvarchivo:
            cpd_product  = csv.DictReader(csvarchivo)
            for r in cpd_product:
              if( self.compara_fechas(fecha_ini,r['fecha']) and self.compara_fechas(r['fecha'],fecha_fin)):
                if (nuevo or (temp_fecha!=r['fecha'] and temp_fecha!='')):
                  temp_fecha=r['fecha']
                  self.tabla_ventas_dia.setRowCount(i+1)
                  self.tabla_ventas_dia.setItem(i,0, QTableWidgetItem(r['fecha']))
                  cont,cant,gan=self.numero_veces(r['fecha'])
                  self.tabla_ventas_dia.setItem(i,1, QTableWidgetItem(str(cont)))
                  self.tabla_ventas_dia.setItem(i,2, QTableWidgetItem('S/. '+str(cant)))
                  self.tabla_ventas_dia.setItem(i,3, QTableWidgetItem('S/. '+str(gan)))
                  i=i+1
                  nuevo=False
        else:
          QMessageBox.critical(self, "ALERTA", "Ingrese correctamente la fecha", QMessageBox.Ok)   	

    def facturas_por_dia(self,tip=False):
        i=0
        fechas=[]
        cantidad=[]
        tventas=[]
        tganan=[]
        tam= self.tabla_ventas_dia.rowCount()
        while i<tam:
        	if(tip):
        		tv=self.tabla_ventas_dia.item(i,2).text()
        		tg=self.tabla_ventas_dia.item(i,3).text()
        		tventas.append(float(tv[4:]))
        		tganan.append(float(tg[4:]))
	        fv=self.tabla_ventas_dia.item(i,0).text()
	        cv=self.tabla_ventas_dia.item(i,1).text()
	        fechas.append(fv)
	        cantidad.append(float(cv))
	        i=i+1
        if(tip):
        	self.graficar2(fechas,tventas,tganan)
        else:
        	self.graficar(fechas,cantidad)
        
    def venta_vs_ganan(self):
      self.facturas_por_dia(True)

    def llenar_top(self,p):
      nombre=[]
      masv=[]
      i=0
      while i<10:
        self.tabla_top.setRowCount(i+1)
        self.tabla_top.setItem(i,0, QTableWidgetItem(str(p['codigo'][i])))
        self.tabla_top.setItem(i,1, QTableWidgetItem(p['nombre'][i]))
        self.tabla_top.setItem(i,2, QTableWidgetItem(str(p['contador'][i])))
        nombre.append(p['nombre'][i])
        masv.append(p['contador'][i])
        i=i+1
      return nombre,masv

    def mas_vendidos(self):
        f = open(self.productosCSV,'rU')
        products = pd.read_csv(f)
        top="Top 10 más Vendidos"
        p=products.sort_values(by=['contador'],ascending=[False]).head(10)
        p=p.reset_index(drop=True)
        nombre,masv=self.llenar_top(p)
        plt.pie(masv, labels=nombre, autopct='%1.1f%%')
        plt.title(top, bbox={"facecolor":"0.8", "pad":5})
        plt.legend()
        plt.show()
    
    def menos_vendidos(self):
        f = open(self.productosCSV,'rU')
        products = pd.read_csv(f)
        top="Top 10 menos Vendidos"
        p=products.sort_values(by=['contador'],ascending=[True]).head(10)
        p=p.reset_index(drop=True)
        nombre,masv=self.llenar_top(p)
        numbars = len(nombre)
        plt.barh(range(numbars), masv, .75, align='center')
        plt.xlabel(top)
        plt.yticks(range(numbars), nombre)
        plt.show()


    #top 10 mas agotados
    def mas_agotados(self):
        f = open(self.productosCSV,'rU')
        products = pd.read_csv(f)
        p=products.sort_values(by=['stock'],ascending=[True]).head(10)
        p=p.reset_index(drop=True)
        nombre=[]
        masv=[]
        i=0
        while i<10:
          self.tabla_agotados.setRowCount(i+1)
          self.tabla_agotados.setItem(i,0, QTableWidgetItem(str(p['codigo'][i])))
          self.tabla_agotados.setItem(i,1, QTableWidgetItem(p['nombre'][i]))
          self.tabla_agotados.setItem(i,2, QTableWidgetItem(str(p['stock'][i])))
          nombre.append(p['nombre'][i])
          masv.append(p['stock'][i])
          i=i+1
        numbars = len(nombre)
        plt.barh(range(numbars), masv, .75, align='center')
        plt.xlabel('Top 10 Productos más Agotados')
        plt.yticks(range(numbars), nombre)
        plt.show()
    
    # conteo total de reportes
    def reportes_totales(self):
      nv=0
      tv=0
      tg=0
      cp=0
      with open(self.boletasFacturas) as csvarchivo:
        cpd_product  = csv.DictReader(csvarchivo)
        for r in cpd_product:
          nv=nv+1
          tv=tv+float(r['total'])
          tg=tg+float(r['ganancia'])

      with open(self.productosCSV) as csvarchivo:
        cpd_product  = csv.DictReader(csvarchivo)
        for n in cpd_product:
          if(n['codigo']!=''):
            cp=cp+1
      self.n_ventas.setText(str(nv))
      self.total_v.setText('S/. '+str(tv))
      self.total_g.setText('S/. '+str(tg))
      self.n_product.setText(str(cp))


    #abrir logo
    def abrir(self):

        filename = QFileDialog.getOpenFileName(self, 'Open file','/home')
        
        #Se define la imagen en la etiqueta
        #pixmap = QPixmap("%s" %self.filename)
        #self.logito.setPixmap(pixmap)

    def generarDoc(self):    
        #archi=open('datos.html','w')

        archivoActual='documentos/reporte/actual.txt'
        #archivoRegistro=archivoRegistro+self.fechaDocumento.date().toString("dd-MM-yyyy")+'-'+time.strftime('%H-%M-%S')+'.txt
        datos=''
        #print(archivoRegistro)
        archi=open(archivoActual,'w')
        datos=datos+(time.strftime("%d/%m/%Y"))
        datos=datos+(',')
        datos=datos+(self.fi_fecha.date().toString('dd/MM/yyyy'))
        datos=datos+(',')
        datos=datos+(self.ff_fecha.date().toString('dd/MM/yyyy'))
      
        htmlDoc='documentos/reporte/reporte.html'
        pdfDoc='documentos/reporte/reporte.pdf'
        pdf2Doc='documentos\\reporte\\reporte.pdf'
           
        for i in range(self.tabla_ventas_dia.rowCount()):
            datos=datos+(',')
            datos=datos+(self.tabla_ventas_dia.item(i,0).text()[1:])
            datos=datos+(',')
            datos=datos+(self.tabla_ventas_dia.item(i,1).text())
            datos=datos+(',')
            datos=datos+(self.tabla_ventas_dia.item(i,2).text())
            datos=datos+(',')
            datos=datos+(self.tabla_ventas_dia.item(i,3).text())

        archi.write(datos)
        archi.close()
        pdfkit.from_file(htmlDoc,pdfDoc)
        os.startfile(pdf2Doc)

    def configuracion(self):
    	datos=self.nombre_empresa.text()+','+self.rubro.text()+','+self.nombre_titular.text()+','+self.direccion.text()
    	datos+=',R.U.C. '
    	datos+=self.ruc.text()
    	datosr=self.nombre_empresa.text()+',R.U.C. '+self.ruc.text()
    	archivoActual='documentos/boletas/template/datos.txt'
    	archivoActual2='documentos/boletas/template/datos.txt'
    	archivoActual3='documentos/reporte/datos.txt'
    	archi=open(archivoActual,'w')
    	archi.write(datos)
    	archi.close()
    	archi1=open(archivoActual2,'w')
    	archi1.write(datos)
    	archi1.close()
    	archi2=open(archivoActual3,'w')
    	archi2.write(datosr)
    	archi2.close()
    
