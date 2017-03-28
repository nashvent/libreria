from funciones import * ##FUNCIONES CONTIENE TODAS LAS LIBRERIAS NECESARIAS


##Interfaz donde se encuentran los productos a selecionar en pedido
class Lista(QDialog):
    ##LISTA PRINCIPAL USADA POR LA CLASE LISTA-PEDIDO-DOCUMENTO
    productos=actualizarListaProductos()
    ##TODO CAMBIO IMPLICA ACUTALIZAR ESTA LISTA
    
    def __init__(self): #CONSTRUCTOR
        QDialog.__init__(self)#CONSTRUCT DE UI
        uic.loadUi("ui/lista_productos.ui", self)
        self.tableWidget.doubleClicked.connect(self.on_click)
        self.listaTitulo.setStyleSheet("background: #89f9ad")
        self.btn_buscar.clicked.connect(self.ver_productos)
    
    def productoElegido(self): #Funcion usada al hacer doble click sobre celda
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            self.agregarCodigo(currentQTableWidgetItem.row())

    def agregarCodigo(self,cod,cant): ##Funcion que sera redefinida en otro objeto
        print('')
        
    def actualizarLista(self):##Actualizar lista d la interfaz de Lista
        i=0
        self.tableWidget.setRowCount(len(self.productos))
        while(len(self.productos)>i):
            self.tableWidget.setItem(i,0, QTableWidgetItem(self.productos[i]['codigo']))
            self.tableWidget.setItem(i,1, QTableWidgetItem(self.productos[i]['nombre']))
            self.tableWidget.setItem(i,2, QTableWidgetItem(self.productos[i]['precio_venta']))
            self.tableWidget.setItem(i,3, QTableWidgetItem(self.productos[i]['stock']))
            i=i+1

    #Toma el menor de los string para comparar el inicio en otros
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

    #Con filtro busqueda colocaba los resultados en las celdas
    def busqueda(self,busca): 
        i=0
        temp=True
        for r in self.productos:
            if(self.filtro_busqueda(r[busca],self.listaProducto.text())):
                if(r['codigo']!=''):
                    self.tableWidget.setRowCount(i+1)
                    self.tableWidget.setItem(i,0, QTableWidgetItem(r['codigo']))
                    self.tableWidget.setItem(i,1, QTableWidgetItem(r['nombre']))
                    self.tableWidget.setItem(i,2, QTableWidgetItem(r['precio_venta']))
                    self.tableWidget.setItem(i,3, QTableWidgetItem(r['stock']))
                    i=i+1
                    temp=False
        if(temp):
            self.tableWidget.setRowCount(0)

    ##Selecciona el tipo de busqueda que se realizara
    def ver_productos(self):
        tipo_buscar=(self.tipoBusca.currentText())
        if (tipo_buscar=='Nombre'):
          self.busqueda('nombre')
        else:
          self.busqueda('codigo')

    #DEtecta el doble click y llama a la funcion agregarCodigo()
    @pyqtSlot()
    def on_click(self):
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            r=currentQTableWidgetItem.row()
            cod=self.tableWidget.item(r,0).text()
            cant=self.tableWidget.item(r,3).text()
            self.agregarCodigo(cod,cant)
    
