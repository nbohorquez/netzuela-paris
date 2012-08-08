# -*- coding: utf-8 -*-
'''
Created on 08/04/2012

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
    registro,
    tamano_reciente,
    territorio,
    tienda,
    turno,
    usuario
)
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPNotFound
from pyramid.security import authenticated_userid
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from pyramid.view import view_config

# Aptana siempre va a decir que las clases de spuria (tienda, producto, etc) no estan 
# definidas explicitamente en ninguna parte. Esto es porque yo las cargo de forma 
# dinamica cuando inicia la aplicacion.

class ProductoView(Diagramas, Comunes):
    def __init__(self, peticion):
        self.peticion = peticion
        self.pagina_actual = peticion.url
        if 'producto_id' in self.peticion.matchdict:
            self.producto_id = self.peticion.matchdict['producto_id']

    @reify
    def peticion(self):
        return self.peticion
    
    @reify
    def pagina_actual(self):
        return self.pagina_actual
    
    @reify
    def peticion_id(self):
        return self.producto_id
    
    @reify
    def tipo_de_peticion(self):
        return 'producto'
    
    @reify
    def tipo_de_rastreable(self):
        return 'producto'
    
    @reify
    def inventario_reciente(self):
        return DBSession.query(inventario_reciente).\
        filter_by(producto_id = self.producto_id).all()

    @reify
    def registro(self):
        r = aliased(rastreable)
        p = aliased(producto)
        
        resultado = []
        for reg in DBSession.query(registro).\
        join(r, or_(registro.actor_activo == r.rastreable_id, registro.actor_pasivo == r.rastreable_id)).\
        join(p, r.rastreable_id == p.rastreable_p).\
        filter(p.producto_id == self.producto_id).order_by(registro.fecha_hora.desc()).all():
            resultado.append(self.formatear_entrada_registro(reg, self.peticion, self.tipo_de_rastreable))

        return resultado
    
    @reify
    def descripciones(self):
        return DBSession.query(descripcion).\
        join(describible).\
        join(producto).\
        filter(producto.producto_id == self.producto_id).all()
    
    @reify
    def calificaciones_resenas(self):
        var_comentarios = DBSession.query(calificacion_resena).\
        join(calificable_seguible).\
        join(producto).\
        filter(producto.producto_id == self.producto_id).all()
        
        return self.formatear_comentarios(var_comentarios)
    
    @reify
    def fotos_grandes(self):
        return self.obtener_fotos(self.tipo_de_peticion, self.peticion_id, 'grandes')
    
    @reify
    def fotos_medianas(self):
        return self.obtener_fotos(self.tipo_de_peticion, self.peticion_id, 'medianas')
    
    @reify
    def fotos_pequenas(self):
        return self.obtener_fotos(self.tipo_de_peticion, self.peticion_id, 'pequenas')
    
    @reify
    def fotos_miniaturas(self):
        return self.obtener_fotos(self.tipo_de_peticion, self.peticion_id, 'miniaturas')
    
    @reify
    def ruta_categoria_actual(self):
        cat_padre = DBSession.query(producto.categoria).\
        filter_by(producto_id = self.peticion_id).first()[0]
        return self.obtener_ruta_categoria(cat_padre)
        
    @view_config(route_name='producto', renderer='../plantillas/producto.pt')
    def producto_view(self):
        var_producto = self.obtener_producto(self.producto_id)
        resultado = HTTPNotFound(MENSAJE_DE_ERROR) \
        if (var_producto is None) \
        else {'pagina': 'Producto', 'producto': var_producto, 'autentificado': authenticated_userid(self.peticion)}
        return resultado