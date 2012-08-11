# -*- coding: utf-8 -*-
'''
Created on 31/07/2012

@author: nestor
'''

from paris.comunes import (
    Comunes
)    
from paris.constantes import MENSAJE_DE_ERROR
from paris.diagramas import Diagramas
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPNotFound
from pyramid.security import authenticated_userid
from pyramid.view import view_config

class PatrocinanteView(Diagramas, Comunes):
    def __init__(self, peticion):
        self.peticion = peticion
        self.pagina_actual = peticion.url
        if 'patrocinante_id' in self.peticion.matchdict:
            self.patrocinante_id = self.peticion.matchdict['patrocinante_id']
            
    @reify
    def peticion(self):
        return self.peticion
    
    @reify
    def pagina_actual(self):
        return self.pagina_actual
    
    @reify
    def tipo_de_peticion(self):
        return 'patrocinante'
    
    @reify
    def tipo_de_rastreable(self):
        return 'cliente'
    
    @reify
    def peticion_id(self):
        return self.patrocinante_id
    
    @reify
    def cliente_padre(self):
        return self.obtener_cliente_padre(self.tipo_de_peticion, self.patrocinante_id)
    
    @view_config(route_name='patrocinante', renderer='../plantillas/patrocinante.pt')
    def patrocinante_view(self):
        var_patrocinante = self.obtener_patrocinante(self.patrocinante_id)
        resultado = HTTPNotFound(MENSAJE_DE_ERROR) \
        if (var_patrocinante is None) \
        else {'pagina': 'Patrocinante', 'patrocinante': var_patrocinante, 'autentificado': authenticated_userid(self.peticion)}
        return resultado