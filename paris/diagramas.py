# -*- coding: utf-8 -*-
'''
Created on 28/02/2012

@author: Nestor
'''

from paris.models.spuria import (
    accion,
    calificacion,
    categoria,
    codigo_de_error,
    DBSession,
    dia,
    estatus,
    grado_de_instruccion,
    grupo_de_edad,
    idioma,
    privilegios,    
    sexo,
    tipo_de_codigo,
    visibilidad
)
from pyramid.decorator import reify
from pyramid.renderers import get_renderer
from sqlalchemy.sql import asc

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
    def categorias(self):
        return DBSession.query(categoria).filter_by(nivel = 1).all()
    
    @reify
    def grados_de_instruccion(self):
        return DBSession.query(grado_de_instruccion).order_by(asc(grado_de_instruccion.orden)).all()
    
    @reify
    def sexos(self):
        return DBSession.query(sexo).all()
    
    @reify
    def codigos_de_error(self):
        return DBSession.query(codigo_de_error).all()
    
    @reify
    def privilegios(self):
        return DBSession.query(privilegios).all()
    
    @reify
    def idiomas(self):
        return DBSession.query(idioma).all()
    
    @reify
    def tipos_de_codigo(self):
        return DBSession.query(tipo_de_codigo).all()
    
    @reify
    def visibilidades(self):
        return DBSession.query(visibilidad).all()
    
    @reify
    def acciones(self):
        return DBSession.query(accion).all()
    
    @reify
    def calificaciones(self):
        return DBSession.query(calificacion).all()
    
    @reify
    def grupos_de_edades(self):
        return DBSession.query(grupo_de_edad).all()

    @reify
    def estatus(self):
        return DBSession.query(estatus).all()
    
    @reify
    def dias(self):
        return DBSession.query(dia).order_by(asc(dia.orden)).all()