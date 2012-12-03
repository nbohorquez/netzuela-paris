# -*- coding: utf-8 -*-
'''
Created on 09/04/2012

@author: nestor
'''

from paris.comunes import (
    Comunes
)
from paris.diagramas import Diagramas
from spuria.orm import (
    Categoria,
    Cliente,
    Croquis,
    DBSession,
    Dibujable,
    Inventario,
    Producto,
    Punto,
    PuntoDeCroquis,
    Territorio,
    Tienda,
    Usuario
)
from pyramid.decorator import reify
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from sqlalchemy import and_

# Aptana siempre va a decir que las clases de spuria (Tienda, Producto, etc) no estan 
# definidas explicitamente en ninguna parte. Lo que ocurre es que yo las cargo de forma 
# dinamica cuando inicia la aplicacion.

class ListadoView(Diagramas, Comunes):
    def __init__(self, peticion, *args, **kwargs):
        super(ListadoView, self).__init__(peticion=peticion, *args, **kwargs)
        self.tiendas = None
        self.productos = None

        if 'categoria_id' in self.peticion.matchdict: 
            self.categoria_id = self.peticion.matchdict['categoria_id']
        if 'territorio_id' in self.peticion.matchdict:
            self.territorio_id = self.peticion.matchdict['territorio_id']

    @reify
    def tipo_de_peticion(self):
        return 'listado'
    
    @reify 
    def territorio_padre(self):
        tmp = DBSession.query(Territorio.territorio_padre_id).\
        filter_by(territorio_id = self.territorio_id).first()
        return tmp[0] if (tmp is not None) else None
    
    @view_config(route_name='productos', renderer='../plantillas/listado.pt')
    def listado_productos_view(self):
        # Este metodo me permite saber rapidamente si una
        # categoria o territorio es hijo de otro(a).
        self.productos = DBSession.query(Producto).\
        join(Inventario).\
        join(Tienda).\
        filter(and_(
            Producto.categoria_id.contains(self.categoria_base),
            Tienda.ubicacion_id.contains(self.territorio_base)
        )).all()
        
        self.subtipo_de_peticion = 'productos'
        return {
            'pagina': self.subtipo_de_peticion.capitalize(), 
            'lista': self.productos, 
            'autentificado': authenticated_userid(self.peticion)
        }
    
    @view_config(route_name='tiendas', renderer='../plantillas/listado.pt')
    def listado_tiendas_view(self):
        self.tiendas = DBSession.query(Tienda).\
        filter(and_(
            Tienda.categoria_id.contains(self.categoria_base),
            Tienda.ubicacion_id.contains(self.territorio_base)
        )).all()
        
        self.subtipo_de_peticion = 'tiendas'
        return {
            'pagina': self.subtipo_de_peticion.capitalize(), 
            'lista': self.tiendas, 
            'autentificado': authenticated_userid(self.peticion)
        }