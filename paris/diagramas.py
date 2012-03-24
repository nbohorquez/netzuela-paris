'''
Created on 28/02/2012

@author: Nestor
'''

from pyramid.decorator import reify
from pyramid.renderers import get_renderer
from constantes import (CLIENTE, INVENTARIO_RECIENTE, PRODUCTO, CLIENTE_REDUCIDO, PRODUCTO_REDUCIDO)
    
class diagramas(object):
    def __init__(self):
        '''
        Constructor
        '''

    @reify
    def diagrama_global(self):
        renderer = get_renderer("plantillas/global.pt")
        return renderer.implementation().macros['diagrama']
    
    @reify
    def macros(self):
        renderer = get_renderer("plantillas/macros.pt")
        return renderer.implementation().macros

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
