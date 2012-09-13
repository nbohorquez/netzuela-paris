# -*- coding: utf-8 -*-
'''
Created on 07/06/2012

@author: nestor
'''

from paris.comunes import Comunes
from paris.diagramas import Diagramas
from paris.models.spuria import (
    cliente,
    crear_usuario, 
    crear_tienda, 
    crear_horarios_y_turnos,
    crear_descripcion,
    DBSession,
    tienda
)
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound
from pyramid.security import authenticated_userid
from pyramid.view import view_config, forbidden_view_config

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
    def __init__(self, peticion):
        self.peticion = peticion
        self.pagina_actual = peticion.url

    @reify
    def peticion(self):
        return self.peticion
    
    @reify
    def pagina_actual(self):
        return self.pagina_actual
    
    @property
    def pagina_anterior(self):
        return self.peticion.params.get('pagina_anterior', self.referido_por)
    
    @view_config(route_name='registro', renderer='../plantillas/registro.pt')
    def registro_view(self):
        self.referido_por = self.pagina_actual \
        if (self.pagina_actual != self.peticion.route_url('registro')) \
        else '/'
        
        resultado = {'pagina': 'Registro', 'aviso': None}
        
        if 'enviar' in self.peticion.params:
            usuario = crear_usuario(dict(self.peticion.POST))
            resultado['aviso'] = {
                'error': 'Error', 'mensaje': usuario['error']
            } if (usuario['error'] is not None) \
            else {'error': 'OK', 'mensaje': 'Registro completado con exito'}
        elif 'cancelar' in self.peticion.params:
            resultado = HTTPFound(location = self.pagina_anterior)
        
        return resultado
    
    @view_config(
        route_name='registro_tienda',
        renderer='../plantillas/registro_tienda.pt',
        permission='entrar'
    )
    @forbidden_view_config(route_name='registro')
    def registro_tienda_view(self):
        self.referido_por = self.pagina_actual \
        if (self.pagina_actual != self.peticion.route_url('registro_tienda')) \
        else '/'
        
        resultado = {'pagina': 'Registro de tienda', 'aviso': None}
        
        if 'enviar' in self.peticion.POST:
            autentificado = authenticated_userid(self.peticion)
            usuario_autentificado = self.obtener_usuario(
                'correo_electronico', autentificado
            )
            
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
            
            tnd = crear_tienda(parametros, usuario_autentificado.usuario_id)
            
            # Si hubo un error en la creacion de la tienda, no se puede avanzar;
            # hay que abortar
            if tnd['error'] is not None:
                resultado['aviso'] = {
                    'error': 'Error', 'mensaje': tnd['error']
                }
                return resultado

            # Creamos horarios y turnos predeterminados
            error = crear_horarios_y_turnos(
                horario_por_defecto, int(tnd['tienda'])
            )
        
            creador, descrb = DBSession.query(
            cliente.rastreable_p, cliente.describible_p).\
            join(tienda).\
            filter(tienda.tienda_id == int(tnd['tienda'])).first()
            
            # Creamos una descripcion 'dummy'
            descrp = crear_descripcion(
                {'contenido': 'Escriba una descripcion aqui'}, creador, descrb 
            )
            
            # Revisamos errores
            if error is not None or descrp['error'] is not None:
                resultado['aviso'] = {'error': 'Error', 'mensaje': []}
                if error is not None:
                    resultado['aviso']['mensaje'].append(error)
                if descrp['error'] is not None:
                    resultado['aviso']['mensaje'].append(descrp['error'])
            else:
                resultado['aviso'] = {
                    'error': 'OK', 
                    'mensaje': 'Registro de tienda completado con exito'
                }
        elif 'cancelar' in self.peticion.params:
            resultado = HTTPFound(location = self.pagina_anterior)
           
        return resultado