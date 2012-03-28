'''
Created on 28/02/2012

@author: Nestor
'''

from pyramid.decorator import reify
from pyramid.renderers import get_renderer
from constantes import (CLIENTE, INVENTARIO_RECIENTE, PRODUCTO)
    
class diagramas(object):
    def __init__(self):
        pass

    @reify
    def diagrama_global(self):
        renderer = get_renderer("plantillas/global.pt")
        return renderer.implementation().macros['diagrama']
    
    @reify
    def macros(self):
        renderer = get_renderer("plantillas/macros.pt")
        return renderer.implementation().macros

    @reify
    def columnas_inventario_tienda(self):
        resultado = []
        for columna in INVENTARIO_RECIENTE[:]:
            if columna != 'tienda_id':
                mostrar = columna.replace('_', ' ').capitalize()
                resultado.append({'db': columna, 'bonito': mostrar})
        return resultado
    
    @reify
    def columnas_inventario_producto(self):
        resultado = []
        for columna in INVENTARIO_RECIENTE[:]:
            if columna != 'producto_id':
                mostrar = columna.replace('_', ' ').capitalize()
                resultado.append({'db': columna, 'bonito': mostrar})
        return resultado

    @reify
    def columnas_cliente(self):
        columnas = CLIENTE[:]
        return columnas
    
    @reify
    def columnas_producto(self):
        columnas = PRODUCTO[:]
        return columnas