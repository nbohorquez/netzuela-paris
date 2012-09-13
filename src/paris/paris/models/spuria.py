# -*- coding: utf-8 -*-
'''
Created on 20/07/2012

@author: nestor
'''

from formencode.api import Invalid
from sqlalchemy import and_, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker, mapper
from sqlalchemy.sql import select, func, bindparam
from zope.sqlalchemy import ZopeTransactionExtension
import bcrypt, transaction

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

# Codigo tomado de:
# http://danielkaes.wordpress.com/2009/07/30/create-new-classes-with-python-at-runtime/    
def __mixIn(classname, parentclasses):
    if len(parentclasses) > 0:
        parents = map(lambda p:p.__name__, parentclasses)
        createclass = "class %s (%s):\n\tpass" % (classname, ",".join(parents))
    else:
        createclass = "class %s:\n\tpass" % classname
    exec createclass
    globals()[classname] = eval(classname)
            
root = 1
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
    
# Asocia las tablas de la base de datos con clases en python
def __cargar_tablas(motor):
    metadata = MetaData(motor)
    for asociacion in __tablas:
        tabla = asociacion
        objeto = asociacion
        esquema_tabla = Table(tabla, metadata, autoload=True)
        __mixIn(objeto, [object])
        mapper(globals()[objeto], esquema_tabla)
    
    # Cargamos el primer "diferente": la vista inventario_reciente. 
    # Esta no tiene PK definida.
    esquema_tabla = Table(
        'inventario_reciente', metadata,
        Column('tienda_id', Integer, primary_key=True),
        Column('codigo', String, primary_key=True),
        autoload=True
    )
    __mixIn('inventario_reciente', [object])
    mapper(globals()['inventario_reciente'], esquema_tabla)
    
    # Cargamos el segundo "diferente": la vista tamano_reciente. 
    # Tampoco tiene PK definida.
    esquema_tabla = Table(
        'tamano_reciente', metadata,
        Column('tienda_id', Integer, primary_key=True),
        Column('fecha_inicio', String, primary_key=True),
        autoload=True
    )
    __mixIn('tamano_reciente', [object])
    mapper(globals()['tamano_reciente'], esquema_tabla)
    
def agregar_consumidor(parametros, usuario_id):
    from paris.formularios import FormularioAgregarConsumidor
    from paris.comunes import formatear_fecha_para_mysql
    resultado = {}
    try:
        valido = FormularioAgregarConsumidor.to_python(parametros)
    except Invalid as e:
        resultado['error'] = e.msg
        resultado['consumidor'] = -1
    else:
        sql = select([func.InsertarConsumidor2(
            bindparam('a_usuario_id'), 
            bindparam('a_sexo'),
            bindparam('a_fecha_de_nacimiento'),
            bindparam('a_grupo_de_edad'),
            bindparam('a_grado_de_instruccion'),
        )])

        fecha_string = formatear_fecha_para_mysql(str(valido['fecha_de_nacimiento']))
        
        DBSession.execute('begin')
        consumidor = DBSession.execute(sql, params=dict(
            a_usuario_id = usuario_id,
            a_sexo = valido['sexo'],
            a_fecha_de_nacimiento = fecha_string,
            a_grupo_de_edad = 'Adultos jovenes',
            a_grado_de_instruccion = valido['grado_de_instruccion']
        )).scalar()
        DBSession.execute('commit')
        
        error = 'Registro de consumidor no exitoso' \
        if consumidor == -1048 or consumidor == -1452 or consumidor == -1062 \
        else None
        
        resultado['error'] = error
        resultado['consumidor'] = consumidor
        
    return resultado

def crear_usuario(parametros):
    from paris.formularios import FormularioCrearUsuario
    resultado = {}
    try:
        valido = FormularioCrearUsuario.to_python(parametros)
    except Invalid as e:
        resultado['error'] = e.msg
        resultado['usuario'] = -1
    else:
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
        usr = DBSession.execute(sql, params=dict(
            a_creador = root,
            a_nombre = valido['nombre'], 
            a_apellido = valido['apellido'],
            a_estatus = 'Activo',
            a_ubicacion = valido['ubicacion'], 
            a_correo_electronico = valido['correo_electronico'],
            a_contrasena = bcrypt.hashpw(valido['contrasena'], bcrypt.gensalt())
        )).scalar()
        DBSession.execute('commit')
        
        error = 'Registro de usuario no exitoso' \
        if usuario == -1048 or usuario == -1452 or usuario == -1062 \
        else None
                                                
        resultado['error'] = error
        resultado['usuario'] = int(usr)
        
    return resultado
   
