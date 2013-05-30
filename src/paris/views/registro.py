# -*- coding: utf-8 -*-
'''
Created on 07/06/2012

@author: nestor
'''

from formencode.api import Invalid
from paris.comunes import Comunes
from paris.diagramas import Diagramas
from paris.models.edicion import (
    crear_usuario, 
    crear_tienda, 
    crear_descripcion,
    editar_horarios_y_turnos
)
from pyramid.httpexceptions import HTTPFound
from pyramid.security import authenticated_userid
from pyramid.view import view_config, forbidden_view_config
from spuria.orm import Cliente, DBSession, Tienda
import transaction

horario_por_defecto = {
    'Lunes': 'Abierto',
    'Lunes.hora_de_apertura.0': '08:00:00',
    'Lunes.hora_de_cierre.0': '16:00:00',
    'Martes': 'Abierto',
    'Martes.hora_de_apertura.0': '08:00:00',
    'Martes.hora_de_cierre.0': '16:00:00',
    'Miercoles': 'Abierto',
    'Miercoles.hora_de_apertura.0': '08:00:00',
    'Miercoles.hora_de_cierre.0': '16:00:00',
    'Jueves': 'Abierto',
    'Jueves.hora_de_apertura.0': '08:00:00',
    'Jueves.hora_de_cierre.0': '16:00:00',
    'Viernes': 'Abierto',
    'Viernes.hora_de_apertura.0': '08:00:00',
    'Viernes.hora_de_cierre.0': '16:00:00',
    'Sabado': 'Abierto',
    'Sabado.hora_de_apertura.0': '08:00:00',
    'Sabado.hora_de_cierre.0': '12:00:00',
    'Domingo': 'Cerrado',
    'Domingo.hora_de_apertura.0': '00:00:00',
    'Domingo.hora_de_cierre.0': '00:00:00'
}

class RegistroView(Comunes, Diagramas):
    def __init__(self, peticion, *args, **kwargs):
        super(RegistroView, self).__init__(peticion=peticion, *args, **kwargs)

    @property
    def pagina_anterior(self):
        return self.peticion.params.get('pagina_anterior', self.referido_por)
    
    @view_config(route_name='registro', renderer='../plantillas/registro.pt')
    def registro_view(self):
        aviso = None
        
        self.referido_por = self.pagina_actual \
        if (self.pagina_actual != self.peticion.route_url('registro')) \
        else '/'

        if 'enviar' in self.peticion.params:
            try:
                with transaction.manager:
                    crear_usuario(dict(self.peticion.POST))
                aviso = {
                    'error': 'OK',
                    'mensaje': 'Registro completado con exito'
                }
            except Invalid as e:
                aviso = { 'error': 'Error', 'mensaje': e.msg }
        elif 'cancelar' in self.peticion.params:
            return HTTPFound(location = self.pagina_anterior)
        
        return {
            'titulo': 'Registro de usuario',
            'pagina': 'Registro de usuario',
            'aviso': aviso
        }

    @view_config(
        route_name='registro_tienda',
        renderer='../plantillas/registro_tienda.pt',
        permission='entrar'
    )
    @forbidden_view_config(route_name='registro')
    def registro_tienda_view(self):
        aviso = None
        
        self.referido_por = self.pagina_actual \
        if (self.pagina_actual != self.peticion.route_url('registro_tienda')) \
        else '/'
        
        if 'enviar' in self.peticion.POST:
            autentificado = authenticated_userid(self.peticion)
            
            parametros = dict(self.peticion.params)
            
            # El formulario registro_tienda no tiene estas campos por simplici-
            # dad. Pero hay que ponerselas porque sino explota el formencode.
            parametros['apartamento'] = ''
            parametros['casa'] = ''
            parametros['correo_electronico_publico'] = ''
            parametros['edificio'] = ''
            parametros['facebook'] = ''
            parametros['local_no'] = ''
            parametros['pagina_web'] = ''
            parametros['piso'] = ''
            parametros['twitter'] = ''
            
            try:
                with transaction.manager:
                    usuario_autentificado = self.obtener_usuario(
                        'correo_electronico', autentificado
                    )
                    tnd = crear_tienda(parametros, usuario_autentificado)
                    # Creamos horarios y turnos predeterminados
                    editar_horarios_y_turnos(horario_por_defecto, tnd)
                    # Creamos una descripcion 'dummy'
                    crear_descripcion(
                        parametros={'contenido':'Escriba una descripcion aqui'}, 
                        creador=tnd, describible=tnd.describible
                    )
                aviso = {
                    'error': 'OK',
                    'mensaje': 'Registro de tienda completado con exito'
                }
            except Invalid as e:
                aviso = { 'error': 'Error', 'mensaje': e.msg }
        elif 'cancelar' in self.peticion.params:
            return HTTPFound(location = self.pagina_anterior)
        
        return {
            'titulo': 'Registro de tienda',
            'pagina': 'Registro de tienda',
            'aviso': aviso
        }