#Interfaz objeto que sirve para armar el pedido
class Pedido(QMainWindow):    
    def __init__(self,lista):
        self.lista=lista
        self.tamPedido=0
        self.TotalPedido=0

        #Reasigno funcion dentro del objeto Lista 
        lista.agregarCodigo=self.agregarCodigo

        QMainWindow.__init__(self)
        uic.loadUi("ui/pedido.ui", self)
        self.botonLista.clicked.connect(self.mostrarLista)
        self.botonAgregar.clicked.connect(self.agregarProducto)
        self.quitarProducto.clicked.connect(self.productoRemovido)
        self.cancelarPedido.clicked.connect(self.limpiarPedido)        
        self.lb_titulo.setStyleSheet("background: #98dc12")

    def agregarCodigo(self,cod,cant):
        #Funcion que se asigna en la clase Lista
        self.lineaCodigo.setText(cod)
        self.cantidadPedido.setMaximum(int(cant))
        self.lista.hide()

    #Mostrar Lista pero antes actualizarla    
    def mostrarLista(self):
        self.lista.actualizarLista()
        self.lista.show()

    #Buscar si existe el producto, caso contrario devolver -1
    def PosPorCodigo(self,cod):
        pos=0
        for i in self.lista.productos:
            if i['codigo']==cod :
                break
            pos=pos+1
        if pos==len(self.lista.productos):
            pos=-1
        return pos

    #Agregar producto a la celda de Pedido, en caso no exista lanza alerta
    def agregarProducto(self):
        pos1=self.PosPorCodigo(self.lineaCodigo.text())
        pos=pos1
        cantidad=self.cantidadPedido.value()
        if(pos==-1):
            QMessageBox.warning(self, "ALERTA", "Este codigo de producto no existe.", QMessageBox.Ok)
            self.lineaCodigo.setText('')
            return
        if(self.lista.productos[pos]['stock']=='0'):
            QMessageBox.warning(self, "ALERTA", "Ya no hay stock de "+self.lista.productos[pos]['nombre']+'.', QMessageBox.Ok)
            self.lineaCodigo.setText('')
            return
        else:
            self.tablePedido.setRowCount(self.tamPedido+1)
            self.tablePedido.setItem(self.tamPedido,0,QTableWidgetItem(self.lista.productos[pos]['codigo']))
            self.tablePedido.setItem(self.tamPedido,1,QTableWidgetItem(self.lista.productos[pos]['nombre']))
            self.tablePedido.setItem(self.tamPedido,2,QTableWidgetItem(self.lista.productos[pos]['precio_venta']))
            self.tablePedido.setItem(self.tamPedido,3,QTableWidgetItem(str(cantidad)))
            total=str(float(self.lista.productos[pos]['precio_venta'])*cantidad)
            self.TotalPedido=self.TotalPedido+float(total)
            self.tablePedido.setItem(self.tamPedido,4,QTableWidgetItem(total))
            self.tamPedido=self.tamPedido+1
            self.TotalPedidoLabel.setText('S/.'+str(self.TotalPedido))

    #Permite eliminar productos de las celdas de pedido, actualizando el total
    def productoRemovido(self):
        for currentQTableWidgetItem in self.tablePedido.selectedItems():
            self.TotalPedido=self.TotalPedido-float(self.tablePedido.item(currentQTableWidgetItem.row(),4).text())
            self.TotalPedidoLabel.setText('S/.'+str(self.TotalPedido))
            self.tablePedido.removeRow(currentQTableWidgetItem.row())
            self.tamPedido=self.tamPedido-1
    #Limpia totalmente todos los valores y campos de Pedido
    def limpiarPedido(self):
        self.lineaCodigo.setText('')
        self.TotalPedido=0;
        self.TotalPedidoLabel.setText('S/.'+str(self.TotalPedido))
        self.tamPedido=0
        self.tablePedido.setRowCount(self.tamPedido)
        self.cantidadPedido.setValue(1)


