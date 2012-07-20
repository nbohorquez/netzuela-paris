'''
Created on 20/07/2012

@author: nestor
'''

from .formulario_registro import FormularioConsumidor, FormularioUsuario, FormularioTienda
from .models import DBSession
from formencode.api import Invalid
from sqlalchemy.sql import select, func, bindparam
from time import strftime, strptime
import bcrypt
    
class Spuria(object):
    creador = 1
    
    @staticmethod
    def crear_usuario(parametros):
        resultado = {}
        try:
            valido = FormularioUsuario.to_python(parametros)
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
                a_creador = Spuria.creador,
                a_nombre = valido['nombre'], 
                a_apellido = valido['apellido'],
                a_estatus = 'Activo',
                a_ubicacion = valido['ubicacion'], 
                a_correo_electronico = valido['correo_electronico'],
                a_contrasena = bcrypt.hashpw(valido['contrasena'], bcrypt.gensalt())
            )).scalar()
            DBSession.execute('commit')
            
            if usuario == -1048 or usuario == -1452 or usuario == -1062:
                error = 'Registro de usuario no exitoso'                                    
            resultado['error'] = error
            resultado['usuario'] = usuario
            
        return resultado
    
    @staticmethod
    def crear_tienda(parametros, propietario):
        resultado = {}
        try:
            valido = FormularioTienda.to_python(parametros)
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
                a_edificio_cc = valido['edificio_cc'], 
                a_piso = valido['piso'],
                a_apartamento = valido['apartamento'],
                a_local = valido['local_no'],
                a_casa = valido['casa'],
                a_calle = valido['calle'],
                a_sector_urb_barrio = valido['urbanizacion'], 
                a_pagina_web = valido['pagina_web'], 
                a_facebook = valido['facebook'],
                a_twitter = valido['twitter'],
                a_correo_electronico_publico = valido['correo_electronico_publico']
            )).scalar()
            DBSession.execute('commit')
            
            if tienda == -1048 or tienda == -1452 or tienda == -1062:
                error = 'Registro de tienda no exitoso.'                    
            resultado['error'] = error
            resultado['tienda'] = tienda
            
        return resultado
    
    @staticmethod
    def crear_consumidor(parametros):
        resultado = {}
        try:
            valido = FormularioConsumidor.to_python(parametros)
        except Invalid as e:
            resultado['error'] = e.msg
            resultado['consumidor'] = -1
        else:
            error = None
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
                a_creador = Spuria.creador,
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
                error = 'Registro de consumidor no exitoso'
            resultado['error'] = error
            resultado['consumidor'] = consumidor
            
        return resultado
    
    @staticmethod
    def crear_consumidor2(parametros, usuario):
        resultado = {}
        try:
            valido = FormularioConsumidor.to_python(parametros)
        except Invalid as e:
            resultado['error'] = e.msg
            resultado['consumidor'] = -1
        else:
            error = None
            sql = select([func.InsertarConsumidor2(
                bindparam('a_usuario_id'), 
                bindparam('a_sexo'),
                bindparam('a_fecha_de_nacimiento'),
                bindparam('a_grupo_de_edad'),
                bindparam('a_grado_de_instruccion'),
            )])

            fecha_time = strptime(valido['fecha_de_nacimiento'], '%d/%m/%Y')
            fecha_string = strftime('%Y-%m-%d', fecha_time)
            
            DBSession.execute('begin')
            consumidor = DBSession.execute(sql, params=dict(
                a_usuario_id = usuario,
                a_sexo = valido['sexo'],
                a_fecha_de_nacimiento = fecha_string,
                a_grupo_de_edad = 'Adultos jovenes',
                a_grado_de_instruccion = valido['grado_de_instruccion']
            )).scalar()
            DBSession.execute('commit')
            
            if consumidor == -1048 or consumidor == -1452 or consumidor == -1062:
                error = 'Registro de consumidor no exitoso'
            resultado['error'] = error
            resultado['consumidor'] = consumidor
            
        return resultado