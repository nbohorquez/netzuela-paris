# -*- coding: utf-8 -*-
'''
Created on 08/04/2012

@author: nestor
'''

from formencode.api import Invalid
from paris.comunes import Comunes
from paris.formatos import (
    formatear_comentarios,
    formatear_entrada_noticias,
    formatear_fecha_para_paris
)
from paris.constantes import MENSAJE_DE_ERROR
from paris.diagramas import Diagramas
from paris.models.edicion import editar_producto
from paris.models.constantes import ROOT
from spuria.orm import (
    CalificableSeguible,
    CalificacionResena,
    DBSession,
    Describible,
    Descripcion,
    InventarioReciente,
    Producto,
    Rastreable,
    Registro,
    Inventario,
    Tienda
)
from spuria.orm.descripciones_fotos import DescribibleAsociacion
from spuria.orm.calificaciones_resenas import CalificableSeguibleAsociacion
from spuria.orm.rastreable import RastreableAsociacion
from sqlalchemy import desc, or_, and_
from sqlalchemy.orm import aliased
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from pyramid.security import authenticated_userid
from pyramid.view import view_config
import transaction


# Aptana siempre va a decir que las clases de spuria (tienda, producto, etc) no 
# estan definidas explicitamente en ninguna parte. Esto es porque yo las cargo 
# de forma dinamica cuando inicia la aplicacion.

class ProductoView(Diagramas, Comunes):
    def __init__(self, peticion):
        self.peticion = peticion
        self.pagina_actual = peticion.url
        
        if 'producto_id' in self.peticion.matchdict:
            self.producto_id = self.peticion.matchdict['producto_id']
        if 'territorio_id' in self.peticion.matchdict:
            self.territorio_id = self.peticion.matchdict['territorio_id']
        else:
            self.territorio_id = None

    @reify
    def peticion_id(self):
        return self.producto_id
    
    @reify
    def tipo_de_peticion(self):
        return 'producto'
    
    @property
    def producto(self):
        return self.obtener_producto(self.producto_id)
    
    @reify
    def inventario_reciente(self):
        return DBSession.query(InventarioReciente).\
        join(Tienda, InventarioReciente.tienda_id == Tienda.tienda_id).\
        filter(and_(
            InventarioReciente.producto_id == self.producto_id,
            Tienda.ubicacion_id.contains(self.territorio_base)
        )).all()

    @reify
    def debut_en_el_mercado(self):
        return formatear_fecha_para_paris(
            str(self.producto.debut_en_el_mercado)
        ) if self.producto.debut_en_el_mercado is not None \
        else None
    
    @reify
    def registro(self):
        inventario = DBSession.query(Inventario).\
        join(Tienda).\
        filter(Tienda.ubicacion_id.contains(self.territorio_base)).\
        subquery()
        
        reg1 = DBSession.query(Registro).\
        join(Rastreable, Registro.actor_pasivo_id == Rastreable.rastreable_id).\
        join(RastreableAsociacion).\
        join(inventario).\
        join(Producto).\
        filter(Producto.producto_id == self.producto_id)
        
        reg2 = DBSession.query(Registro).\
        join(Rastreable, or_(
            Registro.actor_activo_id == Rastreable.rastreable_id,
            Registro.actor_pasivo_id == Rastreable.rastreable_id
        )).join(RastreableAsociacion).\
        join(Producto).\
        filter(Producto.producto_id == self.producto_id)
        
        registros = reg1.union(reg2).order_by(desc(Registro.fecha_hora)).\
        limit(10)
        
        noticias = [formatear_entrada_noticias(registro, self.peticion, \
                    self.producto) for registro in registros]
        return noticias
    
    @reify
    def descripciones(self):
        return DBSession.query(Descripcion).\
        join(Describible).\
        join(DescribibleAsociacion).\
        join(Producto).\
        filter(Producto.producto_id == self.producto_id).all()
    
    @reify
    def calificaciones_resenas(self):
        comentarios = DBSession.query(CalificacionResena).\
        join(CalificableSeguible).\
        join(CalificableSeguibleAsociacion).\
        join(Producto).\
        filter(Producto.producto_id == self.producto_id).all()
        
        return formatear_comentarios(comentarios)
    
    @reify
    def ruta_categoria_actual(self):
        return self.obtener_ruta_categoria(self.producto.categoria)
        
    @view_config(route_name='producto', renderer='../plantillas/producto.pt', 
                 request_method='GET')
    @view_config(route_name='producto', renderer='../plantillas/producto.pt', 
                 request_method='POST')
    @view_config(route_name='producto_geo', renderer='../plantillas/producto.pt', 
                 request_method='GET')
    @view_config(route_name='producto_geo', renderer='../plantillas/producto.pt',
                 request_method='POST')
    def producto_view(self):
        editar = False
        aviso = None
        
        if self.territorio_id is None:
            return HTTPFound(location = self.peticion.route_url(
                'producto_geo', producto_id = self.producto_id, 
                territorio_id = '0.02.00.00.00.00'
            ))
        
        if self.producto is None:
            return HTTPNotFound(MENSAJE_DE_ERROR)
        
        autentificado = authenticated_userid(self.peticion)
        
        if autentificado:
            usuario_autentificado = self.obtener_usuario(
                'correo_electronico', autentificado
            )
            editar = True if usuario_autentificado.usuario_id == ROOT else False
            
            if editar and ('guardar' in self.peticion.POST):
                try:
                    with transaction.manager:
                        editar_producto(dict(self.peticion.POST), self.producto)
                    aviso = {
                        'error': 'OK',
                        'mensaje': 'Datos actualizados correctamente'
                    }
                except Invalid as e:
                    aviso = { 'error': 'Error', 'mensaje': e.msg }

        return {
            'pagina': 'Producto', 
            'producto': self.producto, 
            'autentificado': autentificado,
            'aviso': aviso,
            'editar': editar
        }