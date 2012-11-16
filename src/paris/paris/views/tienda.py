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
from paris.models.funciones import editar_tienda
from spuria.orm import (
    CalificableSeguible,
    CalificacionResena,
    Cliente,
    Croquis,
    DBSession,
    Dia,
    Describible,
    Descripcion,
    Dibujable,
    HorarioDeTrabajo,
    InventarioReciente,
    Punto,
    PuntoDeCroquis,
    Rastreable,
    Registro,
    TamanoReciente,
    Territorio,
    Tienda,
    Turno
)
from spuria.orm.descripciones_fotos import DescribibleAsociacion
from spuria.orm.calificaciones_resenas import CalificableSeguibleAsociacion
from spuria.orm.croquis_puntos import DibujableAsociacion
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPNotFound
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from sqlalchemy import and_, or_
from sqlalchemy.orm import aliased
from sqlalchemy.sql import asc

# Aptana siempre va a decir que las clases de spuria (tienda, producto, etc) no 
# estan definidas explicitamente en ninguna parte. Lo que ocurre es que yo las 
# cargo de forma dinamica cuando inicia la aplicacion.

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
        return DBSession.query(InventarioReciente).\
        filter_by(tienda_id = self.tienda_id).all()
        
    @property
    def cliente_padre(self):
        return self.obtener_cliente_padre(self.tipo_de_peticion, self.tienda_id)

    @reify
    def registro(self):
        r = aliased(Rastreable)
        c = aliased(Cliente)
        t = aliased(Tienda)
        
        resultado = []
        for reg in DBSession.query(Registro).\
        join(r, or_(
            Registro.actor_activo == r.rastreable_id, 
            Registro.actor_pasivo == r.rastreable_id
        )).\
        join(c, r.rastreable_id == c.rastreable_p).\
        join(t, c.rif == t.cliente_p).\
        filter(t.tienda_id == self.tienda_id).\
        order_by(Registro.fecha_hora.desc()).all():
            resultado.append(formatear_entrada_registro(
                reg, self.peticion, self.tipo_de_rastreable
            ))
        return resultado
        
    @reify
    def direccion(self):
        try:
            resultado = {
                'parroquia': self.tienda.ubicacion.nombre, 
                'municipio': self.tienda.ubicacion.padre.nombre,
                'estado': self.tienda.ubicacion.padre.padre.nombre 
            }
        except Exception:
            resultado = None
            
        return resultado
        
    @reify
    def descripciones(self):
        return DBSession.query(Descripcion).\
        join(Describible).\
        join(DescribibleAsociacion).\
        join(Tienda).\
        filter(Tienda.tienda_id == self.tienda_id).all()
    
    @reify
    def horarios(self):
        horarios = DBSession.query(HorarioDeTrabajo).\
        join(Dia).\
        filter(HorarioDeTrabajo.tienda_id == self.tienda_id).\
        order_by(asc(Dia.orden)).all()
        #horarios = self.tienda.horarios_de_trabajo
        
        if horarios is not None:
            resultado = []
            for jornada in horarios:
                horario = {}
                horario['dia'] = jornada.dia
                horario['laborable'] = jornada.laborable
                horario['turnos'] = jornada.turnos
                resultado.append(horario)
        else:
            resultado = None

        return resultado
    
    @reify
    def tamano_reciente(self):
        return DBSession.query(TamanoReciente).\
        filter(TamanoReciente.tienda_id == self.tienda_id).first()
    
    @reify
    def calificaciones_resenas(self):
        comentarios = DBSession.query(CalificacionResena).\
        join(CalificableSeguible).\
        join(CalificableSeguibleAsociacion).\
        join(Tienda).\
        filter(Tienda.tienda_id == self.tienda_id).all()
        return formatear_comentarios(comentarios)
    
    @reify
    def ruta_categoria_actual(self):
        return self.obtener_ruta_categoria(self.tienda.categoria)
    
    @view_config(route_name='tienda', renderer='../plantillas/tienda.pt', 
                 request_method='GET')
    @view_config(route_name='tienda', renderer='../plantillas/tienda.pt', 
                 request_method='POST')
    def tienda_view(self):
        editar = False
        aviso = None
        
        if self.tienda is None:
            return HTTPNotFound(MENSAJE_DE_ERROR)
        
        autentificado = authenticated_userid(self.peticion)
        
        if autentificado:
            usuario_autentificado = self.obtener_usuario(
                'correo_electronico', autentificado
            )
            propietario = self.obtener_usuario(
                'id', self.cliente_padre.propietario
            )
            editar = True \
            if usuario_autentificado.usuario_id == propietario.usuario_id \
            else False

            if editar and ('guardar' in self.peticion.POST):
                error = editar_tienda(dict(self.peticion.POST), self.tienda_id)
                aviso = { 'error': 'Error', 'mensaje': error } \
                if (error is not None) \
                else { 
                    'error': 'OK', 
                    'mensaje': 'Datos actualizados correctamente' 
                }

        return {
            'pagina': 'Tienda', 
            'tienda': self.tienda, 
            'autentificado': autentificado, 
            'aviso': aviso, 
            'editar': editar
        }

    @view_config(route_name="tienda_turno", renderer="json")
    def tienda_turno_view(self):
        dia = self.peticion.params['dia']
        
        turnos = []
        for apertura, cierre in DBSession.query(
            Turno.hora_de_apertura, Turno.hora_de_cierre
        ).filter(and_(
            Turno.tienda_id == self.tienda_id, 
            Turno.dia == dia)
        ).all():
            turno = {
                'apertura': "{0}".format(str(apertura)), 
                'cierre': "{0}".format(str(cierre))
            }
            turnos.append(turno)
            
        return turnos
        
    @view_config(route_name="tienda_coordenadas", renderer="json")
    def tienda_coordenadas_view(self):
        puntos = []
        
        for lat, lng in DBSession.query(Punto.latitud, Punto.longitud).\
        join(PuntoDeCroquis).\
        join(Croquis).\
        join(Dibujable).\
        join(DibujableAsociacion).\
        join(Tienda).\
        filter_by(tienda_id = self.tienda_id).all():
            pto = {
                'latitud': "{0}".format(str(lat)), 
                'longitud': "{0}".format(str(lng))
            }
            puntos.append(pto)
        
        return { 'puntos': puntos }