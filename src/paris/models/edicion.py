# -*- coding: utf-8 -*-
'''
Created on 20/07/2012

@author: nestor
'''

from datetime import time
from paris.formatos import formatear_fecha_para_mysql
from paris.formularios import (
    FormularioCrearUsuario,
    FormularioCrearTienda,
    FormularioCrearConsumidor,
    FormularioEditarTurno,
    FormularioEditarUsuario,
    FormularioEditarConsumidor,
    FormularioEditarProducto,
    FormularioEditarDireccion,
    FormularioEditarHorarioDeTrabajo,
    TextoValido,
    CategoriaValida
)
from paris.models.constantes import ROOT
from spuria.orm import (
    DBSession,
    Usuario,
    Tienda,
    Patrocinante,
    HorarioDeTrabajo,
    Turno,
    Dia,
    Consumidor,
    Producto,
    Patrocinante,
    Descripcion,
    Cliente,
    Territorio,
    Categoria
)
from sqlalchemy import and_
import bcrypt

def crear_usuario(parametros):
    valido = FormularioCrearUsuario.to_python(parametros)
    
    ubicacion = DBSession.query(Territorio).filter_by(
        territorio_id = valido['ubicacion']
    ).first()
    
    usuario = Usuario(
        creador=ROOT, nombre=valido['nombre'], apellido=valido['apellido'], 
        estatus='Activo', ubicacion=ubicacion, 
        correo_electronico=valido['correo_electronico'], 
        contrasena=bcrypt.hashpw(valido['contrasena'], bcrypt.gensalt())
    )
    
    DBSession.add(usuario)
    return usuario

def crear_tienda(parametros, propietario):
    valido = FormularioCrearTienda.to_python(parametros)
    
    categoria = DBSession.query(Categoria).filter_by(
        categoria_id = valido['categoria']
    ).first()
    ubicacion = DBSession.query(Territorio).filter_by(
        territorio_id = valido['ubicacion']
    ).first()
    
    tienda = Tienda(
        ubicacion=ubicacion, rif=valido['rif'].replace('-',''),
        propietario=propietario, categoria=categoria, estatus='Activo',
        nombre_legal=valido['nombre_legal'],
        nombre_comun=valido['nombre_comun'], 
        telefono=valido['telefono'].replace('-',''),
        edificio_cc = valido['edificio'], piso = valido['piso'],
        apartamento = valido['apartamento'], local = valido['local_no'],
        casa = valido['casa'], calle = valido['calle'],
        sector_urb_barrio = valido['urbanizacion'], 
        pagina_web = valido['pagina_web'], 
        facebook = valido['facebook'],
        twitter = valido['twitter'],
        correo_electronico_publico = valido['correo_electronico_publico']
    )
    
    DBSession.add(tienda)
    return tienda

def crear_consumidor(parametros):
    valido = FormularioCrearConsumidor.to_python(parametros)
    
    ubicacion = DBSession.query(Territorio).filter_by(
        territorio_id = valido['ubicacion']
    ).first()
    fecha_string = formatear_fecha_para_mysql(
        str(valido['fecha_de_nacimiento'])
    )
    
    consumidor = Consumidor(
        creador=ROOT, nombre=valido['nombre'], apellido=valido['apellido'], 
        estatus='Activo', sexo=valido['sexo'], fecha_de_nacimiento=fecha_string,
        ubicacion=ubicacion, correo_electronico=valido['correo_electronico'],
        grupo_de_edad='Adultos jovenes',
        grado_de_instruccion=valido['grado_de_instruccion'],
        contrasena=bcrypt.hashpw(valido['contrasena'], bcrypt.gensalt())
    )
    
    DBSession.add(consumidor)
    return consumidor

    """
    Como yo llamo a las funciones de spuria con SELECT, SQLAlchemy automaticamente 
    hace un ROLLBACK de todo lo que hizo el SELECT ya que esa instruccion no deberia
    generar ningun cambio en la base de datos. 
    
    Para anular este comportamiento, hay que encapsular la transaccion entre las 
    instrucciones connection.begin() y connection.commit(). Lee:            
    http://stackoverflow.com/questions/7559570/make-sqlalchemy-commit-instead-of-rollback-after-a-select-query
    """

def crear_horario_de_trabajo(parametros, tienda, dia):
    valido = FormularioEditarHorarioDeTrabajo.to_python(parametros)
    laborable = {
        'Abierto': True,
        'Cerrado': False
    }[valido['laborable']]
    
    tienda.horarios_de_trabajo.append(HorarioDeTrabajo(dia, laborable))
    
    return tienda.horarios_de_trabajo[-1]

def crear_turno(parametros, horario_de_trabajo):
    valido = FormularioEditarTurno.to_python(parametros)
    ha = valido['hora_de_apertura']
    hc = valido['hora_de_cierre']
    
    horario_de_trabajo.turnos.append(Turno(
        time(ha[0], ha[1], ha[2]), time(hc[0], hc[1], hc[2])
    ))
    
    return horario_de_trabajo.turnos[-1]

