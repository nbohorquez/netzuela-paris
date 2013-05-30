# -*- coding: utf-8 -*-
'''
Created on 08/04/2012

@author: nestor
'''

from formencode.api import Invalid
from paris.comunes import Comunes
from paris.formatos import (
    formatear_comentarios,
    formatear_entrada_noticias
)
from paris.constantes import MENSAJE_DE_ERROR
from paris.diagramas import Diagramas
from paris.models.edicion import editar_tienda
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
    Turno,
    Producto,
    Inventario
)
from spuria.orm.calificaciones_resenas import CalificableSeguibleAsociacion
from spuria.orm.croquis_puntos import DibujableAsociacion
from spuria.orm.descripciones_fotos import DescribibleAsociacion
from spuria.orm.rastreable import RastreableAsociacion
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from sqlalchemy import and_, desc, or_
from sqlalchemy.sql import asc
import transaction

# Aptana siempre va a decir que las clases de spuria (tienda, producto, etc) no 
# estan definidas explicitamente en ninguna parte. Lo que ocurre es que yo las 
# cargo de forma dinamica cuando inicia la aplicacion.

class TiendaView(Diagramas, Comunes):
    def __init__(self, peticion, *args, **kwargs):
        super(TiendaView, self).__init__(peticion=peticion, *args, **kwargs)

        if 'tienda_id' in self.peticion.matchdict:
            self.tienda_id = self.peticion.matchdict['tienda_id']
        if 'categoria_id' in self.peticion.matchdict:
            self.categoria_id = self.peticion.matchdict['categoria_id']
        else:
            self.categoria_id = None
        
    @reify
    def peticion_id(self):
        return self.tienda_id
    
    @reify
    def tipo_de_peticion(self):
        return 'tienda'
    
    @property
    def tienda(self):
        return self.obtener_tienda(self.tienda_id)

    @reify
    def inventario_reciente(self):
        return DBSession.query(InventarioReciente).\
        join(Producto, InventarioReciente.producto_id == Producto.producto_id).\
        filter(and_(
            InventarioReciente.tienda_id == self.tienda_id,
            Producto.categoria_id.contains(self.categoria_base)
        )).all()
        
    @property
    def cliente_padre(self):
        return self.obtener_cliente_padre(self.tipo_de_peticion, self.tienda_id)

    @reify
    def registro(self):
        reg1 = DBSession.query(Registro).\
        join(Rastreable, Registro.actor_pasivo_id == Rastreable.rastreable_id).\
        join(RastreableAsociacion).\
        join(Inventario).\
        join(Producto).\
        filter(and_(
            Producto.categoria_id.contains(self.categoria_base),
            Inventario.tienda_id == self.tienda_id
        ))
        """
        reg2 = DBSession.query(Registro).\
        join(Rastreable, or_(
            Registro.actor_activo_id == Rastreable.rastreable_id,
            Registro.actor_pasivo_id == Rastreable.rastreable_id
        )).join(RastreableAsociacion).\
        join(Tienda).\
        filter(Tienda.tienda_id == self.tienda_id)
        """
        registros = reg1.order_by(desc(Registro.fecha_hora)).\
        limit(10)
        
        noticias = [formatear_entrada_noticias(registro, self.peticion, \
                    self.tienda) for registro in registros]
        return noticias
        
    @reify
    def direccion(self):
        """
        try:
            resultado = {
                'parroquia': self.tienda.ubicacion.nombre, 
                'municipio': self.tienda.ubicacion.padre.nombre,
                'estado': self.tienda.ubicacion.padre.padre.nombre 
            }
        except Exception:
            resultado = None
        
        return resultado
        """
        return self.obtener_ruta_territorio(self.tienda.ubicacion, 2, False)
        
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
        
        resultado = []
        for comentario in comentarios:
            resultado.append(formatear_comentarios(comentario))
            
        return resultado
    
    @view_config(route_name='tienda', renderer='../plantillas/tienda.pt', 
                 request_method='GET')
    @view_config(route_name='tienda', renderer='../plantillas/tienda.pt', 
                 request_method='POST')
    @view_config(route_name='tienda_cat', renderer='../plantillas/tienda.pt', 
                 request_method='GET')
    @view_config(route_name='tienda_cat', renderer='../plantillas/tienda.pt',
                 request_method='POST')
    def tienda_view(self):
        editar = False
        aviso = None
        
        if self.tienda is None:
            return HTTPNotFound(MENSAJE_DE_ERROR)

        if self.categoria_id is None:
            return HTTPFound(location = self.peticion.route_url(
                'tienda_cat', tienda_id = self.tienda_id, 
                categoria_id = self.tienda.categoria_id
            ))
            
        autentificado = authenticated_userid(self.peticion)
        
        if autentificado:
            usuario_autentificado = self.obtener_usuario(
                'correo_electronico', autentificado
            )
            propietario = self.tienda.propietario
            
            editar = True \
            if usuario_autentificado.usuario_id == propietario.usuario_id \
            else False

            if editar and ('guardar' in self.peticion.POST):
                try:
                    with transaction.manager:
                        editar_tienda(dict(self.peticion.POST), self.tienda)
                    aviso = {
                        'error': 'OK',
                        'mensaje': 'Datos actualizados correctamente'
                    }
                except Invalid as e:
                    aviso = { 'error': 'Error', 'mensaje': e.msg }

        return {
            'titulo': self.tienda.nombre_comun,
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