## Clase Documento recibe la informacion depositada en Pedido para pedir datos
## del comprador y generar el documento 
class Documento(QMainWindow): 
    boletasFacturas = 'productos/boletas_y_facturas.csv'
    productosCSV = 'productos/productos.csv'
    def __init__(self,pedido):
        QMainWindow.__init__(self)
        uic.loadUi("ui/documento.ui", self)
        self.pedido=pedido
        self.tipoDocumento.currentTextChanged.connect(self.itemChanged)
        self.fechaDocumento.setDate(QDate.currentDate())
        self.generarDocumento.clicked.connect(self.confirmarDocumento)
        self.editarPedido.clicked.connect(self.mostrarPedido)
        self.igv=0
        self.totalDocumento=0
        self.pedido.enviarPedido.clicked.connect(self.generarPedido)
        self.datosTitulo.setStyleSheet("background: #ffc962")

    #Funcion asignada a boton dentro de la interfaz Pedido
    #Actualiza la tabla de la interfaz Documento o informa que de faltan
    #agregar productos
    def generarPedido(self):
        if(self.pedido.tamPedido>0):
            self.actualizarTabla(self.pedido.tablePedido,self.pedido.TotalPedidoLabel.text())
            self.pedido.hide()
            self.show()
        else:
            QMessageBox.warning(self, "ALERTA", "No agregaste ningun producto.", QMessageBox.Ok)

    #Con los datos de Pedido copia la tabla en otra para confirmar los
    #productos solicitados
    def actualizarTabla(self,lista,total):
        self.tablaVenta.setRowCount(lista.rowCount())
        for i in range(lista.rowCount()):
            for j in range(5):
                self.tablaVenta.setItem(i,j,QTableWidgetItem(lista.item(i,j).text()))
        self.igv=self.pedido.TotalPedido*0.18
        self.totalDocumento=self.pedido.TotalPedido
        self.totalCobro.setText('S/.'+str(self.totalDocumento))
        self.show()

    #En caso de cambio de Boleta o Factura selecciona si se pedira DNI o RUC
    #tambien actualiza el IGV en caso de FACTURA
    def itemChanged(self):
        if(self.tipoDocumento.currentText()=='Factura'):
            self.documentoLabel.setText('RUC:')
            self.igvLabel.setText('S/.'+str(round(self.igv,9)))
        else:
            self.documentoLabel.setText('DNI:')
            self.igvLabel.setText('S/.0.0')

    #Captura los datos de los input y genera el documento
    #txt que servira para armar el pdf del documento final
    #guarda la informacion del documento generado en un csv
    def generarDoc(self):    
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

        BoleFactu.append({'fecha':'/'+self.fechaDocumento.date().toString("dd/MM/yyyy"), 'hora':time.strftime('%H-%M-%S'),'tipo':tipo,'nombre':self.nombreDocumento.text(),'dni_ruc':self.numeroDocumento.text(),'direccion':self.direccionDocumento.text(),'total':str(self.pedido.TotalPedido),'ganancia':str(ganancia),'ubicacion':archivoRegistro});
        toCSV = BoleFactu 
        keys = toCSV[0].keys()
        with open(self.boletasFacturas, 'w') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(toCSV)
       
        self.actualizarStock(listaActualizar)
        self.pedido.limpiarPedido()
        self.mostrarPedido()

    #Al confirmar la generacion del documento regresa a la pantalla de pedido
    #para realizar un Pedido nuevo
    def mostrarPedido(self):
        self.pedido.show()
        self.hide()

    #Actualiza el stock, reduciendo los productos vendidos y modificando
    #otros campos dentro del csv de productos
    def actualizarStock(self,listaVenta):
        productos=[]
        with open(self.productosCSV) as csvarchivo:
            entrada  = csv.DictReader(csvarchivo)
            for reg in entrada:
                productos.append(reg)
        for i in range(len(listaVenta)):
            for j in productos:
                if(listaVenta[i][0]==j['codigo']):
                    j['stock']=str(int(j['stock'])-(int(listaVenta[i][1])))
                    j['contador']=str(int(j['contador'])+(int(listaVenta[i][1])))
                    break
        toCSV = productos
        keys = toCSV[0].keys()
        with open(self.productosCSV, 'w') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(toCSV)
        self.pedido.lista.productos=productos
        self.pedido.lista.actualizarLista()

    #Lanza alerta de confirmacion para generar el Documento, asegurando
    #que todos los datos ingresados son los correctos
    def confirmarDocumento(self):
        resultado = QMessageBox.question(self, "Confirmar Compra", "Esta Seguro que quiere registrar la compra", QMessageBox.Yes | QMessageBox.No)
        if resultado == QMessageBox.Yes: self.generarDoc()

    #Cada venta significa una ganancia, calculada usando la
    #resta de: PrecioVenta-PrecioCompra
    def busGanancia(self,cod,cant):
        productosGanancia=self.pedido.lista.productos
        for i in productosGanancia:
            if(cod==i['codigo']):
                return float(i['precio_compra'])*float(cant)
        
