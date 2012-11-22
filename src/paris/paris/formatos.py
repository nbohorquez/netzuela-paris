# -*- coding: utf-8 -*-
'''
Created on 21/11/2012

@author: nestor
'''

from datetime import datetime
from models.constantes import ACCIONES, COLUMNAS_NO_VISIBLES
from spuria.orm import (
    Acceso,
    Accion,
    Busqueda,
    Calificacion,
    CalificacionResena,
    Categoria,
    Cliente,
    CodigoDeError,
    Consumidor,
    Croquis,
    DBSession,
    Describible,
    Descripcion,
    Dia,
    Estadisticas,
    Estatus,
    Factura,
    Foto,
    GradoDeInstruccion,
    GrupoDeEdad,
    Idioma,
    Inventario,
    Mensaje,
    Patrocinante,
    Privilegios,
    Producto,
    Publicidad,
    Rastreable,
    Seguimiento,
    Territorio,
    Tienda,
    TipoDeCodigo,
    Usuario,
)
from spuria.orm.descripciones_fotos import DescribibleAsociacion
from time import strftime, strptime
import cPickle

def obtener_columnas_pk(objeto):
    # Tomado de: 
    #http://stackoverflow.com/questions/9398664/given-a-declarative-sqlalchemy-class-how-can-i-programmatically-retrieve-a-list
    from sqlalchemy.orm.attributes import InstrumentedAttribute
    import inspect
    
    predicado = lambda x: isinstance(x, InstrumentedAttribute)
    fields = inspect.getmembers(objeto, predicate=predicado)
    columnas = [vars(y.property.columns[0]) for x,y in fields]
    claves_primarias = [x['name'] for x in columnas if x['primary_key']]
    return claves_primarias
    
def formatear_fecha_para_mysql(fecha):
    fecha_neutra = strptime(fecha, '%d/%m/%Y')
    return strftime('%Y-%m-%d', fecha_neutra)
    
def formatear_fecha_para_paris(fecha):
    fecha_neutra = strptime(fecha, '%Y-%m-%d')
    return strftime('%d/%m/%Y', fecha_neutra)

def formatear_comentarios(comentarios):
    resultado = []
    for comentario in comentarios:
        tmp = {}
        tmp['calificacion'] = comentario.calificacion
        tmp['resena'] = comentario.resena

        fecha = str(comentario.rastreable.fecha_de_creacion)
        tmp['fecha'] = "{0}/{1}/{2} {3}:{4}".format(
            fecha[6:8], fecha[4:6], fecha[0:4], fecha[8:10], fecha[10:12]
        )

        tmp['consumidor'] = DBSession.query(Consumidor).\
        filter_by(consumidor_id = comentario.consumidor_id).first()

        resultado.append(tmp)
    return resultado

