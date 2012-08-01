# -*- coding: utf-8 -*-
'''
Created on 08/04/2012

@author: nestor
'''
from paris.diagramas import Diagramas
from pyramid.decorator import reify
from pyramid.view import view_config

class InicioView(Diagramas):
    def __init__(self, peticion):
        self.peticion = peticion
        
    @reify
    def peticion(self):
        return self.peticion
    
    @view_config(route_name='inicio', renderer='../plantillas/inicio.pt')
    def inicio_view(self):
        return {'nombre_pagina': 'Inicio'}