def crear_descripcion(parametros, creador, describible):
    valido = TextoValido.to_python(parametros['contenido'])
    descripcion = Descripcion(
        describible=describible, contenido=valido, 
        creador=creador.rastreable.rastreable_id
    )
    
    DBSession.add(descripcion)
    return descripcion
    
def editar_usuario(parametros, usuario):
    valido = FormularioEditarUsuario.to_python(parametros)
    
    usuario.nombre = valido['nombre'] \
    if usuario.nombre != valido['nombre'] \
    else usuario.nombre

    usuario.apellido = valido['apellido'] \
    if usuario.apellido != valido['apellido'] \
    else usuario.apellido
    
    usuario.ubicacion_id = valido['ubicacion'] \
    if usuario.ubicacion_id != valido['ubicacion'] \
    else usuario.ubicacion_id

    """
    Aqui hay una buena explicacion de por que tengo que hacer 
    transaction.commit() y no DBSession.commit() 
    http://turbogears.org/2.0/docs/main/Wiki20/wiki20.html#initializing-the-tables

    transaction.commit()
    """
    
    # Si ya hay un consumidor asociado a este usuario lo editamos, sino, 
    # lo creamos
    if 'sexo' in parametros \
    or 'fecha_de_nacimiento' in parametros \
    or 'grado_de_instruccion' in parametros:
        editar_consumidor(parametros, usuario)
        
    return usuario

def editar_consumidor(parametros, consumidor):
    valido = FormularioEditarConsumidor.to_python(parametros)
    
    if 'fecha_de_nacimiento' in valido and \
    valido['fecha_de_nacimiento'] is not None:
        fecha_string = \
        formatear_fecha_para_mysql(str(valido['fecha_de_nacimiento']))
    else:
        fecha_string = None

    consumidor.sexo = valido['sexo'] \
    if 'sexo' in valido and consumidor.sexo != valido['sexo'] \
    and valido['sexo'] is not None \
    else consumidor.sexo
    
    consumidor.fecha_de_nacimiento = fecha_string \
    if fecha_string is not None \
    and consumidor.fecha_de_nacimiento != fecha_string \
    else consumidor.fecha_de_nacimiento
    
    consumidor.grado_de_instruccion = valido['grado_de_instruccion'] \
    if 'grado_de_instruccion' in valido \
    and consumidor.grado_de_instruccion != valido['grado_de_instruccion'] \
    and valido['grado_de_instruccion'] is not None \
    else consumidor.grado_de_instruccion
    
    return consumidor

def editar_producto(parametros, producto):
    if 'fabricante' in parametros:
        valido = FormularioEditarProducto.to_python(parametros)
        """
        fecha_string = formatear_fecha_para_mysql(
            str(valido['debut_en_el_mercado'])
        )
        """
        producto.fabricante = valido['fabricante'] \
        if producto.fabricante != valido['fabricante'] else producto.fabricante
        
        producto.modelo = valido['modelo'] \
        if producto.modelo != valido['modelo'] else producto.modelo
        
        producto.nombre = valido['nombre'] \
        if producto.nombre != valido['nombre'] else producto.nombre
        
        producto.debut_en_el_mercado = valido['debut_en_el_mercado'] \
        if producto.debut_en_el_mercado != valido['debut_en_el_mercado'] \
        else producto.debut_en_el_mercado
        
        producto.largo = valido['largo'] \
        if producto.largo != valido['largo'] else producto.largo
        
        producto.ancho = valido['ancho'] \
        if producto.ancho != valido['ancho'] else producto.ancho
        
        producto.alto = valido['alto'] \
        if producto.alto != valido['alto'] else producto.alto
        
        producto.peso = valido['peso'] \
        if producto.peso != valido['peso'] else producto.peso
        
        producto.pais_de_origen_id = valido['pais_de_origen'] \
        if producto.pais_de_origen_id != valido['pais_de_origen'] \
        else producto.pais_de_origen_id
    elif 'categoria' in parametros:
        valido = CategoriaValida.to_python(parametros['categoria'])
        producto.categoria_id = valido \
        if producto.categoria_id != valido \
        else producto.categoria_id
    elif 'descripcion' in parametros:
        descripcion = DBSession.query(Descripcion).filter_by(
            descripcion_id = parametros['descripcion_id']
        ).first()
        editar_descripcion(
            {'contenido': parametros['descripcion']}, descripcion
        )
        
    return producto

def editar_descripcion(parametros, descripcion):
    valido = TextoValido.to_python(parametros['contenido'])
    
    descripcion.contenido = valido \
    if descripcion.contenido != valido \
    else descripcion.contenido
    
    return descripcion
    