def formatear_entrada_noticias(reg, peticion, demandante):
    def formatear_objeto(objeto, mostrar_href):
        return {
            'tienda': lambda x, y: reg_tienda(x, y),
            'patrocinante': lambda x, y: reg_patrocinante(x, y),
            'administrador': lambda x, y: reg_usuario(x, y),
            'consumidor': lambda x, y: reg_usuario(x, y),
            'usuario': lambda x, y: reg_usuario(x, y),
            'inventario': lambda x, y: reg_inventario(x, y),
            'croquis': lambda x, y: reg_croquis(x, y),
            'producto': lambda x, y: reg_producto(x, y),
            'mensaje': lambda x, y: reg_mensaje(x, y),
            'busqueda': lambda x, y: reg_busqueda(x, y),
            'calificacion_resena': lambda x, y: reg_calificacion_resena(x, y),
            'seguimiento': lambda x, y: reg_seguimiento(x, y),
            'descripcion': lambda x, y: reg_descripcion(x, y),
            'publicidad': lambda x, y: reg_publicidad(x, y),
            'estadisticas': lambda x, y: reg_estadisticas(x, y),
            'factura': lambda x, y: reg_factura(x, y)
        }[objeto.__tablename__](objeto, mostrar_href)
    def reg_tienda(tienda, muestro_href):
        valor = {}
        valor['nombre'] = tienda.nombre_comun
        valor['titulo'] = tienda.nombre_legal
        
        valor['foto'] = DBSession.query(Foto.ruta_de_foto).\
        join(Describible).\
        join(DescribibleAsociacion).\
        join(Tienda).\
        filter(Tienda.tienda_id == tienda.tienda_id)
        
        valor['href'] = peticion.route_url(
            'tienda', tienda_id = tienda.tienda_id
        ) if muestro_href else None

        valor['diccionario'] = {
            'Nombre legal': tienda.nombre_legal,
            'Nombre comun': tienda.nombre_comun,
            'RIF': tienda.rif,
            'Estatus': tienda.estatus,
            'Propietario': tienda.propietario.nombre \
                           + tienda.propietario.apellido,
            'Categoria': tienda.categoria.nombre,
            'Telefono': tienda.telefono,
            'Ubicacion': tienda.ubicacion.nombre
        }

        return valor
    def reg_patrocinante(patrocinante, muestro_href):
        valor = {}
        valor['nombre'] = patrocinante.nombre_comun
        valor['titulo'] = patrocinante.nombre_legal
        
        valor['foto'] = DBSession.query(Foto.ruta_de_foto).\
        join(Describible).\
        join(DescribibleAsociacion).\
        join(Patrocinante).\
        filter(Patrocinante.patrocinante_id == patrocinante.patrocinante_id)

        valor['href'] = peticion.route_url(
            'patrocinante', patrocinante_id = patrocinante.patrocinante_id
        ) if muestro_href else None

        valor['diccionario'] = {
            'Nombre legal': patrocinante.nombre_legal,
            'Nombre comun': patrocinante.nombre_comun,
            'RIF': patrocinante.rif,
            'Estatus': patrocinante.estatus,
            'Propietario': patrocinante.propietario.nombre \
                           + patrocinante.propietario.apellido,
            'Categoria': patrocinante.categoria.nombre,
            'Telefono': patrocinante.telefono,
            'Ubicacion': patrocinante.ubicacion.nombre
        }

        return valor
    def reg_usuario(usuario, muestro_href):
        valor = {}
        valor['nombre'] = valor['titulo'] = "{0} {1}".format(
            usuario.nombre, usuario.apellido
        )
        valor['foto'] = DBSession.query(Foto.ruta_de_foto).\
        join(Describible).\
        join(DescribibleAsociacion).\
        join(Usuario).\
        filter(Usuario.usuario_id == usuario.usuario_id)
        
        valor['href'] = peticion.route_url(
            'usuario', usuario_id = usuario.usuario_id
        ) if muestro_href else None
        
        valor['diccionario'] = {
            'Nombre': valor['nombre'],
            'Estatus': usuario.estatus,
            'Ubicacion': usuario.ubicacion.nombre \
                         if usuario.ubicacion != None else None
        }
        return valor
    def reg_inventario(inventario, muestro_href):
        valor = {}
        valor['titulo'] = valor['nombre'] = inventario.descripcion
        valor['foto'] = DBSession.query(Foto.ruta_de_foto).\
        join(Describible).\
        join(DescribibleAsociacion).\
        join(Producto).\
        filter(Producto.producto_id == inventario.producto_id)
        
        valor['href'] = peticion.route_url(
            'producto', producto_id = inventario.producto_id
        ) if muestro_href else None
        valor['diccionario'] = {
            'Descripcion': valor['nombre'],
            'SKU': inventario.codigo
        }
        if inventario.producto != None:
            valor['diccionario'][inventario.producto.tipo_de_codigo] = \
            inventario.producto.codigo
        return valor
    def reg_croquis(croquis, muestro_href):
        valor = {}
        valor['titulo'] = valor['nombre'] = 'croquis'
        valor['href'] = '#' if muestro_href else None
        valor['diccionario'] = {
            'punto ' + str(i):'Lat: {}, Lng: {}'.format(
                punto.latitud, punto.longitud
            ) for (i, punto) in enumerate(croquis.puntos)
        }
        return valor
    def reg_producto(producto, muestro_href):
        valor = {}
        valor['foto'] = DBSession.query(Foto.ruta_de_foto).\
        join(Describible).\
        join(DescribibleAsociacion).\
        join(Producto).\
        filter(Producto.producto_id == producto.producto_id)
        valor['nombre'] = valor['titulo'] = "{0} {1}".format(
            producto.fabricante, producto.nombre
        )
        valor['href'] = peticion.route_url(
            'producto', producto_id = producto.producto_id
        ) if muestro_href else None
            
        valor['diccionario'] = {}
        return valor
    def reg_mensaje(mensaje, muestro_href):
        valor = {}
        valor['nombre'] = valor['titulo'] = 'mensaje'
        valor['href'] = '#' if muestro_href else None
        valor['diccionario'] = { 'contenido': mensaje.contenido }
        return valor
    def reg_busqueda(busqueda, muestro_href):
        valor = {}
        valor['nombre'] = valor['titulo'] = 'busqueda'
        valor['href'] = '#' if muestro_href else None
        valor['diccionario'] = { 'contenido': busqueda.contenido}
        return valor
    def reg_calificacion_resena(calificacion_resena, muestro_href):
        valor = {}
        valor['nombre'] = valor['titulo'] = 'comentario'
        valor['href'] = '#' if muestro_href else None
        valor['diccionario'] = {
            'calificacion': calificacion_resena.calificacion,
            'resena': calificacion_resena.resena
        }
        return valor
    def reg_seguimiento(seguimiento, muestro_href):
        valor = {}
        valor['nombre'] = valor['titulo'] = 'seguimiento'
        valor['href'] = '#' if muestro_href else None
        valor['diccionario'] = {}
        return valor
    def reg_descripcion(descripcion, muestro_href):
        valor = {}
        valor['nombre'] = 'descripcion'
        padre = descripcion.describible.padre
        valor['titulo'] = {
            'producto': lambda x: x.fabricante + ' ' + x.nombre,
            'tienda': lambda x: x.nombre_legal,
            'patrocinante': lambda x: x.nombre_legal,
            'usuario': lambda x: x.nombre + ' ' + x.apellido,
            'publicidad': lambda x: x.nombre
        }[padre.__tablename__](padre)
        valor['href'] = '#' if muestro_href else None
        valor['diccionario'] = { 'contenido':descripcion.contenido }
        return valor
    def reg_publicidad(publicidad, muestro_href):
        valor = {}
        valor['nombre'] = 'publicidad'
        valor['titulo'] = publicidad.nombre
        valor['href'] = '#' if muestro_href else None
        valor['diccionario'] = {}
        return valor
    def reg_estadisticas(estadisticas, muestro_href):
        valor = {}
        valor['nombre'] = valor['titulo'] = 'estadisticas'
        valor['href'] = '#' if muestro_href else None
        valor['diccionario'] = {}
        return valor
    def reg_factura(factura, muestro_href):
        valor = {}
        valor['nombre'] = valor['titulo'] = 'factura'
        valor['href'] = '#' if muestro_href else None
        valor['diccionario'] = {}
        return valor
    def depurar_columnas_registro(diccionario):
        return dict((entrada[0].replace('_', ' '), entrada[1]) \
        for entrada in diccionario.items() \
        if entrada[0] not in COLUMNAS_NO_VISIBLES)
    def pulir_columnas_registro(diccionario):
        return dict((entrada[0].capitalize(), entrada[1]) \
        for entrada in diccionario.items())
    
    por_defecto = {}
    por_defecto['nombre'] = por_defecto['titulo'] = ''
    por_defecto['href'] = None
    por_defecto['diccionario'] = {}
    
    actor_activo = reg.actor_activo.padre
    pk_activo = obtener_columnas_pk(actor_activo)
    pk_demandante = obtener_columnas_pk(demandante)
    
    id_activo = { col:getattr(actor_activo, col) for col in pk_activo }
    id_demandante = { col:getattr(demandante, col) for col in pk_demandante }
    
    try:
        actor_pasivo = reg.actor_pasivo.padre
        pk_pasivo = obtener_columnas_pk(actor_pasivo)
        id_pasivo = { col:getattr(actor_pasivo, col) for col in pk_pasivo }
    except Exception:
        actor_pasivo = None
        id_pasivo = 0

    activo = formatear_objeto(
        actor_activo, not (\
            actor_activo.__tablename__ == demandante.__tablename__ \
            and id_activo == id_demandante
        )
    ) if (actor_activo is not None) else por_defecto

    pasivo = formatear_objeto(
        actor_pasivo, not (\
            actor_pasivo.__tablename__ == demandante.__tablename__ \
            and id_pasivo == id_demandante
        )
    ) if (actor_pasivo is not None) else por_defecto
    
    if 'foto' in activo:
        tmp = activo['foto'].filter(Foto.ruta_de_foto.like('%miniaturas%')).\
        first()
        activo['foto'] = tmp[0] if (tmp is not None) else ''
    else:
        activo['foto'] = ''
        
    if 'foto' in pasivo:
        tmp = pasivo['foto'].filter(
            Foto.ruta_de_foto.like('%miniaturas%')
        ).first()
        pasivo['foto'] = tmp[0] if (tmp is not None) else ''
    else:
        pasivo['foto'] = ''
    
    entrada = {}
    entrada['actor_activo'] = activo
    entrada['actor_pasivo'] = pasivo
    entrada['accion'] = ACCIONES[reg.accion]
    entrada['info'] = activo \
    if demandante.__tablename__ != actor_activo.__tablename__ \
    else pasivo

    diccionario = cPickle.loads(reg.detalles) \
    if reg.detalles is not None \
    else {}
    
    diccionario_depurado = depurar_columnas_registro(diccionario)
    entrada['parametros'] = diccionario_depurado \
    if (entrada['accion'] == 'actualizo') \
    else {}

    fecha = str(reg.fecha_hora)
    ano = int(fecha[0:4])
    mes = int(fecha[4:6])
    dia = int(fecha[6:8])
    hora = int(fecha[8:10])
    minu = int(fecha[10:12])
    seg = int(fecha[12:14])
    mseg = int(fecha[15:18])
    entonces = datetime(ano, mes, dia, hora, minu, seg, mseg * 1000)
    ahora = datetime.now()
    diferencia = ahora - entonces
    
    if diferencia.days > 0:
        entrada['tiempo'] = "{0} dia(s)".format(str(diferencia.days))
    else:
        if diferencia.seconds > 3600:
            entrada['tiempo'] = "{0} hora(s)".format(
                str(diferencia.seconds/3600)
            )
        elif diferencia.seconds < 3600 and diferencia.seconds > 60:
            entrada['tiempo'] = "{0} minuto(s)".format(
                str(diferencia.seconds/60)
            )
        else:
            entrada['tiempo'] = "{0} segundo(s)".format(str(diferencia.seconds))

    return entrada