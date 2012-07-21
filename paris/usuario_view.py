# -*- coding: utf-8 -*-
'''
Created on 20/07/2012

@author: nestor
'''

from .comunes import Comunes
from .constantes import MENSAJE_DE_ERROR
from .diagramas import Diagramas
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPNotFound
from pyramid.security import authenticated_userid
from pyramid.view import view_config

class UsuarioView(Diagramas, Comunes):
    def __init__(self, peticion):
        self.peticion = peticion
        self.pagina_actual = peticion.url
        if 'usuario_id' in self.peticion.matchdict:
            self.tienda_id = self.peticion.matchdict['usuario_id']
            
    @reify
    def peticion(self):
        return self.peticion
    
    @reify
    def pagina_actual(self):
        return self.pagina_actual
    
    @reify
    def peticion_id(self):
        return self.usuario_id
    
    @view_config(route_name='usuario', renderer='plantillas/usuario.pt')
    def usuario_view(self):
        var_usuario = self.obtener_usuario(self.tienda_id)
        resultado = HTTPNotFound(MENSAJE_DE_ERROR) \
        if (var_usuario is None) \
        else {'pagina': 'Usuario', 'usuario': var_usuario, 'autentificado': authenticated_userid(self.peticion)}
        return resultado