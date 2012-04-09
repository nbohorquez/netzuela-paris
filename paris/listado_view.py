'''
Created on 09/04/2012

@author: nestor
'''

from .comunes import comunes
from .constantes import MENSAJE_DE_ERROR
from .models import (
    calificable_seguible,
    calificacion_resena,
    categoria,
    cliente,
    consumidor,
    croquis,
    DBSession,
    describible,
    descripcion,
    dibujable,    
    foto,
    horario_de_trabajo,
    inventario_reciente,
    patrocinante,
    producto,
    publicidad,
    punto,
    punto_de_croquis,
    rastreable,
    tamano_reciente,
    territorio,
    tienda,
    turno,
    usuario
)
from .diagramas import diagramas
from pyramid.decorator import reify
from pyramid.httpexceptions import (HTTPNotFound)
from pyramid.view import view_config
from sqlalchemy import and_
from sqlalchemy.orm import aliased
import string

# Aptana siempre va a decir que las clases de spuria (tienda, producto, etc) no estan 
# definidas explicitamente en ninguna parte. Lo que ocurre es que yo las cargo de forma 
# dinamica cuando inicia la aplicacion.

class listado_view(diagramas, comunes):
    def __init__(self, peticion):
        self.peticion = peticion
        self.productos = []
        self.tiendas = []
        self.clientes = []
        if 'categoria_id' in self.peticion.matchdict and 'territorio_id' in self.peticion.matchdict:
            self.categoria_id = self.peticion.matchdict['categoria_id']
            self.territorio_id = self.peticion.matchdict['territorio_id']
        
    @reify
    def peticion(self):
        return self.peticion
        
    @reify
    def categoria_id(self):
        return self.categoria_id
    
    @reify
    def territorio_id(self):
        return self.territorio_id
    
    @reify
    def tipo_de_peticion(self):
        return 'listado'

    @reify
    def territorios_hijos(self):
        ters = DBSession.query(territorio).\
        filter(territorio.territorio_padre == self.categoria_id).all()
        if self.subtipo_de_peticion == 'Productos':
            lista = [t for t in ters for p in self.productos if (c.categoria_id.replace('.00', '') in p.categoria)]
        elif self.subtipo_de_peticion == 'Tiendas':
            lista = [t for t in ters for t in self.clientes if (c.categoria_id.replace('.00', '') in t.categoria)]
        return set(lista)
    
        resultado = DBSession.query(territorio).\
        filter_by(territorio_padre = self.territorio_id).all()
        return resultado
    
    @reify
    def ruta_territorio_actual(self):
        return self.obtener_ruta_territorio(self.territorio_id)
    
    @reify
    def categorias_hijas(self):
        cts = DBSession.query(categoria).\
        filter(and_(
            categoria.hijo_de_categoria == self.categoria_id,
            categoria.categoria_id != categoria.hijo_de_categoria)
        ).all()
        if self.subtipo_de_peticion == 'Productos':
            lista = [c for c in cts for p in self.productos if (c.categoria_id.replace('.00', '') in p.categoria)]
        elif self.subtipo_de_peticion == 'Tiendas':
            lista = [c for c in cts for t in self.clientes if (c.categoria_id.replace('.00', '') in t.categoria)]
        return set(lista)

    @reify
    def ruta_categoria_actual(self):
        return self.obtener_ruta_categoria(self.categoria_id)
    
    @view_config(route_name='productos', renderer='plantillas/listado.pt')
    def listado_productos_view(self):
        i = aliased(inventario_reciente)
        p = aliased(producto)
        t = aliased(tienda)
        c = aliased(cliente)
        u = aliased(usuario)
        
        # Este metodo me permite saber rapidamente si una
        # categoria o territorio es hijo de otro(a).
        cat = self.categoria_id.replace('.00', '')
        terr = self.territorio_id.replace('.00', '')
        
        self.productos = DBSession.query(p).\
        join(i, p.producto_id == i.producto_id).\
        join(t, i.tienda_id == t.tienda_id).\
        join(c, t.cliente_p == c.rif).\
        join(u, c.usuario_p == u.usuario_id).\
        filter(and_(
            p.categoria.contains(cat),
            u.ubicacion.contains(terr)
        )).all()
        
        self.subtipo_de_peticion = 'Productos'
        return {'pagina': self.subtipo_de_peticion, 'lista': self.productos}
    
    @view_config(route_name='tiendas', renderer='plantillas/listado.pt')
    def listado_tiendas_view(self):
        t = aliased(tienda)
        c = aliased(cliente)
        u = aliased(usuario)
        
        cat = self.categoria_id.replace('.00', '')
        terr = self.territorio_id.replace('.00', '')
        
        for a, b in DBSession.query(t, c).\
        join(c, t.cliente_p == c.rif).\
        join(u, c.usuario_p == u.usuario_id).\
        filter(and_(
            c.categoria.contains(cat),
            u.ubicacion.contains(terr)
        )).all():
            self.tiendas.append(a)
            self.clientes.append(b)

        self.subtipo_de_peticion = 'Tiendas'
        return {'pagina': self.subtipo_de_peticion, 'lista': self.tiendas}