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
from paris.models.spuria import editar_patrocinante
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
    
    @property
    def patrocinante(self):
        return self.obtener_patrocinante(self.patrocinante_id)
    
    @reify
    def cliente_padre(self):
        return self.obtener_cliente_padre(self.tipo_de_peticion, self.patrocinante_id)
    
    @view_config(route_name='patrocinante', renderer='../plantillas/patrocinante.pt')
    def patrocinante_view(self):        
        editar = False
        aviso = None
        
        if self.patrocinante is None:
            return HTTPNotFound(MENSAJE_DE_ERROR)
        
        autentificado = authenticated_userid(self.peticion)
        
        if autentificado:
            usuario_autentificado = self.obtener_usuario('correo_electronico', autentificado)
            propietario = self.obtener_usuario('id', self.cliente_padre.propietario)
            editar = True if usuario_autentificado.usuario_id == propietario.usuario_id else False
            
            if editar and ('guardar' in self.peticion.POST):
                resultado = editar_patrocinante(dict(self.peticion.POST), self.patrocinante_id)
                aviso = { 'error': 'Error', 'mensaje': resultado['error'] } \
                if (resultado['error'] is not None) \
                else { 'error': 'OK', 'mensaje': 'Datos actualizados correctamente' }
        
        return {
            'pagina': 'Patrocinante', 
            'usuario': self.patrocinante, 
            'autentificado': autentificado, 
            'aviso': aviso, 
            'editar': editar
        }