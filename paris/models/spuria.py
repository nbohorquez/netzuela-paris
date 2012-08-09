# -*- coding: utf-8 -*-
'''
Created on 20/07/2012

@author: nestor
'''

#from .formularios import FormularioConsumidor, FormularioUsuario, FormularioTienda
from formencode.api import Invalid
from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker, mapper
from sqlalchemy.sql import select, func, bindparam
from time import strftime, strptime
from zope.sqlalchemy import ZopeTransactionExtension
import bcrypt
import transaction

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

# Codigo tomado de: http://danielkaes.wordpress.com/2009/07/30/create-new-classes-with-python-at-runtime/    
def mixIn(classname, parentclasses):
    if len(parentclasses) > 0:
        parents = map(lambda p:p.__name__, parentclasses)
        createclass = "class %s (%s):\n\tpass" % (classname, ",".join(parents))
    else:
        createclass = "class %s:\n\tpass" % classname
    exec createclass
    globals()[classname] = eval(classname)
            
class Spuria(object):
    creador = 1    
    accion = { 
        'Insertar': 'agrego',
        'Abrir': 'abrio',
        'Actualizar': 'actualizo',
        'Eliminar': 'elimino',
        'Bloquear': 'bloqueo',
        'Abrir sesion': 'abrio sesion',
        'Cerrar sesion': 'cerro sesion'
    }
    tablas = [
        'acceso',
        'accion',
        'administrador',
        'buscable',
        'busqueda',
        'calificable_seguible',
        'calificacion',
        'calificacion_resena',
        'categoria',
        'cliente',
        'cobrable',
        'codigo_de_error',
        'consumidor',
        'consumidor_objetivo',
        'contador_de_exhibiciones',
        'croquis',
        'describible',
        'descripcion',
        'dia',
        'dibujable',
        'estadisticas',
        'estadisticas_de_influencia',
        'estadisticas_de_popularidad',
        'estadisticas_de_visitas',
        'estadisticas_temporales',
        'estatus',
        'etiqueta',
        'etiquetable',
        'factura',
        'foto',
        'grado_de_instruccion',
        'grado_de_instruccion_objetivo',
        'grupo_de_edad',
        'grupo_de_edad_objetivo',
        'horario_de_trabajo',
        'idioma',
        'interlocutor',
        'inventario',
        'mensaje',
        'palabra',
        'patrocinante',
        'precio_cantidad',
        'privilegios',
        'producto',
        'publicidad',
        'punto',
        'punto_de_croquis',
        'rastreable',
        'region',
        'region_territorio',
        'registro',
        'relacion_de_palabras',
        'resultado_de_busqueda',
        'seguidor',
        'servicio_vendido',
        'sexo',
        'sexo_objetivo',
        'tamano',
        'territorio',
        'territorio_objetivo',
        'tienda',
        'tiendas_consumidores',
        'tipo_de_codigo',
        'turno',
        'usuario',
        'visibilidad',
    ]
    columnas_no_visibles = [
        'cliente_p',
        'estadisticas_id',
        'estadisticas_p',
        'etiquetable_id',
        'etiquetable_p',
        'rastreable_id',
        'rastreable_p',
        'describible_id',
        'describible_p',
        'dibujable_id',
        'dibujable_p',
        'buscable_id',
        'buscable_p',
        'calificable_seguible_id',
        'calificable_seguible_p',
        'cobrable_id',
        'cobrable_p',
        'interlocutor_id',
        'interlocutor_p',
        'usuario_id',
        'usuario_p',
        
        'tienda_id',
        'patrocinante_id',
        'publicidad_id',
        'palabra_id',
        'etiqueta_id',        
        'mensaje_id',
        'descripcion_id',
        'producto_id',
        'foto_id',
        'punto_id',
        'croquis_id',
        'region_id',
        'territorio_id',
        'busqueda_id',
        'acceso_id',
        'factura_id',
        'consumidor_id',
        'calificacion_resena_id',
        
        'ruta_de_foto',
        'describible',
        'dibujable',
        'calificable_seguible',
        'estatus',
        'visibilidad',
        'usuario',
        'cliente',
        'propietario',
        'fecha_inicio'
    ]
    
    _FormularioAgregarConsumidor = None
    _FormularioCrearUsuario = None
    _FormularioCrearTienda = None
    _FormularioCrearConsumidor = None
    _FormularioEditarUsuario = None
    _FormularioEditarConsumidor = None
    
    @staticmethod
    def formatear_fecha_para_mysql(fecha):
        fecha_neutra = strptime(fecha, '%d/%m/%Y')
        return strftime('%Y-%m-%d', fecha_neutra)
    
    @staticmethod
    def inicializar(motor):
        Spuria.cargar_tablas(motor)
        paris_formularios = __import__('paris.formularios', fromlist = [
            'FormularioEditarConsumidor', 
            'FormularioCrearUsuario',
            'FormularioCrearTienda',
            'FormularioCrearConsumidor',
            'FormularioEditarUsuario',
        ])
        Spuria._FormularioAgregarConsumidor = getattr(paris_formularios, 'FormularioAgregarConsumidor')
        Spuria._FormularioCrearUsuario = getattr(paris_formularios, 'FormularioCrearUsuario')
        Spuria._FormularioCrearTienda = getattr(paris_formularios, 'FormularioCrearTienda')
        Spuria._FormularioCrearConsumidor = getattr(paris_formularios, 'FormularioCrearConsumidor')
        Spuria._FormularioEditarUsuario = getattr(paris_formularios, 'FormularioEditarUsuario')
        Spuria._FormularioEditarConsumidor = getattr(paris_formularios, 'FormularioEditarConsumidor')
        
    # Asocia las tablas de la base de datos con clases en python
    @staticmethod
    def cargar_tablas(motor):
        metadata = MetaData(motor)
        for asociacion in Spuria.tablas:
            tabla = asociacion
            objeto = asociacion
            esquema_tabla = Table(tabla, metadata, autoload=True)
            mixIn(objeto, [object])
            mapper(globals()[objeto], esquema_tabla)
        
        # Cargamos el primer "diferente": la vista inventario_reciente. Esta no tiene PK definida.
        esquema_tabla = Table('inventario_reciente', metadata,
                            Column('tienda_id', Integer, primary_key=True),
                            Column('codigo', String, primary_key=True),
                            autoload=True)
        mixIn('inventario_reciente', [object])
        mapper(globals()['inventario_reciente'], esquema_tabla)
        
        # Cargamos el segundo "diferente": la vista tamano_reciente. Tampoco tiene PK definida.
        esquema_tabla = Table('tamano_reciente', metadata,
                            Column('tienda_id', Integer, primary_key=True),
                            Column('fecha_inicio', String, primary_key=True),
                            autoload=True)
        mixIn('tamano_reciente', [object])
        mapper(globals()['tamano_reciente'], esquema_tabla)
        
    @staticmethod
    def agregar_consumidor(parametros, usuario_id):
        resultado = {}
        try:
            valido = Spuria._FormularioAgregarConsumidor.to_python(parametros)
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

            fecha_string = Spuria.formatear_fecha_para_mysql(str(valido['fecha_de_nacimiento']))
            
            DBSession.execute('begin')
            consumidor = DBSession.execute(sql, params=dict(
                a_usuario_id = usuario_id,
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
    
    @staticmethod
    def crear_usuario(parametros):
        resultado = {}
        try:
            valido = Spuria._FormularioCrearUsuario.to_python(parametros)
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
            valido = Spuria._FormularioCrearTienda.to_python(parametros)
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
            valido = Spuria._FormularioCrearConsumidor.to_python(parametros)
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
            
            fecha_string = Spuria.formatear_fecha_para_mysql(str(valido['fecha_de_nacimiento']))
            
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
    def editar_usuario(parametros, _id):
        resultado = {'error': None, 'consumidor': None}
        try:
            valido = Spuria._FormularioEditarUsuario.to_python(parametros)
            
            usu = DBSession.query(usuario).filter_by(usuario_id = _id).first()
            usu.nombre = valido['nombre'] if usu.nombre != valido['nombre'] else usu.nombre
            usu.apellido = valido['apellido'] if usu.apellido != valido['apellido'] else usu.apellido
            usu.ubicacion = valido['ubicacion'] if usu.ubicacion != valido['ubicacion'] else usu.ubicacion
            """
            Aqui hay una buena explicacion de por que tengo que hacer transaction.commit() y 
            no DBSession.commit() 
            http://turbogears.org/2.0/docs/main/Wiki20/wiki20.html#initializing-the-tables
            """
            transaction.commit()
            
            # Si ya hay un consumidor asociado a este usuario lo editamos, sino, lo creamos
            if 'sexo' in parametros or 'fecha_de_nacimiento' in parametros or 'grado_de_instruccion' in parametros:
                con = DBSession.query(consumidor).filter_by(usuario_p = _id).first()
                con_id = con.consumidor_id
                tmp = Spuria.agregar_consumidor(parametros, _id) if con is None else Spuria.editar_consumidor(parametros, con.consumidor_id)
                
                if isinstance(tmp, dict):
                    if 'consumidor' in tmp:
                        resultado['consumidor'] = tmp['consumidor']
                    resultado['error'] = tmp['error']
                else:
                    resultado['error'] = tmp
                    resultado['consumidor'] = con_id
                
        except Invalid as e:
            resultado['error'] = e.msg
        except AttributeError as e:
            resultado['error'] = 'Usuario no existe'
            
        return resultado
    
    @staticmethod
    def editar_consumidor(parametros, _id):
        error = None        
        try:
            valido = Spuria._FormularioEditarConsumidor.to_python(parametros)
            
            fecha_string = lambda: Spuria.formatear_fecha_para_mysql(str(valido['fecha_de_nacimiento'])) \
            if 'fecha_de_nacimiento' in valido \
            else None
            
            con = DBSession.query(consumidor).filter_by(consumidor_id = _id).first()
            
            con.sexo = valido['sexo'] \
            if 'sexo' in valido and con.sexo != valido['sexo'] \
            else con.sexo
            
            con.fecha_de_nacimiento = fecha_string \
            if fecha_string is not None and con.fecha_de_nacimiento != fecha_string \
            else con.fecha_de_nacimiento
            
            con.grado_de_instruccion = valido['grado_de_instruccion'] \
            if 'grado_de_instruccion' in valido and con.grado_de_instruccion != valido['grado_de_instruccion'] \
            else con.grado_de_instruccion
            
            transaction.commit()
        except Invalid as e:
            error = e.msg
        except AttributeError as e:
            error = 'Consumidor no existe'            
        return error