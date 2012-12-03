# -*- coding: utf-8 -*-
'''
Created on 08/04/2012

@author: nestor
'''
from paris.diagramas import Diagramas
from paris.comunes import Comunes
from pyramid.view import view_config

class InicioView(Diagramas, Comunes):
    def __init__(self, peticion, *args, **kwargs):
        super(InicioView, self).__init__(peticion=peticion, *args, **kwargs)
    
    @view_config(route_name='inicio', renderer='../plantillas/inicio.pt')
    def inicio_view(self):
        return {'pagina': 'Inicio'}