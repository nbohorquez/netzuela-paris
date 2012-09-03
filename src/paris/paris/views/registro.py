# -*- coding: utf-8 -*-
'''
Created on 07/06/2012

@author: nestor
'''

from paris.comunes import Comunes
from paris.diagramas import Diagramas
from paris.models.spuria import crear_usuario, crear_consumidor, crear_tienda
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

class RegistroView(Comunes, Diagramas):
    def __init__(self, peticion):
        self.peticion = peticion
        registro_url = peticion.route_url('registro_consumidor')
        self.pagina_actual = peticion.url
        self.referido_por = peticion.url if (peticion.url != registro_url) else '/'

    @reify
    def peticion(self):
        return self.peticion
    
    @reify
    def pagina_actual(self):
        return self.pagina_actual
    
    @reify
    def pagina_anterior(self):
        return self.peticion.params.get('pagina_anterior', self.referido_por)
    
    @view_config(route_name='registro', renderer='../plantillas/registro.pt')
    def registro_view(self):
        resultado = {'pagina': 'Registro', 'aviso': None}
        if 'enviar' in self.peticion.params:      
            usuario = crear_usuario(dict(self.peticion.params))
            resultado['aviso'] = {'error': 'Error', 'mensaje': usuario['error']} \
            if (usuario['error'] is not None) \
            else {'error': 'OK', 'mensaje': 'Registro completado con éxito'}
        elif 'cancelar' in self.peticion.params:
            resultado = HTTPFound(location = self.pagina_anterior)
        
        return resultado
    
    @view_config(route_name='registro_consumidor', renderer='../plantillas/registro_consumidor.pt')
    def registro_consumidor_view(self):
        resultado = {'pagina': 'Registro de consumidor', 'aviso': None}
        if 'enviar' in self.peticion.params:      
            consumidor = crear_consumidor(dict(self.peticion.params))
            resultado['aviso'] = {'error': 'Error', 'mensaje': consumidor['error']} \
            if (consumidor['error'] is not None) \
            else {'error': 'OK', 'mensaje': 'Registro completado con éxito'}
        elif 'cancelar' in self.peticion.params:
            resultado = HTTPFound(location = self.pagina_anterior)
                    
        return resultado   
    
    @view_config(route_name='registro_tienda', renderer='../plantillas/registro_tienda.pt')
    def registro_tienda_view(self):        
        resultado = {'pagina': 'Registro de tienda', 'aviso': None}
        if 'enviar' in self.peticion.params:
            usuario = crear_usuario(dict(self.peticion.params))            
            if (usuario['error'] is not None):
                resultado['aviso'] = {'error': 'Error', 'mensaje': usuario['error']}
            else:
                tienda = crear_tienda(dict(self.peticion.params), usuario['usuario'])
                resultado['aviso'] = {'error': 'Error', 'mensaje': tienda['error']} \
                if (tienda['error'] is not None) \
                else {'error': 'OK', 'mensaje': 'Registro completado con éxito'}
        elif 'cancelar' in self.peticion.params:
            resultado = HTTPFound(location = self.pagina_anterior)
            
        return resultado