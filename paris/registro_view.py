'''
Created on 07/06/2012

@author: nestor
'''

from .comunes import comunes
from .diagramas import diagramas
from pyramid.decorator import reify
from pyramid.view import view_config

class registro_view(diagramas, comunes):
    def __init__(self, peticion):
        self.peticion = peticion
        self.pagina_actual = peticion.url

    @reify
    def peticion(self):
        return self.peticion
    
    @reify
    def pagina_actual(self):
        return self.pagina_actual
    
    @view_config(route_name='registro', renderer='plantillas/registro.pt')
    def registro_view(self):
        return  {'pagina': 'Registro'}