#!/usr/bin/env python
# -*- coding: utf-8 -*-

##Librerias necesarias para usar PyQt

from PyQt5.QtWidgets import  QWidget, QFileDialog,QFileDialog,QMessageBox,QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout, QPushButton,QHBoxLayout,QDialog
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDate
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui, QtCore
import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd
import time
import shutil
import csv, operator
import pdfkit
import sys
import os

##Funcion que devuelve una lista de productos actualizada
def actualizarListaProductos():
    productos=[]
    with open('productos/productos.csv') as csvarchivo:
        entrada = csv.DictReader(csvarchivo)
        for reg in entrada:
            productos.append(reg)
        return productos


##Abecedario usado para encriptar
abc='ABCDEFGHIJKLMNÑOPQRSTUVWXYZabcdefghijklmnñopqrstuvwxyz123456789'
def posABC(letra): ##Funcion que devuelve la posicion de una letra en el abecedario
    for i in range(len(abc)):
        if(letra==abc[i]):
            return i

def cifrar(contra): ##Algoritmo de cifrado Cesar
    clave=3
    contraC=''
    for i in range(len(contra)):
        contraC=contraC+(abc[(posABC(contra[i])+clave)%len(abc)])
    return contraC

def descifrar(contra): ##Descifrado cesar
    clave=3
    contraC=''
    for i in range(len(contra)):
        contraC=contraC+(abc[(posABC(contra[i])-clave)%len(abc)])
    return contraC


def comprobar(clave,claveC): ##Comprobacion de cifrado 
    if(cifrar(clave)==claveC):
        return True
    else:
        return False

def txtToArray(texto):
    cadena=[]
    j=0
    for i in range(len(texto)):
        if(texto[i]==',' or i+1==len(texto)):
            sub=texto[j:i]
            j=i+1
            cadena.append(sub)
    return cadena
    
