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

def formatear_comentarios(comentario):
    tmp = {}
    tmp['calificacion'] = comentario.calificacion
    tmp['resena'] = comentario.resena

    fecha = str(comentario.rastreable.fecha_de_creacion)
    tmp['fecha'] = "{0}/{1}/{2} {3}:{4}".format(
        fecha[6:8], fecha[4:6], fecha[0:4], fecha[8:10], fecha[10:12]
    )

    tmp['consumidor'] = DBSession.query(Consumidor).\
    filter_by(consumidor_id = comentario.consumidor_id).first()

    return tmp

def formatear_objeto_noticia(objeto, mostrar_href, peticion):
    def ntc_tienda(tienda, muestro_href):
        valor = {}
        valor['tipo'] = 'tienda'
        valor['id'] = tienda.tienda_id
        valor['nombre'] = tienda.nombre_comun
        
        valor['foto'] = DBSession.query(Foto.ruta_de_foto).\
        join(Describible).\
        join(DescribibleAsociacion).\
        join(Tienda).\
        filter(Tienda.tienda_id == tienda.tienda_id)
        
        valor['href'] = peticion.route_url(
            'tienda', tienda_id = tienda.tienda_id
        ) if muestro_href else None
        
        return valor
    def ntc_patrocinante(patrocinante, muestro_href):
        valor = {}
        valor['tipo'] = 'patrocinante'
        valor['id'] = patrocinante.patrocinante_id
        valor['nombre'] = patrocinante.nombre_comun
        
        valor['foto'] = DBSession.query(Foto.ruta_de_foto).\
        join(Describible).\
        join(DescribibleAsociacion).\
        join(Patrocinante).\
        filter(Patrocinante.patrocinante_id == patrocinante.patrocinante_id)
        
        valor['href'] = peticion.route_url(
            'patrocinante', patrocinante_id = patrocinante.patrocinante_id
        ) if muestro_href else None
        
        return valor
    def ntc_usuario(usuario, muestro_href):
        valor = {}
        valor['tipo'] = 'usuario'
        valor['id'] = usuario.usuario_id
        valor['nombre'] = "{0} {1}".format(
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
        
        return valor
    def ntc_inventario(inventario, muestro_href):
        valor = {}
        valor['tipo'] = 'inventario'
        valor['id'] = '{}:{}'.format(inventario.tienda_id, inventario.codigo) 
        valor['nombre'] = inventario.descripcion
        valor['foto'] = DBSession.query(Foto.ruta_de_foto).\
        join(Describible).\
        join(DescribibleAsociacion).\
        join(Producto).\
        filter(Producto.producto_id == inventario.producto_id)
        
        valor['href'] = peticion.route_url(
            'producto', producto_id = inventario.producto_id
        ) if muestro_href else None
        
        return valor
    def ntc_croquis(croquis, muestro_href):
        valor = {}
        valor['tipo'] = 'croquis'
        valor['id'] = croquis.croquis_id
        valor['nombre'] = 'croquis'
        valor['href'] = '#' if muestro_href else None
        return valor
    def ntc_producto(producto, muestro_href):
        valor = {}
        valor['tipo'] = 'producto'
        valor['id'] = producto.producto_id
        valor['nombre'] = "{0} {1}".format(
            producto.fabricante, producto.nombre
        )
        
        valor['foto'] = DBSession.query(Foto.ruta_de_foto).\
        join(Describible).\
        join(DescribibleAsociacion).\
        join(Producto).\
        filter(Producto.producto_id == producto.producto_id)
        
        valor['href'] = peticion.route_url(
            'producto', producto_id = producto.producto_id
        ) if muestro_href else None
        
        return valor
    def ntc_mensaje(mensaje, muestro_href):
        valor = {}
        valor['tipo'] = 'mensaje'
        valor['id'] = mensaje.mensaje_id
        valor['nombre'] = 'mensaje'
        valor['href'] = '#' if muestro_href else None
        return valor
    def ntc_busqueda(busqueda, muestro_href):
        valor = {}
        valor['tipo'] = 'busqueda'
        valor['id'] = busqueda.busqueda_id
        valor['nombre'] = 'busqueda'
        valor['href'] = '#' if muestro_href else None
        return valor
    def ntc_calificacion_resena(calificacion_resena, muestro_href):
        valor = {}
        valor['tipo'] = 'calificacion_resena'
        valor['id'] = '{}:{}'.format(
            calificacion_resena.calificable_seguible_id, 
            calificacion_resena.consumidor_id
        )
        valor['nombre'] = 'comentario'
        valor['href'] = '#' if muestro_href else None
        return valor
    def ntc_seguimiento(seguimiento, muestro_href):
        valor = {}
        valor['tipo'] = 'seguimiento'
        valor['id'] = '{}:{}'.format(
            seguimiento.calificable_seguible_id, 
            seguimiento.consumidor_id
        )
        valor['nombre'] = 'seguimiento'
        valor['href'] = '#' if muestro_href else None
        return valor
    def ntc_descripcion(descripcion, muestro_href):
        valor = {}
        valor['tipo'] = 'descripcion'
        valor['id'] = descripcion.descripcion_id
        valor['nombre'] = 'descripcion'
        valor['href'] = '#' if muestro_href else None
        return valor
    def ntc_publicidad(publicidad, muestro_href):
        valor = {}
        valor['tipo'] = 'publicidad'
        valor['id'] = publicidad.publicidad_id
        valor['nombre'] = 'publicidad'
        valor['href'] = '#' if muestro_href else None
        return valor
    def ntc_estadisticas(estadisticas, muestro_href):
        valor = {}
        valor['tipo'] = 'estadisticas'
        valor['id'] = estadisticas.estadisticas_id
        valor['nombre'] = 'estadisticas'
        valor['href'] = '#' if muestro_href else None
        return valor
    def ntc_factura(factura, muestro_href):
        valor = {}
        valor['tipo'] = 'factura'
        valor['id'] = factura.factura_id
        valor['nombre'] = 'factura'
        valor['href'] = '#' if muestro_href else None
        return valor
    
    return {
        'tienda': lambda x, y: ntc_tienda(x, y),
        'patrocinante': lambda x, y: ntc_patrocinante(x, y),
        'administrador': lambda x, y: ntc_usuario(x, y),
        'consumidor': lambda x, y: ntc_usuario(x, y),
        'usuario': lambda x, y: ntc_usuario(x, y),
        'inventario': lambda x, y: ntc_inventario(x, y),
        'croquis': lambda x, y: ntc_croquis(x, y),
        'producto': lambda x, y: ntc_producto(x, y),
        'mensaje': lambda x, y: ntc_mensaje(x, y),
        'busqueda': lambda x, y: ntc_busqueda(x, y),
        'calificacion_resena': lambda x, y: ntc_calificacion_resena(x, y),
        'seguimiento': lambda x, y: ntc_seguimiento(x, y),
        'descripcion': lambda x, y: ntc_descripcion(x, y),
        'publicidad': lambda x, y: ntc_publicidad(x, y),
        'estadisticas': lambda x, y: ntc_estadisticas(x, y),
        'factura': lambda x, y: ntc_factura(x, y)
    }[objeto.__tablename__](objeto, mostrar_href)
    
def formatear_objeto_teaser(objeto):
    def tea_tienda(tienda):
        valor = {}
        valor['titulo'] = tienda.nombre_legal
        
        valor['foto'] = DBSession.query(Foto.ruta_de_foto).\
        join(Describible).\
        join(DescribibleAsociacion).\
        join(Tienda).\
        filter(Tienda.tienda_id == tienda.tienda_id)
        
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
    def tea_patrocinante(patrocinante):
        valor = {}
        valor['titulo'] = patrocinante.nombre_legal
        
        valor['foto'] = DBSession.query(Foto.ruta_de_foto).\
        join(Describible).\
        join(DescribibleAsociacion).\
        join(Patrocinante).\
        filter(Patrocinante.patrocinante_id == patrocinante.patrocinante_id)
    
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
    def tea_usuario(usuario):
        valor = {}
        valor['titulo'] = "{0} {1}".format(
            usuario.nombre, usuario.apellido
        )
        
        valor['foto'] = DBSession.query(Foto.ruta_de_foto).\
        join(Describible).\
        join(DescribibleAsociacion).\
        join(Usuario).\
        filter(Usuario.usuario_id == usuario.usuario_id)
        
        valor['diccionario'] = {
            'Nombre': valor['nombre'],
            'Estatus': usuario.estatus,
            'Ubicacion': usuario.ubicacion.nombre \
                         if usuario.ubicacion != None else None
        }
        return valor
    def tea_inventario(inventario):
        valor = {}
        valor['titulo'] = inventario.descripcion
        valor['foto'] = DBSession.query(Foto.ruta_de_foto).\
        join(Describible).\
        join(DescribibleAsociacion).\
        join(Producto).\
        filter(Producto.producto_id == inventario.producto_id)
        
        valor['diccionario'] = {
            'Descripcion': valor['titulo'],
            'SKU': inventario.codigo,
            'Precio': str(inventario.precios_cantidades[-1].precio),
            'Cantidad': str(inventario.precios_cantidades[-1].cantidad)
        }
        return valor
    def tea_croquis(croquis):
        valor = {}
        valor['titulo'] = 'croquis'
        valor['diccionario'] = {
            'punto ' + str(i):'Lat: {}, Lng: {}'.format(
                punto.latitud, punto.longitud
            ) for (i, punto) in enumerate(croquis.puntos)
        }
        return valor
    def tea_producto(producto):
        valor = {}
        valor['titulo'] = "{0} {1}".format(
            producto.fabricante, producto.nombre
        )
        
        valor['foto'] = DBSession.query(Foto.ruta_de_foto).\
        join(Describible).\
        join(DescribibleAsociacion).\
        join(Producto).\
        filter(Producto.producto_id == producto.producto_id)
        
        valor['diccionario'] = {}
        return valor
    def tea_mensaje(mensaje):
        valor = {}
        valor['titulo'] = 'mensaje'
        valor['diccionario'] = { 'contenido': mensaje.contenido }
        return valor
    def tea_busqueda(busqueda):
        valor = {}
        valor['titulo'] = 'busqueda'
        valor['diccionario'] = { 'contenido': busqueda.contenido}
        return valor
    def tea_calificacion_resena(calificacion_resena):
        valor = {}
        valor['titulo'] = 'comentario'
        valor['diccionario'] = {
            'calificacion': calificacion_resena.calificacion,
            'resena': calificacion_resena.resena
        }
        return valor
    def tea_seguimiento(seguimiento):
        valor = {}
        valor['titulo'] = 'seguimiento'
        valor['diccionario'] = {}
        return valor
    def tea_descripcion(descripcion):
        valor = {}
        padre = descripcion.describible.padre
        valor['titulo'] = {
            'producto': lambda x: x.fabricante + ' ' + x.nombre,
            'tienda': lambda x: x.nombre_legal,
            'patrocinante': lambda x: x.nombre_legal,
            'usuario': lambda x: x.nombre + ' ' + x.apellido,
            'publicidad': lambda x: x.nombre
        }[padre.__tablename__](padre)
        valor['diccionario'] = { 'contenido':descripcion.contenido }
        return valor
    def tea_publicidad(publicidad):
        valor = {}
        valor['titulo'] = publicidad.nombre
        valor['diccionario'] = {}
        return valor
    def tea_estadisticas(estadisticas):
        valor = {}
        valor['titulo'] = 'estadisticas'
        valor['diccionario'] = {}
        return valor
    def tea_factura(factura):
        valor = {}
        valor['titulo'] = 'factura'
        valor['diccionario'] = {}
        return valor
    
    teaser = {
        'tienda': lambda x: tea_tienda(x),
        'patrocinante': lambda x: tea_patrocinante(x),
        'administrador': lambda x: tea_usuario(x),
        'consumidor': lambda x: tea_usuario(x),
        'usuario': lambda x: tea_usuario(x),
        'inventario': lambda x: tea_inventario(x),
        'croquis': lambda x: tea_croquis(x),
        'producto': lambda x: tea_producto(x),
        'mensaje': lambda x: tea_mensaje(x),
        'busqueda': lambda x: tea_busqueda(x),
        'calificacion_resena': lambda x: tea_calificacion_resena(x),
        'seguimiento': lambda x: tea_seguimiento(x),
        'descripcion': lambda x: tea_descripcion(x),
        'publicidad': lambda x: tea_publicidad(x),
        'estadisticas': lambda x: tea_estadisticas(x),
        'factura': lambda x: tea_factura(x)
    }[objeto.__tablename__](objeto)
    
    if 'foto' in teaser:
        tmp = teaser['foto'].filter(Foto.ruta_de_foto.like('%miniaturas%')).\
        first()
        teaser['foto'] = tmp[0] if (tmp is not None) else ''
    else:
        teaser['foto'] = ''
        
    return teaser

def formatear_entrada_noticias(reg, peticion, demandante):
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

    activo = formatear_objeto_noticia(
        actor_activo, not (\
            actor_activo.__tablename__ == demandante.__tablename__ \
            and id_activo == id_demandante
        ), peticion
    ) if (actor_activo is not None) else por_defecto

    pasivo = formatear_objeto_noticia(
        actor_pasivo, not (\
            actor_pasivo.__tablename__ == demandante.__tablename__ \
            and id_pasivo == id_demandante
        ), peticion
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
    """
    entrada['info'] = activo \
    if demandante.__tablename__ != actor_activo.__tablename__ \
    else pasivo
    """

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