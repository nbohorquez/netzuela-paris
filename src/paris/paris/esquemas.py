'''
Created on 28/02/2012

@author: Nestor
'''
from pyramid.decorator import reify
from spuria import (CLIENTE, INVENTARIO_RECIENTE, PRODUCTO, TIENDA, CLIENTE_REDUCIDO, PRODUCTO_REDUCIDO)
    
class Esquemas(object):
    def __init__(self):
        '''
        Constructor
        '''

    @reify
    def columnas_inventario(self):
        columnas = INVENTARIO_RECIENTE[:]
        return columnas

    @reify
    def columnas_cliente(self):
        columnas = CLIENTE[:]
        return columnas
    
    @reify
    def columnas_cliente_reducido(self):
        columnas = CLIENTE_REDUCIDO[:]
        return columnas
    
    @reify
    def columnas_producto(self):
        columnas = PRODUCTO[:]
        return columnas
    
    @reify
    def columnas_producto_reducido(self):
        columnas = PRODUCTO_REDUCIDO[:]
        return columnas
    
    @reify
    def columnas_tienda(self):
        columnas = TIENDA[:]
        return columnas
    
    
        