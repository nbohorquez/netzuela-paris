# -*- coding: utf-8 -*-
'''
Created on 08/04/2012

@author: nestor
'''

from paris.comunes import (
    Comunes,
    formatear_comentarios,
    formatear_entrada_registro
)
from paris.constantes import MENSAJE_DE_ERROR
from paris.diagramas import Diagramas
from paris.models.spuria import (
    busqueda,
    calificable_seguible,
    calificacion_resena,
    categoria,
    cliente,
    consumidor,
    croquis,
    DBSession,
    dia,
    describible,
    descripcion,
    dibujable,
    editar_tienda,
    estadisticas,
    factura,
    foto,
    horario_de_trabajo,
    inventario,
    inventario_reciente,
    mensaje,
    patrocinante,
    producto,
    publicidad,
    punto,
    punto_de_croquis,
    rastreable,
    registro,
    seguidor,
    tamano_reciente,
    territorio,
    tienda,
    turno,
    usuario
)
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPNotFound
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from sqlalchemy import and_, or_
from sqlalchemy.orm import aliased
from sqlalchemy.sql import asc

# Aptana siempre va a decir que las clases de spuria (tienda, producto, etc) no estan 
# definidas explicitamente en ninguna parte. Lo que ocurre es que yo las cargo de forma 
# dinamica cuando inicia la aplicacion.