def crear_tienda(parametros, propietario):
    from paris.formularios import FormularioCrearTienda
    resultado = {}
    try:
        valido = FormularioCrearTienda.to_python(parametros)
    except Invalid as e:
        resultado['error'] = e.msg
        resultado['tienda'] = -1
    else:
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
        tnd = DBSession.execute(sql, params=dict(
            a_propietario = propietario, 
            a_ubicacion = valido['ubicacion'], 
            a_rif = valido['rif'].replace('-',''),
            a_categoria = valido['categoria'],
            a_estatus = 'Activo',
            a_nombre_legal = valido['nombre_legal'],
            a_nombre_comun = valido['nombre_comun'],
            a_telefono = valido['telefono'].replace('-',''), 
            a_edificio_cc = valido['edificio'], 
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
        
        error = 'Registro de tienda no exitoso.' \
        if tnd == -1048 or tnd == -1452 or tnd == -1062 \
        else None
                            
        resultado['error'] = error
        resultado['tienda'] = int(tnd)
        
    return resultado

def crear_consumidor(parametros):
    from paris.formularios import FormularioCrearConsumidor
    from paris.comunes import formatear_fecha_para_mysql
    resultado = {}
    try:
        valido = FormularioCrearConsumidor.to_python(parametros)
    except Invalid as e:
        resultado['error'] = e.msg
        resultado['consumidor'] = -1
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
        Como yo llamo a las funciones de spuria con SELECT, SQLAlchemy automaticamente 
        hace un ROLLBACK de todo lo que hizo el SELECT ya que esa instruccion no deberia
        generar ningun cambio en la base de datos. 
        
        Para anular este comportamiento, hay que encapsular la transaccion entre las 
        instrucciones connection.begin() y connection.commit(). Lee:            
        http://stackoverflow.com/questions/7559570/make-sqlalchemy-commit-instead-of-rollback-after-a-select-query
        """
        
        fecha_string = formatear_fecha_para_mysql(str(valido['fecha_de_nacimiento']))
        
        DBSession.execute('begin')
        con = DBSession.execute(sql, params=dict(
            a_creador = root,
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
        
        error = 'Registro de consumidor no exitoso' \
        if con == -1048 or con == -1452 or con == -1062 \
        else None
        
        resultado['error'] = error
        resultado['consumidor'] = int(con)
        
    return resultado

def crear_horario_de_trabajo(parametros, tienda_dia):
    from paris.formularios import FormularioEditarHorarioDeTrabajo
    resultado = {}
    try:
        valido = FormularioEditarHorarioDeTrabajo.to_python(parametros)
    except Invalid as e:
        resultado['error'] = e.msg
        resultado['horario_de_trabajo'] = -1 
    else:
        laborable = True if valido['laborable'] == 'Abierto' else False
        sql = select([func.InsertarHorarioDeTrabajo(
            bindparam('a_tienda_id'),
            bindparam('a_dia'),
            bindparam('a_laborable')
        )])
        
        DBSession.execute('begin')
        horario = DBSession.execute(sql, params=dict(
            a_tienda_id = tienda_dia['tienda_id'],
            a_dia = tienda_dia['dia'],
            a_laborable = laborable
        )).scalar()
        DBSession.execute('commit')
        
        error = 'Registro de horario_de_trabajo no exitoso' \
        if horario == -1048 or horario == -1452 or horario == -1062 \
        else None
        
        resultado['error'] = error
        resultado['horario_de_trabajo'] = horario
        
    return resultado
    
def crear_turno(parametros, tienda_dia):
    from paris.formularios import FormularioEditarTurno
    resultado = {}
    try:
        valido = FormularioEditarTurno.to_python(parametros)
    except Invalid as e:
        resultado['error'] = e.msg
        resultado['turno'] = -1 
    else:
        ha = valido['hora_de_apertura']
        hc = valido['hora_de_cierre']
                    
        sql = select([func.InsertarTurno(
            bindparam('a_tienda_id'),
            bindparam('a_dia'),
            bindparam('a_hora_de_apertura'),
            bindparam('a_Hora_de_cierre')
        )])
            
        DBSession.execute('begin')
        trn = DBSession.execute(sql, params=dict(
            a_tienda_id = tienda_dia['tienda_id'],
            a_dia = tienda_dia['dia'],
            a_hora_de_apertura = '{}:{}:{}'.format(ha[0], ha[1], hc[2]),
            a_Hora_de_cierre = '{}:{}:{}'.format(hc[0], hc[1], hc[2])
        )).scalar()
        DBSession.execute('commit')
                    
        error = 'Registro de turno no exitoso' \
        if trn == -1048 or trn == -1452 or trn == -1062 \
        else None
        
        resultado['error'] = error
        resultado['turno'] = trn
        
    return resultado 

def crear_horarios_y_turnos(parametros, tienda_id):
    def agregar_a_lista(lista, dato):
        if not isinstance(lista, list):
            lista = []
        lista.append(dato)        
    """
    Estoy recibiendo claves de la forma:
    Lunes
    Lunes.hora_de_apertura.0
    Lunes.hora_de_cierre.0
    Lunes.hora_de_apertura.1
    Lunes.hora_de_cierre.1
    Martes
    Martes.hora_de_apertura.0
    Martes.hora_de_cierre.0
    ...
    """
    error = None
    
    claves = parametros.keys()
    dias = [x.valor for x in DBSession.query(dia).all()]
    
    # Procesamos cada dia de la semana
    for d in dias:
        hdt = DBSession.query(horario_de_trabajo).\
        filter(and_(
            horario_de_trabajo.tienda_id == tienda_id,
            horario_de_trabajo.dia == d
        )).first()
        
        tienda_dia = {'tienda_id': tienda_id, 'dia': d}
        laborable = {'laborable': parametros[d]}
        
        # Si la tienda no tiene un horario_de_trabajo para ese dia, se
        # crea uno. De lo contrario se edita el que ya existe
        res = crear_horario_de_trabajo(laborable, tienda_dia) \
        if hdt is None \
        else editar_horario_de_trabajo(laborable, tienda_dia)
            
        if res is not None:
            if isinstance(res, dict) and res['error'] is not None:
                agregar_a_lista(error, res['error'])
            else:
                agregar_a_lista(error, res)
    
        turnos_del_dia = DBSession.query(turno).\
        filter(and_(turno.tienda_id == tienda_id, turno.dia == d)).\
        all()
        
        # Borramos todos los turnos de ese dia
        for turn in turnos_del_dia:
            DBSession.delete(turn)
            transaction.commit()
        
        # El formato del dia es '<Dia>.' Ej: 'Lunes.', 'Martes.', etc    
        formato_del_dia = '{}.'.format(d)
        # Estas son las claves de cada dia. De la forma:
        # ['Lunes.hora_de_apertura.0', 'Lunes.hora_de_apertura.1', ...]
        claves_del_dia = [x for x in claves if formato_del_dia in x]
        # En turnos esta el indice mas alto de las claves del dia.
        # En el ejemplo anterior seria 1
        turnos = max([int(x.split('.')[2]) for x in claves_del_dia])
                    
        # Creamos nuevos turnos con la informacion que pasa el cliente
        for turn in range(0, turnos + 1):
            horas = {
                'hora_de_apertura': parametros['{}.hora_de_apertura.{}'.format(d, turn)], 
                'hora_de_cierre': parametros['{}.hora_de_cierre.{}'.format(d, turn)]
            } if parametros[d] == 'Abierto' \
            else {
                'hora_de_apertura': '00:00:00', 
                'hora_de_cierre': '00:00:00'
            }
            
            res = crear_turno(horas, tienda_dia)
            if res['error'] is not None:
                agregar_a_lista(error, res['error'])

    return error

def crear_descripcion(parametros, creador, describible):
    from paris.formularios import TextoValido
    resultado = {}
    try:
        valido = TextoValido.to_python(parametros['contenido'])
    except Invalid as e:
        resultado['error'] = e.msg
        resultado['descripcion'] = -1
    else:
        sql = select([func.InsertarDescripcion(
            bindparam('a_creador'),
            bindparam('a_describible'),
            bindparam('a_contenido')
        )])

        DBSession.execute('begin')
        des = DBSession.execute(sql, params=dict(
            a_creador = creador,
            a_describible = describible,
            a_contenido = valido
        )).scalar()
        DBSession.execute('commit')
                    
        error = 'Registro de descripcion no exitoso' \
        if des == -1048 or des == -1452 or des == -1062 \
        else None
        
        resultado['error'] = error
        resultado['descripcion'] = int(des)
        
    return resultado
    
def editar_usuario(parametros, _id):
    from paris.formularios import FormularioEditarUsuario
    resultado = {'error': None, 'consumidor': None}
    try:
        valido = FormularioEditarUsuario.to_python(parametros)
        
        usr = DBSession.query(usuario).filter_by(usuario_id = _id).first()
        
        usr.nombre = valido['nombre'] \
        if usr.nombre != valido['nombre'] else usr.nombre
        
        usr.apellido = valido['apellido'] \
        if usr.apellido != valido['apellido'] \
        else usr.apellido
        
        usr.ubicacion = valido['ubicacion'] \
        if usr.ubicacion != valido['ubicacion'] \
        else usr.ubicacion
        """
        Aqui hay una buena explicacion de por que tengo que hacer 
        transaction.commit() y no DBSession.commit() 
        http://turbogears.org/2.0/docs/main/Wiki20/wiki20.html#initializing-the-tables
        """
        transaction.commit()
        
        # Si ya hay un consumidor asociado a este usuario lo editamos, sino, 
        # lo creamos
        if 'sexo' in parametros \
        or 'fecha_de_nacimiento' in parametros \
        or 'grado_de_instruccion' in parametros:
            con = DBSession.query(consumidor).filter_by(usuario_p = _id).first()
            # Tengo que guardar con_id aqui porque DBSession hace un cambio de 
            # contexto cuando llamo a una funcion y pierde la referencia cuando 
            # vuelve otra vez aqui
            con_id = con.consumidor_id if con is not None else None
            
            tmp = editar_consumidor(parametros, con.consumidor_id) \
            if con is not None \
            else agregar_consumidor(parametros, _id)
            
            if isinstance(tmp, dict):
                if 'consumidor' in tmp:
                    resultado['consumidor'] = tmp['consumidor']
                resultado['error'] = tmp['error']
            else:
                resultado['error'] = tmp
                resultado['consumidor'] = int(con_id)
            
    except Invalid as e:
        resultado['error'] = e.msg
    except AttributeError as e:
        resultado['error'] = 'Usuario no existe'
    finally:
        return resultado

def editar_consumidor(parametros, _id):
    from paris.comunes import formatear_fecha_para_mysql
    from paris.formularios import FormularioEditarConsumidor
    error = None        
    try:
        valido = FormularioEditarConsumidor.to_python(parametros)
        con = DBSession.query(consumidor).filter_by(consumidor_id = _id).first()
        
        fecha_string = \
        lambda: formatear_fecha_para_mysql(str(valido['fecha_de_nacimiento'])) \
        if 'fecha_de_nacimiento' in valido \
        else None

        con.sexo = valido['sexo'] \
        if 'sexo' in valido and con.sexo != valido['sexo'] \
        else con.sexo
        
        con.fecha_de_nacimiento = fecha_string \
        if fecha_string is not None and con.fecha_de_nacimiento != fecha_string \
        else con.fecha_de_nacimiento
        
        con.grado_de_instruccion = valido['grado_de_instruccion'] \
        if 'grado_de_instruccion' in valido \
        and con.grado_de_instruccion != valido['grado_de_instruccion'] \
        else con.grado_de_instruccion
        
        transaction.commit()
    except Invalid as e:
        error = e.msg
    except AttributeError as e:
        error = 'Consumidor no existe'
    finally:
        return error

def editar_producto(parametros, _id):
    from paris.formularios import CategoriaValida, FormularioEditarProducto
    error = None
    try:
        pro = DBSession.query(producto).filter_by(producto_id = _id).first()
        if 'fabricante' in parametros:
            valido = FormularioEditarProducto.to_python(parametros)
            """
            fecha_string = __formatear_fecha_para_mysql(
                str(valido['debut_en_el_mercado'])
            )
            """
            pro.fabricante = valido['fabricante'] \
            if pro.fabricante != valido['fabricante'] else pro.fabricante
            
            pro.modelo = valido['modelo'] \
            if pro.modelo != valido['modelo'] else pro.modelo
            
            pro.nombre = valido['nombre'] \
            if pro.nombre != valido['nombre'] else pro.nombre
            
            pro.debut_en_el_mercado = valido['debut_en_el_mercado'] \
            if pro.debut_en_el_mercado != valido['debut_en_el_mercado'] \
            else pro.debut_en_el_mercado
            
            pro.largo = valido['largo'] \
            if pro.largo != valido['largo'] else pro.largo
            
            pro.ancho = valido['ancho'] \
            if pro.ancho != valido['ancho'] else pro.ancho
            
            pro.alto = valido['alto'] \
            if pro.alto != valido['alto'] else pro.alto
            
            pro.peso = valido['peso'] \
            if pro.peso != valido['peso'] else pro.peso
            
            pro.pais_de_origen = valido['pais_de_origen'] \
            if pro.pais_de_origen != valido['pais_de_origen'] \
            else pro.pais_de_origen
            
            transaction.commit()
        elif 'categoria' in parametros:
            valido = CategoriaValida.to_python(parametros['categoria'])
            pro.categoria = valido if pro.categoria != valido else pro.categoria 
            transaction.commit()
        elif 'descripcion' in parametros:
            error = editar_descripcion(
                {'contenido': parametros['descripcion']}, 
                parametros['descripcion_id']
            )
    except Invalid as e:
        error = e.msg
    except AttributeError as e:
        error = 'Consumidor no existe'
    finally:
        return error

def editar_descripcion(parametros, _id):
    from paris.formularios import TextoValido
    error = None
    try:
        valido = TextoValido.to_python(parametros['contenido'])
        des = DBSession.query(descripcion).\
        filter_by(descripcion_id = _id).first()
        
        des.contenido = valido if des.contenido != valido else des.contenido
        transaction.commit()
    except Invalid as e:
        error = e.msg
    except AttributeError as e:
        error = 'Descripcion no existe'
    finally:
        return error
    
def editar_tienda(parametros, _id):
    from paris.formularios import CategoriaValida, FormularioEditarDireccion
    
    tie = DBSession.query(cliente).\
    join(tienda).\
    filter(tienda.tienda_id == _id).first()
    error = None
    
    try:
        if 'calle' in parametros:
            # Editamos direccion
            valido = FormularioEditarDireccion.to_python(parametros)
            tie.edificio_cc = valido['edificio'] \
            if tie.edificio_cc != valido['edificio'] else tie.edificio_cc
            
            tie.piso = valido['piso'] \
            if tie.piso != valido['piso'] else tie.piso
            
            tie.apartamento = valido['apartamento'] \
            if tie.apartamento != valido['apartamento'] else tie.apartamento
            
            tie.local_no = valido['local_no'] \
            if tie.local_no != valido['local_no'] else tie.local_no
            
            tie.casa = valido['casa'] \
            if tie.casa != valido['casa'] else tie.casa
            
            tie.calle = valido['calle'] \
            if tie.calle != valido['calle'] else tie.calle
            
            tie.sector_urb_barrio = valido['urbanizacion'] \
            if tie.sector_urb_barrio != valido['urbanizacion'] \
            else tie.sector_urb_barrio
            
            tie.ubicacion = valido['ubicacion'] \
            if tie.ubicacion != valido['ubicacion'] else tie.ubicacion
             
            transaction.commit()
        elif 'categoria' in parametros:
            # Editamos categoria
            valido = CategoriaValida.to_python(parametros['categoria'])
            tie.categoria = valido if tie.categoria != valido else tie.categoria 
            transaction.commit()
        elif 'descripcion' in parametros:
            # Editamos descripcion
            error = editar_descripcion(
                {'contenido': parametros['descripcion']}, 
                parametros['descripcion_id']
            )
        elif 'Lunes' in parametros:
            # Editamos horario
            error = crear_horarios_y_turnos(parametros, _id)    
    except Invalid as e:
        error = e.msg
    except AttributeError as e:
        error = 'Tienda no existe'
    finally:
        return error

def editar_horario_de_trabajo(parametros, _id):
    from paris.formularios import FormularioEditarHorarioDeTrabajo
    error = None
    try:
        valido = FormularioEditarHorarioDeTrabajo.to_python(parametros)
        laborable = True if valido['laborable'] == 'Abierto' else False
        
        hdt = DBSession.query(horario_de_trabajo).\
        filter(and_(
            horario_de_trabajo.tienda_id == _id['tienda_id'],
            horario_de_trabajo.dia == _id['dia']
        )).first()
        
        hdt.laborable = laborable \
        if hdt.laborable != laborable else hdt.laborable
         
        transaction.commit()
    except Invalid as e:
        error = e.msg
    except AttributeError as e:
        error = 'Horario de trabajo no existe'
    finally:
        return error
        
def editar_patrocinante(parametros, _id):
    error = None        
    try:
        pat = DBSession.query(cliente).\
        join(patrocinante).\
        filter(patrocinante.patrocinante_id == _id).first()
    except Invalid as e:
        error = e.msg
    except AttributeError as e:
        error = 'Patrocinante no existe'
    finally:
        return error