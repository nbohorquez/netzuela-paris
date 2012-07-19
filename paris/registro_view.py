# -*- coding: utf-8 -*-
'''
Created on 07/06/2012

@author: nestor
'''

from .comunes import comunes
from .constantes import CREADOR
from .diagramas import diagramas
from .models import DBSession
from .formulario_registro import formulario_consumidor, formulario_usuario, formulario_tienda
from formencode.api import Invalid
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from sqlalchemy.sql import select, func, bindparam
from time import strftime, strptime
import bcrypt

class registro_view(diagramas, comunes):
    def __init__(self, peticion):
        self.peticion = peticion
        registro_url = peticion.route_url('registro_consumidor')
        self.pagina_actual = peticion.url
        self.referido_por = peticion.url if (peticion.url != registro_url) else '/'

    @reify
    def peticion(self):
        return self.peticion
    
    @reify
    def pagina_actual(self):
        return self.pagina_actual
    
    @reify
    def pagina_anterior(self):
        return self.peticion.params.get('pagina_anterior', self.referido_por)
    
    @view_config(route_name='registro_consumidor', renderer='plantillas/registro_consumidor.pt')
    def registro_consumidor_view(self):
        resultado = {'pagina': 'Registro de consumidor', 'mensaje': ''}
        if 'enviar' in self.peticion.params:      
            try:
                valido = formulario_consumidor.to_python(dict(self.peticion.params))
            except Invalid as e:
                resultado['mensaje'] = e.msg
            else:
                sql = select([func.InsertarConsumidor(
                    bindparam('a_creador'), 
                    bindparam('a_nombre'), 
                    bindparam('a_apellido'),
                    bindparam('a_estatus'),
                    bindparam('a_sexo'),
                    bindparam('a_fecha_de_nacimiento'),
                    bindparam('a_grupo_de_edad'),
                    bindparam('a_grado_de_instruccion'),
                    bindparam('a_ubicacion'),
                    bindparam('a_correo_electronico'),
                    bindparam('a_contrasena')
                )])
                
                """
                Como yo llamo a las funciones de spuria con SELECT, SQLAlchemy automaticamente hace
                un ROLLBACK de todo lo que hizo el SELECT ya que esa instruccion no deberia generar 
                ningun cambio en la base de datos. 
                
                Para anular este comportamiento, hay que encapsular la transaccion entre las instrucciones
                connection.begin() y connection.commit(). Lee:            
                http://stackoverflow.com/questions/7559570/make-sqlalchemy-commit-instead-of-rollback-after-a-select-query
                """
                fecha_time = strptime(valido['fecha_de_nacimiento'], '%d/%m/%Y')
                fecha_string = strftime('%Y-%m-%d', fecha_time)
                
                DBSession.execute('begin')
                consumidor = DBSession.execute(sql, params=dict(
                    a_creador = CREADOR,
                    a_nombre = valido['nombre'],
                    a_apellido = valido['apellido'],
                    a_estatus = 'Activo',
                    a_sexo = valido['sexo'],
                    a_fecha_de_nacimiento = fecha_string,
                    a_grupo_de_edad = 'Adultos jovenes',
                    a_grado_de_instruccion = valido['grado_de_instruccion'],
                    a_ubicacion = valido['ubicacion'],
                    a_correo_electronico = valido['correo_electronico'],
                    a_contrasena = bcrypt.hashpw(valido['contrasena'], bcrypt.gensalt())
                )).scalar()
                DBSession.execute('commit')
                
                if consumidor == -1048 or consumidor == -1452 or consumidor == -1062:
                    resultado['mensaje'] = 'Problemas internos del servidor. Intentelo nuevamente'
                else:
                    resultado['mensaje'] = 'Registro completado con éxito'
        elif 'cancelar' in self.peticion.params:
            resultado = HTTPFound(location = self.pagina_anterior)
        
        return resultado   
    
    @view_config(route_name='registro_tienda', renderer='plantillas/registro_tienda.pt')
    def registro_tienda_view(self):
        def crear_usuario(parametros):
            resultado = {}
            try:
                valido = formulario_usuario.to_python(dict(parametros))
            except Invalid as e:
                resultado['error'] = e.msg
                resultado['usuario'] = -1
            else:
                error = None
                sql = select([func.InsertarUsuario(
                    bindparam('a_creador'), 
                    bindparam('a_nombre'), 
                    bindparam('a_apellido'),
                    bindparam('a_estatus'),
                    bindparam('a_ubicacion'),
                    bindparam('a_correo_electronico'),
                    bindparam('a_contrasena')
                )])
                
                DBSession.execute('begin')
                usuario = DBSession.execute(sql, params=dict(
                    a_creador = CREADOR,
                    a_nombre = valido['nombre'], 
                    a_apellido = valido['apellido'],
                    a_estatus = 'Activo',
                    a_ubicacion = None, 
                    a_correo_electronico = valido['correo_electronico'],
                    a_contrasena = bcrypt.hashpw(valido['contrasena'], bcrypt.gensalt())
                )).scalar()
                DBSession.execute('commit')
                
                if usuario == -1048:
                    error = 'Error de valor nulo en InsertarUsuario()'
                elif usuario == -1452:
                    error = 'Error de clave externa en InsertarUsuario()'
                elif usuario == -1062:
                    error = 'Error de valor duplicado en InsertarUsuario()'
                                        
                resultado['error'] = error
                resultado['usuario'] = usuario
                
            return resultado
        def crear_tienda(parametros, propietario):
            resultado = {}
            try:
                valido = formulario_tienda.to_python(dict(parametros))
            except Invalid as e:
                resultado['error'] = e.msg
                resultado['tienda'] = -1
            else:
                error = None
                sql = select([func.InsertarTienda(
                    bindparam('a_propietario'), 
                    bindparam('a_ubicacion'), 
                    bindparam('a_rif'),
                    bindparam('a_categoria'),
                    bindparam('a_estatus'),
                    bindparam('a_nombre_legal'),
                    bindparam('a_nombre_comun'),
                    bindparam('a_telefono'), 
                    bindparam('a_edificio_cc'), 
                    bindparam('a_piso'),
                    bindparam('a_apartamento'),
                    bindparam('a_local'),
                    bindparam('a_casa'),
                    bindparam('a_calle'),
                    bindparam('a_sector_urb_barrio'), 
                    bindparam('a_pagina_web'), 
                    bindparam('a_facebook'),
                    bindparam('a_twitter'),
                    bindparam('a_correo_electronico_publico')
                )])
                
                DBSession.execute('begin')
                tienda = DBSession.execute(sql, params=dict(
                    a_propietario = propietario, 
                    a_ubicacion = valido['ubicacion'], 
                    a_rif = valido['rif'].replace('-',''),
                    a_categoria = valido['categoria'],
                    a_estatus = 'Activo',
                    a_nombre_legal = valido['nombre_legal'],
                    a_nombre_comun = valido['nombre_comun'],
                    a_telefono = valido['telefono'].replace('-',''), 
                    a_edificio_cc = None, 
                    a_piso = None,
                    a_apartamento = None,
                    a_local = None,
                    a_casa = None,
                    a_calle = valido['calle'],
                    a_sector_urb_barrio = valido['urbanizacion'], 
                    a_pagina_web = None, 
                    a_facebook = None,
                    a_twitter = None,
                    a_correo_electronico_publico = None
                )).scalar()
                DBSession.execute('commit')
                
                if tienda == -1048 or tienda == -1452 or tienda == -1062:
                    error = 'Registro de tienda no exitoso.'                    
                resultado['error'] = error
                resultado['tienda'] = tienda
                
            return resultado
        
        resultado = {'pagina': 'Registro de tienda', 'mensaje': ''}
        if 'enviar' in self.peticion.params:
            usuario = crear_usuario(self.peticion.params)
            
            if (usuario['error'] is not None):
                resultado['mensaje'] = usuario['error']
            else:
                tienda = crear_tienda(self.peticion.params, usuario['usuario'])
                resultado['mensaje'] = tienda['error'] if (tienda['error'] is not None) else 'Registro completado con éxito' 
        elif 'cancelar' in self.peticion.params:
            resultado = HTTPFound(location = self.pagina_anterior)
        return resultado