# -*- coding: utf-8 -*-
'''
Created on 28/02/2012

@author: Nestor
'''

from pyramid.decorator import reify
from pyramid.renderers import get_renderer

class Diagramas(object):
    def __init__(self):
        pass

    @reify
    def diagrama_global(self):
        renderer = get_renderer("plantillas/global.pt")
        return renderer.implementation().macros['diagrama_global']
    
    @reify
    def macros(self):
        renderer = get_renderer("plantillas/macros.pt")
        return renderer.implementation().macros
    
    @reify
    def formularios(self):
        renderer = get_renderer("plantillas/formularios.pt")
        return renderer.implementation().macros