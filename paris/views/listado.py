# -*- coding: utf-8 -*-
'''
Created on 09/04/2012

@author: nestor
'''

from paris.comunes import Comunes
from paris.constantes import MENSAJE_DE_ERROR
from paris.diagramas import Diagramas
from paris.models.spuria import (
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
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPNotFound
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from sqlalchemy import and_, func
from sqlalchemy.orm import aliased

# Aptana siempre va a decir que las clases de spuria (tienda, producto, etc) no estan 
# definidas explicitamente en ninguna parte. Lo que ocurre es que yo las cargo de forma 
# dinamica cuando inicia la aplicacion.

t = aliased(tienda)
c = aliased(cliente)
u = aliased(usuario)
i = aliased(inventario_reciente)
p = aliased(producto)

class ListadoView(Diagramas, Comunes):
    def __init__(self, peticion):
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
        tmp = DBSession.query(territorio.territorio_padre).\
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
            trr_sub = DBSession.query(territorio).\
            join(c, territorio.territorio_id == c.ubicacion).\
            join(t, t.cliente_p == c.rif).\
            filter(and_(
                c.categoria.contains(self.categoria_base),
                c.ubicacion.contains(self.territorio_base)
            )).subquery()
        elif self.subtipo_de_peticion == 'Productos':
            trr_sub = DBSession.query(territorio).\
            join(c, territorio.territorio_id == c.ubicacion).\
            join(t, c.rif == t.cliente_p).\
            join(i, t.tienda_id == i.tienda_id).\
            join(p, i.producto_id == p.producto_id).\
            filter(and_(
                p.categoria.contains(self.categoria_base),
                c.ubicacion.contains(self.territorio_base)
            )).subquery()
        
        trr = aliased(territorio, trr_sub)
        
        territorios = DBSession.query(territorio).\
        filter(and_(
            territorio.territorio_padre == self.territorio_id,
            territorio.territorio_padre != territorio.territorio_id,
            trr.territorio_id.contains(func.replace(territorio.territorio_id, '.00', ''))
        )).all()
        
        return set(territorios)
    
    @reify
    def ruta_territorio_actual(self):
        return self.obtener_ruta_territorio(self.territorio_id)
    
    @reify
    def categorias_hijas(self):
        if self.subtipo_de_peticion == 'Tiendas':   
            cat_sub = DBSession.query(categoria).\
            join(c, categoria.categoria_id == c.categoria).\
            join(t, c.rif == t.cliente_p).\
            filter(and_(
                c.categoria.contains(self.categoria_base),
                c.ubicacion.contains(self.territorio_base)
            )).subquery()
        elif self.subtipo_de_peticion == 'Productos':
            cat_sub = DBSession.query(categoria).\
            join(p, categoria.categoria_id == p.categoria).\
            join(i, p.producto_id == i.producto_id).\
            join(t, i.tienda_id == t.tienda_id).\
            join(c, t.cliente_p == c.rif).\
            filter(and_(
                p.categoria.contains(self.categoria_base),
                c.ubicacion.contains(self.territorio_base)
            )).subquery()
            
        cat = aliased(categoria, cat_sub)        
        categorias = DBSession.query(categoria).\
        filter(and_(
            categoria.hijo_de_categoria == self.categoria_id,
            categoria.hijo_de_categoria != categoria.categoria_id,
            cat.categoria_id.contains(func.replace(categoria.categoria_id, '.00', ''))
        )).all()
        
        return set(categorias)

    @reify
    def ruta_categoria_actual(self):
        return self.obtener_ruta_categoria(self.categoria_id)
    
    @view_config(route_name='productos', renderer='../plantillas/listado.pt')
    def listado_productos_view(self):
        # Este metodo me permite saber rapidamente si una
        # categoria o territorio es hijo de otro(a).        
        productos = DBSession.query(p).\
        join(i, p.producto_id == i.producto_id).\
        join(t, i.tienda_id == t.tienda_id).\
        join(c, t.cliente_p == c.rif).\
        filter(and_(
            p.categoria.contains(self.categoria_base),
            c.ubicacion.contains(self.territorio_base)
        )).all()
        
        self.subtipo_de_peticion = 'Productos'
        return {'pagina': self.subtipo_de_peticion, 'lista': productos, 'autentificado': authenticated_userid(self.peticion)}
    
    @view_config(route_name='tiendas', renderer='../plantillas/listado.pt')
    def listado_tiendas_view(self):
        t_sub = DBSession.query(t).\
        join(c, t.cliente_p == c.rif).\
        filter(and_(
            c.categoria.contains(self.categoria_base),
            c.ubicacion.contains(self.territorio_base)
        )).subquery()
        
        tie = aliased(tienda, t_sub)
        tiendas = DBSession.query(tie).all()
        
        self.subtipo_de_peticion = 'Tiendas'        
        return {'pagina': self.subtipo_de_peticion, 'lista': set(tiendas), 'autentificado': authenticated_userid(self.peticion)}
    
    @view_config(route_name="territorio_coordenadas", renderer="json")
    def territorio_coordenadas_view(self):
        nivel_terr = DBSession.query(territorio.nivel).filter_by(territorio_id = self.territorio_id).first()[0]
        
        if nivel_terr + int(self.nivel) < 0:
            return HTTPNotFound(MENSAJE_DE_ERROR)
        
        terrs = DBSession.query(territorio.dibujable_p, territorio.nombre, territorio.territorio_id).\
        filter(and_(
            territorio.nivel == nivel_terr + int(self.nivel),
            territorio.territorio_id.contains(self.territorio_base)
        )).all()
        
        resultado = []
        for dibujo, nombre, cedula in terrs:
            poligonos = []
            for crq in DBSession.query(croquis.croquis_id).\
            join(dibujable, croquis.dibujable == dibujable.dibujable_id).\
            filter(dibujable.dibujable_id == dibujo).all():
                poligono = ''
                for lat, lng in DBSession.query(punto.latitud, punto.longitud).\
                join(punto_de_croquis).\
                join(croquis).\
                filter_by(croquis_id = crq[0]).all():
                    poligono += "{0}:{1} ".format(str(lat),str(lng))
                poligonos.append(poligono.strip(' '))
            resultado.append({'nombre': nombre.decode('latin-1'), 'id': cedula, 'poligonos': poligonos})

        return { 'territorios': resultado }