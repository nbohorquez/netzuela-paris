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
from zope.sqlalchemy import ZopeTransactionExtension
import bcrypt
import transaction

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
__formatear_fecha_para_mysql = None
__FormularioAgregarConsumidor = None
__FormularioCrearUsuario = None
__FormularioCrearTienda = None
__FormularioCrearConsumidor = None
__FormularioEditarUsuario = None
__FormularioEditarConsumidor = None
__FormularioEditarProducto = None
__FormularioEditarDireccion = None
__CategoriaValida = None
__TextoValido = None

# Codigo tomado de: http://danielkaes.wordpress.com/2009/07/30/create-new-classes-with-python-at-runtime/    
def __mixIn(classname, parentclasses):
    if len(parentclasses) > 0:
        parents = map(lambda p:p.__name__, parentclasses)
        createclass = "class %s (%s):\n\tpass" % (classname, ",".join(parents))
    else:
        createclass = "class %s:\n\tpass" % classname
    exec createclass
    globals()[classname] = eval(classname)
            
creador = 1
acciones = { 
    'Insertar': 'agrego',
    'Abrir': 'abrio',
    'Actualizar': 'actualizo',
    'Eliminar': 'elimino',
    'Bloquear': 'bloqueo',
    'Abrir sesion': 'abrio sesion',
    'Cerrar sesion': 'cerro sesion'
}
__tablas = [
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

def inicializar(motor):
    __cargar_tablas(motor)
    paris_formularios = __import__('paris.formularios', fromlist = [
        'CategoriaValida',
        'FormularioAgregarConsumidor',
        'FormularioCrearUsuario',
        'FormularioCrearTienda',
        'FormularioCrearConsumidor',
        'FormularioEditarUsuario',
        'FormularioEditarConsumidor',
        'FormularioEditarProducto',
    ])
    paris_comunes = __import__('paris.comunes', fromlist = ['formatear_fecha_para_mysql'])
    
    global __formatear_fecha_para_mysql
    global __CategoriaValida
    global __FormularioAgregarConsumidor
    global __FormularioCrearUsuario
    global __FormularioCrearTienda
    global __FormularioCrearConsumidor
    global __FormularioEditarUsuario
    global __FormularioEditarConsumidor
    global __FormularioEditarProducto
    global __FormularioEditarDireccion
    global __TextoValido
    
    __formatear_fecha_para_mysql = paris_comunes.formatear_fecha_para_mysql    
    __CategoriaValida = paris_formularios.CategoriaValida
    __FormularioAgregarConsumidor = paris_formularios.FormularioAgregarConsumidor
    __FormularioCrearUsuario = paris_formularios.FormularioCrearUsuario
    __FormularioCrearTienda = paris_formularios.FormularioCrearTienda
    __FormularioCrearConsumidor = paris_formularios.FormularioCrearConsumidor
    __FormularioEditarUsuario = paris_formularios.FormularioEditarUsuario
    __FormularioEditarConsumidor = paris_formularios.FormularioEditarConsumidor
    __FormularioEditarProducto = paris_formularios.FormularioEditarProducto
    __FormularioEditarDireccion = paris_formularios.FormularioEditarDireccion
    __TextoValido = paris_formularios.TextoValido
    
# Asocia las tablas de la base de datos con clases en python
def __cargar_tablas(motor):
    metadata = MetaData(motor)
    for asociacion in __tablas:
        tabla = asociacion
        objeto = asociacion
        esquema_tabla = Table(tabla, metadata, autoload=True)
        __mixIn(objeto, [object])
        mapper(globals()[objeto], esquema_tabla)
    
    # Cargamos el primer "diferente": la vista inventario_reciente. Esta no tiene PK definida.
    esquema_tabla = Table('inventario_reciente', metadata,
                        Column('tienda_id', Integer, primary_key=True),
                        Column('codigo', String, primary_key=True),
                        autoload=True)
    __mixIn('inventario_reciente', [object])
    mapper(globals()['inventario_reciente'], esquema_tabla)
    
    # Cargamos el segundo "diferente": la vista tamano_reciente. Tampoco tiene PK definida.
    esquema_tabla = Table('tamano_reciente', metadata,
                        Column('tienda_id', Integer, primary_key=True),
                        Column('fecha_inicio', String, primary_key=True),
                        autoload=True)
    __mixIn('tamano_reciente', [object])
    mapper(globals()['tamano_reciente'], esquema_tabla)
    
def agregar_consumidor(parametros, usuario_id):
    resultado = {}
    try:
        valido = __FormularioAgregarConsumidor.to_python(parametros)
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

        fecha_string = __formatear_fecha_para_mysql(str(valido['fecha_de_nacimiento']))
        
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

def crear_usuario(parametros):
    resultado = {}
    try:
        valido = __FormularioCrearUsuario.to_python(parametros)
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
            a_creador = creador,
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
   
def crear_tienda(parametros, propietario):
    resultado = {}
    try:
        valido = __FormularioCrearTienda.to_python(parametros)
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

def crear_consumidor(parametros):
    resultado = {}
    try:
        valido = __FormularioCrearConsumidor.to_python(parametros)
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
        
        fecha_string = __formatear_fecha_para_mysql(str(valido['fecha_de_nacimiento']))
        
        DBSession.execute('begin')
        consumidor = DBSession.execute(sql, params=dict(
            a_creador = creador,
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

def editar_usuario(parametros, _id):
    resultado = {'error': None, 'consumidor': None}
    try:
        valido = __FormularioEditarUsuario.to_python(parametros)
        
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
            con_id = con.consumidor_id if con is not None else None
            tmp = editar_consumidor(parametros, con.consumidor_id) if con is not None else agregar_consumidor(parametros, _id)
            
            if isinstance(tmp, dict):
                if 'consumidor' in tmp:
                    resultado['consumidor'] = tmp['consumidor']
                resultado['error'] = tmp['error']
            else:
                resultado['error'] = tmp
                resultado['consumidor'] = con_id
            
    except Invalid as e:
        resultado['error'] = e.msg
    finally:
        return resultado
    """
    except AttributeError as e:
        resultado['error'] = 'Usuario no existe'
    """

def editar_consumidor(parametros, _id):
    error = None        
    try:
        valido = __FormularioEditarConsumidor.to_python(parametros)
        fecha_string = lambda: __formatear_fecha_para_mysql(str(valido['fecha_de_nacimiento'])) \
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
    finally:
        return error
    """
    except AttributeError as e:
        error = 'Consumidor no existe'
    """

def editar_producto(parametros, _id):
    error = None        
    try:
        pro = DBSession.query(producto).filter_by(producto_id = _id).first()
        if 'fabricante' in parametros:
            valido = __FormularioEditarProducto.to_python(parametros)
            """
            fecha_string = __formatear_fecha_para_mysql(str(valido['debut_en_el_mercado']))
            """
            pro.fabricante = valido['fabricante'] if pro.fabricante != valido['fabricante'] else pro.fabricante
            pro.modelo = valido['modelo'] if pro.modelo != valido['modelo'] else pro.modelo
            pro.nombre = valido['nombre'] if pro.nombre != valido['nombre'] else pro.nombre
            pro.debut_en_el_mercado = valido['debut_en_el_mercado'] if pro.debut_en_el_mercado != valido['debut_en_el_mercado'] else pro.debut_en_el_mercado
            pro.largo = valido['largo'] if pro.largo != valido['largo'] else pro.largo
            pro.ancho = valido['ancho'] if pro.ancho != valido['ancho'] else pro.ancho
            pro.alto = valido['alto'] if pro.alto != valido['alto'] else pro.alto
            pro.peso = valido['peso'] if pro.peso != valido['peso'] else pro.peso
            pro.pais_de_origen = valido['pais_de_origen'] if pro.pais_de_origen != valido['pais_de_origen'] else pro.pais_de_origen
            transaction.commit()
        elif 'categoria' in parametros:
            valido = __CategoriaValida.to_python(parametros['categoria'])
            pro.categoria = valido if pro.categoria != valido else pro.categoria 
            transaction.commit()
        elif 'descripcion' in parametros:
            valido = __TextoValido.to_python(parametros['descripcion'])
            des = DBSession.query(descripcion).filter_by(describible = pro.describible_p).first()
            des.contenido = valido if des.contenido != valido else des.contenido
            transaction.commit()
    except Invalid as e:
        error = e.msg
    finally:
        return error
    """
    except AttributeError as e:
        error = 'Consumidor no existe'
    """    

def editar_tienda(parametros, _id):
    error = None        
    try:
        tie = DBSession.query(cliente).\
        join(tienda).\
        filter(tienda.tienda_id == _id).first()
        if 'calle' in parametros:
            valido = __FormularioEditarDireccion.to_python(parametros)
            tie.edificio_cc = valido['edificio'] if tie.edificio_cc != valido['edificio'] else tie.edificio_cc
            tie.piso = valido['piso'] if tie.piso != valido['piso'] else tie.piso
            tie.apartamento = valido['apartamento'] if tie.apartamento != valido['apartamento'] else tie.apartamento
            tie.local_no = valido['local_no'] if tie.local_no != valido['local_no'] else tie.local_no
            tie.casa = valido['casa'] if tie.casa != valido['casa'] else tie.casa
            tie.calle = valido['calle'] if tie.calle != valido['calle'] else tie.calle
            tie.sector_urb_barrio = valido['urbanizacion'] if tie.sector_urb_barrio != valido['urbanizacion'] else tie.sector_urb_barrio
            tie.ubicacion = valido['ubicacion'] if tie.ubicacion != valido['ubicacion'] else tie.ubicacion 
            transaction.commit()
        elif 'categoria' in parametros:
            valido = __CategoriaValida.to_python(parametros['categoria'])
            tie.categoria = valido if tie.categoria != valido else tie.categoria 
            transaction.commit()
        elif 'descripcion' in parametros:
            valido = __TextoValido.to_python(parametros['descripcion'])
            des = DBSession.query(descripcion).filter_by(describible = tie.describible_p).first()
            des.contenido = valido if des.contenido != valido else des.contenido
            transaction.commit()
    except Invalid as e:
        error = e.msg
    finally:
        return error
    """
    except AttributeError as e:
        error = 'Consumidor no existe'
    """