class TiendaView(Diagramas, Comunes):
    def __init__(self, peticion):
        self.peticion = peticion
        self.pagina_actual = peticion.url
        if 'tienda_id' in self.peticion.matchdict:
            self.tienda_id = self.peticion.matchdict['tienda_id']
        
    @reify
    def peticion(self):
        return self.peticion
    
    @reify
    def pagina_actual(self):
        return self.pagina_actual
    
    @reify
    def peticion_id(self):
        return self.tienda_id
    
    @reify
    def tipo_de_peticion(self):
        return 'tienda'
    
    @reify
    def tipo_de_rastreable(self):
        return 'cliente'
    
    @property
    def tienda(self):
        return self.obtener_tienda(self.tienda_id)

    @reify
    def inventario_reciente(self):
        return DBSession.query(inventario_reciente).\
        filter_by(tienda_id = self.tienda_id).all()
        
    @property
    def cliente_padre(self):
        return self.obtener_cliente_padre(self.tipo_de_peticion, self.tienda_id)

    @reify
    def registro(self):
        r = aliased(rastreable)                
        c = aliased(cliente)
        t = aliased(tienda)
        
        resultado = []
        for reg in DBSession.query(registro).\
        join(r, or_(registro.actor_activo == r.rastreable_id, registro.actor_pasivo == r.rastreable_id)).\
        join(c, r.rastreable_id == c.rastreable_p).\
        join(t, c.rif == t.cliente_p).\
        filter(t.tienda_id == self.tienda_id).order_by(registro.fecha_hora.desc()).all():
            resultado.append(formatear_entrada_registro(reg, self.peticion, self.tipo_de_rastreable))
        return resultado
        
    @reify
    def direccion(self):
        var_cliente = self.cliente_padre
        
        try:
            padre = aliased(territorio)
            hijo = aliased(territorio)
            
            p = DBSession.query(territorio).\
            filter_by(territorio_id = var_cliente.ubicacion).first()
            
            m = DBSession.query(padre).\
            join(hijo, padre.territorio_id == hijo.territorio_padre).\
            filter_by(territorio_id = p.territorio_id).first()
            
            e = DBSession.query(padre).\
            join(hijo, padre.territorio_id == hijo.territorio_padre).\
            filter_by(territorio_id = m.territorio_id).first()
            
            resultado = {
                'parroquia': p.nombre, 
                'municipio': m.nombre, 
                'estado': e.nombre 
            }
        except Exception, e:
            resultado = None
            
        return resultado
        
    @reify
    def descripciones(self):
        return DBSession.query(descripcion).\
        join(describible).\
        join(cliente).\
        join(tienda).\
        filter(tienda.tienda_id == self.tienda_id).all()
    
    @reify
    def horarios(self):
        var_horario = DBSession.query(horario_de_trabajo).\
        join(dia).\
        filter(horario_de_trabajo.tienda_id == self.tienda_id).order_by(asc(dia.orden)).all()
        
        if var_horario is not None:
            resultado = []
            for jornada in var_horario:
                horario = {}
                horario['dia'] = jornada.dia
                horario['laborable'] = jornada.laborable
                turnos = DBSession.query(turno).\
                filter(and_(turno.tienda_id == self.tienda_id, turno.dia == jornada.dia)).all()
                #horario['turnos'] = [{'apertura': str(t.hora_de_apertura), 'cierre': str(t.hora_de_cierre)} for t in turnos]
                horario['turnos'] = turnos
                resultado.append(horario)
        else:
            resultado = None

        return resultado
    
    @reify
    def tamano_reciente(self):
        return DBSession.query(tamano_reciente).\
        filter(tamano_reciente.tienda_id == self.tienda_id).first()
    
    @reify
    def calificaciones_resenas(self):
        var_comentarios = DBSession.query(calificacion_resena).\
        join(calificable_seguible).\
        join(tienda).\
        filter(tienda.tienda_id == self.tienda_id).all()
        return formatear_comentarios(var_comentarios)
    
    @reify
    def ruta_categoria_actual(self):
        cat_padre = DBSession.query(cliente.categoria).\
        join(tienda).\
        filter(tienda.tienda_id == self.peticion_id).first()[0]        
        return self.obtener_ruta_categoria(cat_padre)
    
    @view_config(route_name='tienda', renderer='../plantillas/tienda.pt', request_method='GET')
    @view_config(route_name='tienda', renderer='../plantillas/tienda.pt', request_method='POST')
    def tienda_view(self):
        editar = False
        aviso = None
        
        if self.tienda is None:
            return HTTPNotFound(MENSAJE_DE_ERROR)
        
        autentificado = authenticated_userid(self.peticion)
        
        if autentificado:
            usuario_autentificado = self.obtener_usuario('correo_electronico', autentificado)
            propietario = self.obtener_usuario('id', self.cliente_padre.propietario)
            editar = True if usuario_autentificado.usuario_id == propietario.usuario_id else False
        
            if editar and ('guardar' in self.peticion.POST):
                error = editar_tienda(dict(self.peticion.POST), self.tienda_id)
                aviso = { 'error': 'Error', 'mensaje': error } \
                if (error is not None) \
                else { 'error': 'OK', 'mensaje': 'Datos actualizados correctamente' }
        
        return {
            'pagina': 'Tienda', 
            'tienda': self.tienda, 
            'autentificado': autentificado, 
            'aviso': aviso, 
            'editar': editar
        }

    @view_config(route_name="tienda_turno", renderer="json")
    def tienda_turno_view(self):
        var_dia = self.peticion.params['dia']
        
        turnos = []
        for apertura, cierre in DBSession.query(turno.hora_de_apertura, turno.hora_de_cierre).\
        filter(and_(
            turno.tienda_id == self.tienda_id, 
            turno.dia == var_dia)
        ).all():
            _turno = {'apertura': "{0}".format(str(apertura)), 'cierre': "{0}".format(str(cierre))} 
            turnos.append(_turno)
                    
        return turnos
        
    @view_config(route_name="tienda_coordenadas", renderer="json")
    def tienda_coordenadas_view(self):
        puntos = []
        
        for lat, lng in DBSession.query(punto.latitud, punto.longitud).\
        join(punto_de_croquis).\
        join(croquis).\
        join(dibujable).\
        join(tienda).\
        filter_by(tienda_id = self.tienda_id).all():
            pto = {'latitud': "{0}".format(str(lat)), 'longitud': "{0}".format(str(lng))}
            puntos.append(pto)
        
        return { 'puntos': puntos }