def editar_tienda(parametros, tienda):
    if 'calle' in parametros:
        # Editamos direccion
        valido = FormularioEditarDireccion.to_python(parametros)
        tienda.edificio_cc = valido['edificio'] \
        if tienda.edificio_cc != valido['edificio'] else tienda.edificio_cc
        
        tienda.piso = valido['piso'] \
        if tienda.piso != valido['piso'] else tienda.piso
        
        tienda.apartamento = valido['apartamento'] \
        if tienda.apartamento != valido['apartamento'] else tienda.apartamento
        
        tienda.local_no = valido['local_no'] \
        if tienda.local_no != valido['local_no'] else tienda.local_no
        
        tienda.casa = valido['casa'] \
        if tienda.casa != valido['casa'] else tienda.casa
        
        tienda.calle = valido['calle'] \
        if tienda.calle != valido['calle'] else tienda.calle
        
        tienda.sector_urb_barrio = valido['urbanizacion'] \
        if tienda.sector_urb_barrio != valido['urbanizacion'] \
        else tienda.sector_urb_barrio
        
        tienda.ubicacion_id = valido['ubicacion'] \
        if tienda.ubicacion_id != valido['ubicacion'] else tienda.ubicacion_id
    elif 'categoria' in parametros:
        # Editamos categoria
        valido = CategoriaValida.to_python(parametros['categoria'])
        tienda.categoria_id = valido if tienda.categoria_id != valido \
        else tienda.categoria_id
    elif 'descripcion' in parametros:
        # Editamos descripcion
        descripcion = DBSession.query(Descripcion).filter_by(
            descripcion_id = parametros['descripcion_id']
        ).first()
        editar_descripcion(
            {'contenido': parametros['descripcion']}, descripcion
        )
    elif 'Lunes' in parametros:
        # Editamos horario
        editar_horarios_y_turnos(parametros, tienda)
        
    return tienda

def editar_horarios_y_turnos(parametros, tienda):
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
    
    claves = parametros.keys()
    dias = [x.valor for x in DBSession.query(Dia).all()]
    
    # Procesamos cada dia de la semana
    for dia in dias:
        hdt = DBSession.query(HorarioDeTrabajo).\
        filter(and_(
            HorarioDeTrabajo.tienda_id == tienda.tienda_id,
            HorarioDeTrabajo.dia == dia
        )).first()
        
        laborable = {'laborable': parametros[dia]}
        
        # Si la tienda no tiene un HorarioDeTrabajo para ese dia, se
        # crea uno. De lo contrario se edita el que ya existe
        hdt = crear_horario_de_trabajo(laborable, tienda, dia) \
        if hdt is None \
        else editar_horario_de_trabajo(laborable, hdt)

        # El formato del dia es '<Dia>.' Ej: 'Lunes.', 'Martes.', etc    
        formato_del_dia = '{}.'.format(dia)
        # Estas son las claves de cada dia. De la forma:
        # ['Lunes.hora_de_apertura.0', 'Lunes.hora_de_apertura.1', ...]
        claves_del_dia = [x for x in claves if formato_del_dia in x]
        # En turnos esta el indice mas alto de las claves del dia.
        # En el ejemplo anterior seria 1
        turnos = max([int(x.split('.')[2]) for x in claves_del_dia])
        turnos = turnos + 1

        # Agregamos o quitamos turnos del horario_de_trabajo para igualar
        # la cantidad de turnos proporcionadas por el cliente
        while(len(hdt.turnos) != (turnos)):
            if len(hdt.turnos) > (turnos):
                DBSession.delete(hdt.turnos[-1])
            elif len(hdt.turnos) < (turnos):
                hdt.turnos.append(Turno(time(0), time(0)))

        # Editamos los turnos con la informacion que pasa el cliente
        for i, turno in enumerate(hdt.turnos):
            horas = {
                'Abierto': {
                    'hora_de_apertura': parametros['{}.hora_de_apertura.{}'.\
                    format(dia, i)],
                    'hora_de_cierre': parametros['{}.hora_de_cierre.{}'.\
                    format(dia, i)]
                },
                'Cerrado': {
                    'hora_de_apertura': '00:00:00', 
                    'hora_de_cierre': '00:00:00'
                }
            }[parametros[dia]]
            
            editar_turno(horas, turno)

def editar_horario_de_trabajo(parametros, horario_de_trabajo):
    valido = FormularioEditarHorarioDeTrabajo.to_python(parametros)
    laborable = {
        'Abierto': True,
        'Cerrado': False
    }[valido['laborable']]

    horario_de_trabajo.laborable = laborable \
    if horario_de_trabajo.laborable != laborable \
    else horario_de_trabajo.laborable

    return horario_de_trabajo
    
def editar_turno(parametros, turno):
    valido = FormularioEditarTurno.to_python(parametros)
    ha = valido['hora_de_apertura']
    hc = valido['hora_de_cierre']
    ha = time(ha[0], ha[1], ha[2])
    hc = time(hc[0], hc[1], hc[2])
    
    turno.hora_de_apertura = ha \
    if turno.hora_de_apertura != ha \
    else turno.hora_de_apertura
    
    turno.hora_de_cierre = hc \
    if turno.hora_de_cierre != hc \
    else turno.hora_de_cierre

    return turno

def editar_patrocinante(parametros, patrocinante):
    pass