import csv, operator

def actualizarListaProductos():
    productos=[]
    with open('productos/productos.csv') as csvarchivo:
        entrada = csv.DictReader(csvarchivo)
        for reg in entrada:
            productos.append(reg)
        return productos
