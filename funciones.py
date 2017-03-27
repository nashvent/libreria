#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv, operator

def actualizarListaProductos():
    productos=[]
    with open('productos/productos.csv') as csvarchivo:
        entrada = csv.DictReader(csvarchivo)
        for reg in entrada:
            productos.append(reg)
        return productos

def posABC(letra):
    abc='ABCDEFGHIJKLMNÑOPQRSTUVWXYZabcdefghijklmnñopqrstuvwxyz123456789'
    for i in range(len(abc)):
        if(letra==abc[i]):
            return i

def cifrar(contra):
    abc='ABCDEFGHIJKLMNÑOPQRSTUVWXYZabcdefghijklmnñopqrstuvwxyz123456789'
    clave=3
    contraC=''
    for i in range(len(contra)):
        contraC=contraC+(abc[(posABC(contra[i])+clave)%len(abc)])
    return contraC

def descifrar(contra):
    abc='ABCDEFGHIJKLMNÑOPQRSTUVWXYZabcdefghijklmnñopqrstuvwxyz123456789'
    clave=3
    contraC=''
    for i in range(len(contra)):
        contraC=contraC+(abc[(posABC(contra[i])-clave)%len(abc)])
    return contraC


def comprobar(clave,claveC):
    if(cifrar(clave)==claveC):
        return True
    else:
        return False
