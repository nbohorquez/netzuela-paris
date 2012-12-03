# -*- coding: utf-8 -*-
'''
Created on 20/07/2012

@author: nestor
'''

from formencode.api import Invalid
from paris.comunes import Comunes
from paris.formatos import (
    formatear_comentarios,
    formatear_fecha_para_paris,
    formatear_entrada_noticias
)
from paris.constantes import MENSAJE_DE_ERROR
from paris.diagramas import Diagramas
from paris.models.edicion import editar_usuario
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPNotFound
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from spuria.orm import (
    CalificacionResena,
    Cliente,
    Consumidor,
    DBSession,
    Patrocinante,
    Rastreable,
    Registro,
    Tienda,
    Usuario
)
from spuria.orm.rastreable import RastreableAsociacion
from sqlalchemy import desc, or_
import transaction

class UsuarioView(Diagramas, Comunes):
    def __init__(self, peticion, *args, **kwargs):
        super(UsuarioView, self).__init__(peticion=peticion, *args, **kwargs)
        if 'usuario_id' in self.peticion.matchdict:
            self.usuario_id = self.peticion.matchdict['usuario_id']
    
    @reify
    def peticion_id(self):
        return self.usuario_id
    
    @reify
    def tipo_de_peticion(self):
        return 'usuario'

    @property
    def usuario(self):
        return self.obtener_usuario('id', self.usuario_id)

    @reify
    def registro(self):
        registros = DBSession.query(Registro).\
        join(Rastreable, or_(
            Registro.actor_activo_id == Rastreable.rastreable_id,
            Registro.actor_pasivo_id == Rastreable.rastreable_id
        )).join(RastreableAsociacion).\
        join(Usuario).\
        filter(Usuario.usuario_id == self.usuario_id).\
        order_by(desc(Registro.fecha_hora)).\
        limit(10)
        
        noticias = [formatear_entrada_noticias(registro, self.peticion, \
                    self.usuario) for registro in registros]
        return noticias

    @reify
    def fecha_de_nacimiento(self):
        return \
        formatear_fecha_para_paris(str(self.usuario.fecha_de_nacimiento)) \
        if self.usuario.tipo == 'consumidor' \
        else None

    @reify
    def tiendas_asociadas(self):
        try:
            l = [ t for t in self.usuario.propiedades if t.tipo == 'tienda' ]
        except Exception:
            l = []
        return l

    @reify
    def patrocinantes_asociados(self):
        try:
            l = [ p for p in self.usuario.propiedades \
            if p.tipo == 'patrocinante' ]
        except Exception:
            l = []
        return l

    @reify
    def calificaciones_resenas(self):
        try:
            comentarios = self.usuario.calificaciones_resenas
        except Exception:
            comentarios = []
            
        resultado = []
        for comentario in comentarios:
            resultado.append(formatear_comentarios(comentario))
            
        return resultado

    @view_config(route_name='usuario', renderer='../plantillas/usuario.pt', 
                 request_method='GET')
    @view_config(route_name='usuario', renderer='../plantillas/usuario.pt', 
                 request_method='POST')
    def usuario_view(self):
        editar = False
        aviso = None

        if self.usuario is None:
            return HTTPNotFound(MENSAJE_DE_ERROR)

        autentificado = authenticated_userid(self.peticion)

        if autentificado:
            usuario_autentificado = self.obtener_usuario(
                'correo_electronico', autentificado
            )
            
            editar = True \
            if usuario_autentificado.usuario_id == self.usuario.usuario_id \
            else False
            
            if editar and ('guardar' in self.peticion.POST):
                try:
                    with transaction.manager:
                        editar_usuario(dict(self.peticion.POST), self.usuario)
                    aviso = {
                        'error': 'OK',
                        'mensaje': 'Datos actualizados correctamente'
                    }
                except Invalid as e:
                    aviso = { 'error': 'Error', 'mensaje': e.msg }

        return {
            'pagina': 'Usuario', 
            'usuario': self.usuario, 
            'autentificado': autentificado, 
            'aviso': aviso, 
            'editar': editar
        }