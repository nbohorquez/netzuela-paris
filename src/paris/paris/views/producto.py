# -*- coding: utf-8 -*-
'''
Created on 08/04/2012

@author: nestor
'''

from paris.comunes import (
    Comunes,
    formatear_comentarios,
    formatear_entrada_registro,
    formatear_fecha_para_paris
)
from paris.constantes import MENSAJE_DE_ERROR
from paris.diagramas import Diagramas
from paris.models.spuria import (
    calificable_seguible,
    calificacion_resena,
    categoria,
    cliente,
    consumidor,
    root,
    croquis,
    DBSession,
    describible,
    descripcion,
    dibujable,
    editar_producto,
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
    
    @property
    def producto(self):
        return self.obtener_producto(self.producto_id)
    
    @reify
    def inventario_reciente(self):
        return DBSession.query(inventario_reciente).\
        filter_by(producto_id = self.producto_id).all()

    @reify
    def debut_en_el_mercado(self):
        return formatear_fecha_para_paris(str(self.producto.debut_en_el_mercado)) \
        if self.producto.debut_en_el_mercado is not None \
        else None
    
    @reify
    def registro(self):
        r = aliased(rastreable)
        p = aliased(producto)
        
        resultado = []
        for reg in DBSession.query(registro).\
        join(r, or_(
            registro.actor_activo == r.rastreable_id, 
            registro.actor_pasivo == r.rastreable_id
        )).\
        join(p, r.rastreable_id == p.rastreable_p).\
        filter(p.producto_id == self.producto_id).\
        order_by(registro.fecha_hora.desc()).all():
            resultado.append(formatear_entrada_registro(
                reg, self.peticion, self.tipo_de_rastreable
            ))

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
        
        return formatear_comentarios(var_comentarios)
    
    @reify
    def ruta_categoria_actual(self):
        cat_padre = DBSession.query(producto.categoria).\
        filter_by(producto_id = self.peticion_id).first()[0]
        return self.obtener_ruta_categoria(cat_padre)
        
    @view_config(route_name='producto', renderer='../plantillas/producto.pt', request_method='GET')
    @view_config(route_name='producto', renderer='../plantillas/producto.pt', request_method='POST')
    def producto_view(self):
        editar = False
        aviso = None
        
        if self.producto is None:
            return HTTPNotFound(MENSAJE_DE_ERROR)
        
        autentificado = authenticated_userid(self.peticion)
        
        if autentificado:
            usuario_autentificado = self.obtener_usuario('correo_electronico', autentificado)
            editar = True if usuario_autentificado.usuario_id == root else False
                        
            if editar and ('guardar' in self.peticion.POST):
                error = editar_producto(dict(self.peticion.POST), self.producto_id)
                aviso = { 'error': 'Error', 'mensaje': error } \
                if (error is not None) \
                else { 'error': 'OK', 'mensaje': 'Datos actualizados correctamente' }
            
        return {
            'pagina': 'Producto', 
            'producto': self.producto, 
            'autentificado': autentificado,
            'aviso': aviso,
            'editar': editar
        }