# -*- coding: utf-8 -*-
'''
Created on 07/06/2012

@author: nestor
'''

from paris.comunes import Comunes
from paris.diagramas import Diagramas
from spuria.orm import Acceso, DBSession, Registro
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget, authenticated_userid
from pyramid.view import view_config, forbidden_view_config
import bcrypt, transaction

class AccesoView(Diagramas, Comunes):
    def __init__(self, peticion, *args, **kwargs):
        super(AccesoView, self).__init__(peticion=peticion, *args, **kwargs)
        ingresar_url = peticion.route_url('ingresar')
        # never use the login form itself as came_from
        self.referido_por = peticion.url \
        if (peticion.url != ingresar_url) \
        else '/'
        
    @reify
    def peticion(self):
        return self.peticion
    
    @reify
    def pagina_actual(self):
        return self.peticion.route_url
    
    @reify
    def pagina_anterior(self):
        return self.peticion.params.get('pagina_anterior', self.referido_por)
    
    @reify
    def correo_electronico(self):
        return self.correo_electronico
    
    @reify
    def usuario(self):
        return self.obtener_usuario(
            'correo_electronico', self.correo_electronico
        )
        
    def autentificar(self, correo, contrasena):
        resultado = False
        tmp = DBSession.query(Acceso.contrasena).\
        filter_by(correo_electronico = correo).first()
        
        if tmp is not None:
            if bcrypt.hashpw(contrasena, tmp[0]) == tmp[0]:
                resultado = True
        
        return resultado
    
    def registrar_alta(self):
        with transaction.manager:
            registrar_alta_sql = Registro(
                actor_activo=self.usuario.rastreable, accion='Abrir sesion', 
                actor_pasivo=None, detalles=None
            )
            DBSession.add(registrar_alta_sql)

    def registrar_baja(self):
        with transaction.manager:
            registrar_baja_sql = Registro(
                actor_activo=self.usuario.rastreable, accion='Cerrar sesion', 
                actor_pasivo=None, detalles=None
            )
            DBSession.add(registrar_baja_sql)
    
    @view_config(route_name='ingresar', renderer='../plantillas/ingresar.pt')
    @forbidden_view_config(renderer='../plantillas/ingresar.pt')
    def ingresar_view(self):
        mensaje = ''
        
        if 'ingresar' in self.peticion.params:
            self.correo_electronico = self.peticion.params['usuario']
            contrasena = self.peticion.params['contrasena']
            
            if self.autentificar(self.correo_electronico, contrasena) is True:
                headers = remember(self.peticion, self.correo_electronico)
                self.registrar_alta()
                return HTTPFound(
                    location = self.pagina_anterior, headers = headers
                )
            else:
                mensaje = 'Par usuario/contrasena invalido'
        elif 'registrarse' in self.peticion.params:
            return HTTPFound(location = self.peticion.route_url('registro'))
            
        return { 'pagina': 'Ingresar', 'mensaje': mensaje }
        
    @view_config(route_name='salir')
    def salir_view(self):
        self.correo_electronico = authenticated_userid(self.peticion)
        headers = forget(self.peticion)
        self.registrar_baja()
        return HTTPFound(
            location = self.peticion.route_url('inicio'), headers = headers
        )