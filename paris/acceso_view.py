# -*- coding: utf-8 -*-
'''
Created on 07/06/2012

@author: nestor
'''

from .diagramas import diagramas
from .models import (acceso, DBSession)
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from pyramid.view import view_config, forbidden_view_config
import bcrypt

class acceso_view(diagramas):
    def __init__(self, peticion):
        ingresar_url = peticion.route_url('ingresar')
        # never use the login form itself as came_from
        self.referido_por = peticion.url if (peticion.url != ingresar_url) else '/'
        self.peticion = peticion
    
    @reify
    def peticion(self):
        return self.peticion
    
    @reify
    def pagina_actual(self):
        return self.peticion.route_url
    
    @reify
    def pagina_anterior(self):
        return self.peticion.params.get('pagina_anterior', self.referido_por)
    
    def autentificar(self, usuario, contrasena):
        resultado = False
        tmp = DBSession.query(acceso.contrasena).filter_by(correo_electronico = usuario).first()
        if tmp is not None:
            if bcrypt.hashpw(contrasena, tmp[0]) == tmp[0]:
                resultado = True
        
        return resultado
        
    @view_config(route_name='ingresar', renderer='plantillas/ingresar.pt')
    @forbidden_view_config(renderer='plantillas/ingresar.pt')
    def ingresar_view(self):
        mensaje = ''
        
        if 'ingresar' in self.peticion.params:
            usuario = self.peticion.params['usuario']
            contrasena = self.peticion.params['contrasena']
            
            if self.autentificar(usuario, contrasena) is True:
                headers = remember(self.peticion, usuario)
                return HTTPFound(location = self.pagina_anterior, headers = headers)
            else:
                mensaje = 'Par usuario/contrasena invalido'
                
        elif 'registrarse' in self.peticion.params:
            return HTTPFound(location = self.peticion.route_url('registro_consumidor'))
    
        return { 'pagina': 'Ingresar', 'mensaje': mensaje }
        
    @view_config(route_name='salir')
    def salir_view(self):
        headers = forget(self.peticion)
        return HTTPFound(location = self.peticion.route_url('inicio'), headers = headers)