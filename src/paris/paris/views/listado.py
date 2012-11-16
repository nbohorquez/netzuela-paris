# -*- coding: utf-8 -*-
'''
Created on 09/04/2012

@author: nestor
'''

from paris.comunes import (
    Comunes
)
from paris.constantes import MENSAJE_DE_ERROR
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
from pyramid.httpexceptions import HTTPNotFound
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from sqlalchemy import and_, func
from sqlalchemy.orm import aliased

# Aptana siempre va a decir que las clases de spuria (Tienda, Producto, etc) no estan 
# definidas explicitamente en ninguna parte. Lo que ocurre es que yo las cargo de forma 
# dinamica cuando inicia la aplicacion.

t = aliased(Tienda)
c = aliased(Cliente)
u = aliased(Usuario)
i = aliased(Inventario)
p = aliased(Producto)

class ListadoView(Diagramas, Comunes):
    def __init__(self, peticion):
        self.tiendas = None
        self.productos = None
        self.peticion = peticion
        self.pagina_actual = peticion.url
        if 'categoria_id' in self.peticion.matchdict: 
            self.categoria_id = self.peticion.matchdict['categoria_id']
        if 'territorio_id' in self.peticion.matchdict:
            self.territorio_id = self.peticion.matchdict['territorio_id']
        if 'nivel' in self.peticion.matchdict:
            self.nivel = self.peticion.matchdict['nivel']
        
    @reify
    def peticion(self):
        return self.peticion
    
    @reify
    def pagina_actual(self):
        return self.pagina_actual
        
    @reify
    def categoria_id(self):
        return self.categoria_id
    
    @reify
    def categoria_base(self):
        return self.categoria_id.replace('.00', '')
    
    @reify
    def territorio_id(self):
        return self.territorio_id
    
    @reify 
    def territorio_padre(self):
        tmp = DBSession.query(Territorio.territorio_padre_id).\
        filter_by(territorio_id = self.territorio_id).first()
        return tmp[0] if (tmp is not None) else None
    
    @reify
    def territorio_base(self):
        return self.territorio_id.replace('.00', '')

    @reify
    def tipo_de_peticion(self):
        return 'listado'

    @reify
    def territorios_hijos(self):
        if self.subtipo_de_peticion == 'Tiendas':
            trr_sub = DBSession.query(Territorio).\
            join(Tienda).\
            filter(and_(
                Tienda.categoria_id.contains(self.categoria_base),
                Tienda.ubicacion_id.contains(self.territorio_base)
            )).subquery()
        elif self.subtipo_de_peticion == 'Productos':
            trr_sub = DBSession.query(Territorio).\
            join(Tienda).\
            join(Inventario).\
            join(Producto).\
            filter(and_(
                Producto.categoria_id.contains(self.categoria_base),
                Tienda.ubicacion_id.contains(self.territorio_base)
            )).subquery()
        
        trr = aliased(Territorio, trr_sub)
        
        territorios = DBSession.query(Territorio).\
        filter(and_(
            Territorio.territorio_padre_id == self.territorio_id,
            Territorio.territorio_padre_id != Territorio.territorio_id,
            trr.territorio_id.contains(
                func.replace(Territorio.territorio_id, '.00', '')
            )
        )).all()
        
        return territorios
    
    @reify
    def ruta_territorio_actual(self):
        return self.obtener_ruta_territorio(
            self.obtener_territorio(self.territorio_id)
        )
    
    @reify
    def categorias_hijas(self):
        if self.subtipo_de_peticion == 'Tiendas':
            cat_sub = DBSession.query(Categoria).\
            join(Tienda).\
            filter(and_(
                Tienda.categoria_id.contains(self.categoria_base),
                Tienda.ubicacion_id.contains(self.territorio_base)
            )).subquery()
        elif self.subtipo_de_peticion == 'Productos':
            cat_sub = DBSession.query(Categoria).\
            join(Producto).\
            join(Inventario).\
            join(Tienda).\
            filter(and_(
                Producto.categoria_id.contains(self.categoria_base),
                Tienda.ubicacion_id.contains(self.territorio_base)
            )).subquery()
            
        cat = aliased(Categoria, cat_sub)
        categorias = DBSession.query(Categoria).\
        filter(and_(
            Categoria.hijo_de_categoria == self.categoria_id,
            Categoria.hijo_de_categoria != Categoria.categoria_id,
            cat.categoria_id.contains(
                func.replace(Categoria.categoria_id, '.00', '')
            )
        )).all()
        
        return categorias

    @reify
    def ruta_categoria_actual(self):
        return self.obtener_ruta_categoria(
            self.obtener_categoria(self.categoria_id)
        )
    
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
        
        self.subtipo_de_peticion = 'Productos'
        return {
            'pagina': self.subtipo_de_peticion, 
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
        
        self.subtipo_de_peticion = 'Tiendas'
        return {
            'pagina': self.subtipo_de_peticion, 
            'lista': self.tiendas, 
            'autentificado': authenticated_userid(self.peticion)
        }
    
    @view_config(route_name="territorio_coordenadas", renderer="json")
    def territorio_coordenadas_view(self):
        nivel_terr = DBSession.query(Territorio.nivel).\
        filter_by(territorio_id = self.territorio_id).first()[0]
        
        if nivel_terr + int(self.nivel) < 0:
            return HTTPNotFound(MENSAJE_DE_ERROR)

        terrs = DBSession.query(Territorio).\
        filter(and_(
            Territorio.nivel == nivel_terr + int(self.nivel),
            Territorio.territorio_id.contains(self.territorio_base)
        )).all()
        
        resultado = []
        for terr in terrs:
            poligonos = []
            for crq in terr.dibujable.croquis:
                poligono = ''
                for pto in crq.puntos:
                    poligono += "{0}:{1} ".format(
                        str(pto.latitud), str(pto.longitud)
                    )
                poligonos.append(poligono.strip(' '))
            resultado.append({
                'nombre': terr.nombre,
                'id': terr.territorio_id,
                'poligonos': poligonos
            })

        return { 'territorios': resultado }