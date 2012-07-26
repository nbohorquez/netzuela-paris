# -*- coding: utf-8 -*-
'''
Created on 20/07/2012

@author: nestor
'''

from .comunes import Comunes
from .constantes import MENSAJE_DE_ERROR
from .diagramas import Diagramas
from .models import (
    calificacion_resena,
    cliente, 
    consumidor,
    DBSession, 
    patrocinante, 
    rastreable, 
    registro, 
    tienda, 
    usuario
)
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPNotFound
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from sqlalchemy import or_
from sqlalchemy.orm import aliased

class UsuarioView(Diagramas, Comunes):
    def __init__(self, peticion):
        self.peticion = peticion
        self.pagina_actual = peticion.url
        if 'usuario_id' in self.peticion.matchdict:
            self.usuario_id = self.peticion.matchdict['usuario_id']
            
    @reify
    def peticion(self):
        return self.peticion
    
    @reify
    def pagina_actual(self):
        return self.pagina_actual
    
    @reify
    def peticion_id(self):
        return self.usuario_id
    
    @reify
    def registro(self):
        r = aliased(rastreable)
        u = aliased(usuario)
        
        resultado = []
        for reg in DBSession.query(registro).\
        join(r, or_(registro.actor_activo == r.rastreable_id, registro.actor_pasivo == r.rastreable_id)).\
        join(u, r.rastreable_id == u.rastreable_p).\
        filter(u.usuario_id == self.usuario_id).all():
            resultado.append(self.formatear_entrada_registro(reg, self.peticion))

        return resultado
    
    @reify
    def tiendas(self):
        return DBSession.query(tienda).\
        join(cliente).\
        filter(cliente.propietario == self.usuario_id).all()
        
    @reify
    def patrocinantes(self):
        return DBSession.query(patrocinante).\
        join(cliente).\
        filter(cliente.propietario == self.usuario_id).all()
        
    @reify
    def calificaciones_resenas(self):
        var_comentarios = DBSession.query(calificacion_resena).\
        join(consumidor).\
        join(usuario).\
        filter(usuario.usuario_id == self.usuario_id).all()
        
        return [{""}] if var_comentarios is None else self.formatear_comentarios(var_comentarios) 
       
    @view_config(route_name='usuario', renderer='plantillas/usuario.pt')
    def usuario_view(self):
        var_usuario = self.obtener_usuario('id', self.usuario_id)
        resultado = HTTPNotFound(MENSAJE_DE_ERROR) \
        if (var_usuario is None) \
        else {'pagina': 'Usuario', 'usuario': var_usuario, 'autentificado': authenticated_userid(self.peticion)}
        return resultado