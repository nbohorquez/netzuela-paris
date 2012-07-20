# -*- coding: utf-8 -*-
'''
Created on 08/04/2012

@author: nestor
'''

from .comunes import Comunes
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
    registro,
    tamano_reciente,
    territorio,
    tienda,
    turno,
    usuario
)
from .diagramas import Diagramas
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
    def inventario_reciente(self):
        var_inventario = DBSession.query(inventario_reciente).\
        filter_by(producto_id = self.producto_id).all()
        
        resultado = [{""}] if (var_inventario is None) else var_inventario
        return resultado

    @reify
    def registro(self):
        r = aliased(rastreable)
        p = aliased(producto)
        
        resultado = []
        for reg in DBSession.query(registro).\
        join(r, or_(registro.actor_activo == r.rastreable_id, registro.actor_pasivo == r.rastreable_id)).\
        join(p, r.rastreable_id == p.rastreable_p).\
        filter(p.producto_id == self.producto_id).all():
            resultado.append(self.formatear_entrada_registro(reg, self.peticion))

        return resultado
    
    @reify
    def descripciones(self):
        var_descripciones = DBSession.query(descripcion).\
        join(describible).\
        join(producto).\
        filter(producto.producto_id == self.producto_id).all()
        
        resultado = [ {'contenido': ""} ] if var_descripciones is None else var_descripciones
        return resultado
    
    @reify
    def calificaciones_resenas(self):
        var_comentarios = DBSession.query(calificacion_resena).\
        join(calificable_seguible).\
        join(producto).\
        filter(producto.producto_id == self.producto_id).all()
        
        return [{""}] if var_comentarios is None else self.formatear_comentarios(var_comentarios) 
    
    @reify
    def fotos_grandes(self):
        var_fotos = self.obtener_fotos(self.tipo_de_peticion, self.peticion_id, 'grandes')
        resultado = [{'ruta_de_foto': ''}] if (var_fotos is None) else var_fotos
        return resultado
    
    @reify
    def fotos_medianas(self):
        var_fotos = self.obtener_fotos(self.tipo_de_peticion, self.peticion_id, 'medianas')
        resultado = [{'ruta_de_foto': ''}] if (var_fotos is None) else var_fotos
        return resultado
    
    @reify
    def fotos_pequenas(self):
        var_fotos = self.obtener_fotos(self.tipo_de_peticion, self.peticion_id, 'pequenas')
        resultado = [{'ruta_de_foto': ''}] if (var_fotos is None) else var_fotos
        return resultado
    
    @reify
    def fotos_miniaturas(self):
        var_fotos = self.obtener_fotos(self.tipo_de_peticion, self.peticion_id, 'miniaturas')
        resultado = [{'ruta_de_foto': ''}] if (var_fotos is None) else var_fotos
        return resultado
    
    @reify
    def ruta_categoria_actual(self):
        cat_padre = DBSession.query(producto.categoria).\
        filter_by(producto_id = self.peticion_id).one()[0]        
        return self.obtener_ruta_categoria(cat_padre)
        
    @view_config(route_name='producto', renderer='plantillas/producto.pt')
    def producto_view(self):
        var_producto = self.obtener_producto(self.producto_id)
        resultado = HTTPNotFound(MENSAJE_DE_ERROR) \
        if (var_producto is None) \
        else {'pagina': 'Producto', 'producto': var_producto, 'autentificado': authenticated_userid(self.peticion)}
        return resultado