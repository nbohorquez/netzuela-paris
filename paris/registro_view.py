'''
Created on 07/06/2012

@author: nestor
'''

from .comunes import comunes
from .constantes import MENSAJE_DE_ERROR
from .diagramas import diagramas
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config

class registro_view(diagramas, comunes):
    def __init__(self, peticion):
        self.peticion = peticion

    @reify
    def peticion(self):
        return self.peticion
    """
    @view_config(route_name='registro', renderer='plantillas/registro.pt')
    def registro_view(self):
        var_tienda = self.obtener_tienda(self.tienda_id)
        resultado = HTTPNotFound(MENSAJE_DE_ERROR) \
        if (var_tienda is None) \
        else {'pagina': 'Tienda', 'tienda': var_tienda}
        return resultado"""