# -*- coding: utf-8 -*-
'''
Created on 20/07/2012

@author: nestor
'''

from paris.comunes import (
    Comunes,
    formatear_comentarios,
    formatear_entrada_registro,
    formatear_fecha_para_paris
)
from paris.constantes import MENSAJE_DE_ERROR
from paris.diagramas import Diagramas
from paris.models.funciones import editar_usuario
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
from sqlalchemy import or_, and_, case
from sqlalchemy.orm import aliased

class UsuarioView(Diagramas, Comunes):
    def __init__(self, peticion):
        self.peticion = peticion
        self.pagina_actual = peticion.url
        if 'usuario_id' in self.peticion.matchdict:
            self.usuario_id = self.peticion.matchdict['usuario_id']

    @reify
    def peticion(self):
        return self.peticion

    @reify
    def pagina_actual(self):
        return self.pagina_actual

    @reify
    def tipo_de_peticion(self):
        return 'usuario'

    @reify
    def tipo_de_rastreable(self):
        return 'usuario'

    @reify
    def peticion_id(self):
        return self.usuario_id

    @property
    def usuario(self):
        return self.obtener_usuario('id', self.usuario_id)

    @reify
    def registro(self):
        r = aliased(Rastreable)
        u = aliased(Usuario)

        resultado = []
        for reg in DBSession.query(Registro).\
        join(r, or_(
            Registro.actor_activo == r.rastreable_id, 
            Registro.actor_pasivo == r.rastreable_id
        )).\
        join(u, r.rastreable_id == u.rastreable_p).\
        filter(u.usuario_id == self.usuario_id).\
        order_by(Registro.fecha_hora.desc()).all():
            resultado.append(formatear_entrada_registro(
                reg, self.peticion, self.tipo_de_rastreable
            ))

        return resultado

    @reify
    def consumidor_asociado(self):
        return DBSession.query(Consumidor).\
        filter_by(usuario_p = self.usuario_id).first()

    @reify
    def fecha_de_nacimiento(self):
        return formatear_fecha_para_paris(str(self.consumidor_asociado.fecha_de_nacimiento)) \
        if self.consumidor_asociado is not None \
        else None

    @reify
    def clientes_asociados(self):
        resultado = []

        x1 = DBSession.query(Cliente, case([
            (Cliente.rif == Tienda.cliente_p, 'tienda')
        ]),
        case([
            (Cliente.rif == Tienda.cliente_p, Tienda.tienda_id)
        ])).\
        filter(and_(
            Cliente.rif == Tienda.cliente_p, 
            Cliente.propietario == self.usuario_id
        ))

        x2 = DBSession.query(Cliente, case([
            (Cliente.rif == Patrocinante.cliente_p, 'patrocinante')
        ]),
        case([
            (Cliente.rif == Patrocinante.cliente_p, Patrocinante.patrocinante_id)
        ])).\
        filter(and_(
            Cliente.rif == Patrocinante.cliente_p, 
            Cliente.propietario == self.usuario_id
        ))

        tmp = x1.union(x2).all()
        for cli, tipo, _id in tmp:
            enlace = {
                'tienda': lambda x: self.peticion.route_url('tienda', tienda_id = x),
                'patrocinante': lambda x: self.peticion.route_url('patrocinante', patrocinante_id = x)
            }[tipo](_id)
            dato = {
                'tipo': tipo,
                'tipo_id': _id,
                'enlace': enlace
            }
            resultado.append(dict(dato.items() + cli.__dict__.items()))
        return resultado

    @reify
    def tiendas_asociadas(self):
        return DBSession.query(Tienda).\
        join(Cliente).\
        filter(Cliente.propietario == self.usuario_id).all()

    @reify
    def patrocinantes_asociados(self):
        return DBSession.query(Patrocinante).\
        join(Cliente).\
        filter(Cliente.propietario == self.usuario_id).all()

    @reify
    def calificaciones_resenas(self):
        var_comentarios = DBSession.query(CalificacionResena).\
        join(Consumidor).\
        join(Usuario).\
        filter(Usuario.usuario_id == self.usuario_id).all()

        return formatear_comentarios(var_comentarios)

    @view_config(route_name='usuario', renderer='../plantillas/usuario.pt', request_method='GET')
    @view_config(route_name='usuario', renderer='../plantillas/usuario.pt', request_method='POST')
    def usuario_view(self):
        editar = False
        aviso = None

        if self.usuario is None:
            return HTTPNotFound(MENSAJE_DE_ERROR)

        autentificado = authenticated_userid(self.peticion)

        if autentificado:
            usuario_autentificado = self.obtener_usuario('correo_electronico', autentificado)
            editar = True if usuario_autentificado.usuario_id == self.usuario.usuario_id else False
            
            if editar and ('guardar' in self.peticion.POST):
                resultado = editar_usuario(dict(self.peticion.POST), self.usuario_id)
                aviso = { 'error': 'Error', 'mensaje': resultado['error'] } \
                if (resultado['error'] is not None) \
                else { 'error': 'OK', 'mensaje': 'Datos actualizados correctamente' }

        return {
            'pagina': 'Usuario', 
            'usuario': self.usuario, 
            'autentificado': autentificado, 
            'aviso': aviso, 
            'editar': editar
        }