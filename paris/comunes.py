# -*- coding: utf-8 -*-
'''
Created on 08/04/2012

@author: nestor
'''

from datetime import datetime
from paris.models.spuria import (
    acceso,
    accion,
    acciones,
    busqueda,
    calificacion,
    calificacion_resena,
    categoria,
    cliente,
    codigo_de_error,
    columnas_no_visibles,
    consumidor,
    croquis,
    DBSession,
    describible,
    descripcion,
    dia,
    estadisticas,
    estatus,
    factura,
    foto,
    grado_de_instruccion,
    grupo_de_edad,
    idioma,
    inventario,
    mensaje,
    patrocinante,
    privilegios,
    producto,
    publicidad,
    rastreable,
    seguidor,
    territorio,
    tienda,
    tipo_de_codigo,
    usuario,
    sexo,
    visibilidad
)
from pyramid.decorator import reify
from sqlalchemy import and_, or_, case, func
from sqlalchemy.sql.expression import asc
from time import strftime, strptime

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
        
        fecha_decimal = DBSession.query(rastreable.fecha_de_creacion).\
        filter_by(rastreable_id = comentario.rastreable_p).first()[0]
        
        fecha = str(fecha_decimal)
        tmp['fecha'] = "{0}/{1}/{2} {3}:{4}".format(fecha[6:8], fecha[4:6], fecha[0:4], fecha[8:10], fecha[10:12])
        
        tmp['consumidor'] = DBSession.query(usuario).\
        join(consumidor).\
        filter_by(consumidor_id = comentario.consumidor_id).first()
        
        resultado.append(tmp)
    return resultado

def formatear_entrada_registro(reg, peticion, demandante):
    def obtener_objeto(tipo, tipo_id, muestro_href):
        return {
            'cliente': lambda x, y: reg_cliente(x, y),
            'usuario': lambda x, y: reg_usuario(x, y),
            'inventario': lambda x, y: reg_inventario(x, y),
            'croquis': lambda x, y: reg_croquis(x, y),
            'producto': lambda x, y: reg_producto(x, y),
            'mensaje': lambda x, y: reg_mensaje(x, y),
            'busqueda': lambda x, y: reg_busqueda(x, y),
            'calificacion_resena': lambda x, y: reg_calificacion_resena(x, y),
            'seguidor': lambda x, y: reg_seguidor(x, y),
            'descripcion': lambda x, y: reg_descripcion(x, y),
            'publicidad': lambda x, y: reg_publicidad(x, y),
            'estadisticas': lambda x, y: reg_estadisticas(x, y),
            'croquis': lambda x, y: reg_croquis(x, y),
            'factura': lambda x, y: reg_factura(x, y)
        }[tipo](tipo_id, muestro_href)
    def reg_cliente(_id, muestro_href):
        valor = {}
        diccionario = DBSession.query(cliente).\
        filter_by(rastreable_p = _id).first()
        
        valor['nombre'] = diccionario.nombre_comun
        valor['titulo'] = diccionario.nombre_legal
        
        valor['foto'] = DBSession.query(foto.ruta_de_foto).\
        join(describible).\
        join(cliente).\
        filter(cliente.rastreable_p == _id)

        tmp1, tmp2 = DBSession.query(case([
            (cliente.rif == tienda.cliente_p, 'tienda'),
            (cliente.rif == patrocinante.cliente_p, 'patrocinante'),
        ]),
        case([
            (cliente.rif == tienda.cliente_p, tienda.tienda_id),
            (cliente.rif == patrocinante.cliente_p, patrocinante.patrocinante_id),
        ])).\
        filter(and_(
            or_(
                cliente.rif == tienda.cliente_p, 
                cliente.rif == patrocinante.cliente_p
            ),
            cliente.rastreable_p == _id, 
        )).first()
        
        valor['href'] = {
            'tienda': lambda x: peticion.route_url('tienda', tienda_id = x),
            'patrocinante': lambda x: peticion.route_url('patrocinante', patrocinante_id = x)
        }[tmp1](tmp2) if muestro_href else None
    
        valor['diccionario'] = {
            'Nombre legal': diccionario.nombre_legal,
            'Nombre comun': diccionario.nombre_comun,
            'RIF': diccionario.rif,
            'Estatus': diccionario.estatus,
            'Propietario': diccionario.propietario,
            'Categoria': diccionario.categoria,
            'Telefono': diccionario.telefono,
            'Ubicacion': diccionario.ubicacion
        }
        
        return valor
    def reg_usuario(_id, muestro_href):
        valor = {}
        diccionario = DBSession.query(usuario).\
        filter_by(rastreable_p = _id).first()
        valor['nombre'] = valor['titulo'] = "{0} {1}".format(diccionario.nombre, diccionario.apellido)
        valor['foto'] = DBSession.query(foto.ruta_de_foto).\
        join(describible).\
        join(usuario).\
        filter(usuario.rastreable_p == _id)
        
        valor['href'] = peticion.route_url('usuario', usuario_id = diccionario.usuario_id) if muestro_href else None
        
        valor['diccionario'] = {
            'Nombre': valor['nombre'],
            'Estatus': diccionario.estatus,
            'Ubicacion': diccionario.ubicacion
        }
        return valor
    def reg_inventario(_id, muestro_href):
        valor = {}
        diccionario = DBSession.query(inventario).\
        filter_by(rastreable_p = _id).first()
        valor['titulo'] = valor['nombre'] = diccionario.descripcion
        valor['foto'] = DBSession.query(foto.ruta_de_foto).\
        join(describible).\
        join(producto).\
        join(inventario).\
        filter(inventario.rastreable_p == _id)
        
        valor['href'] = peticion.route_url('producto', producto_id = diccionario.producto_id) if muestro_href else None
        
        tipo_codigo, codigo = DBSession.query(producto.tipo_de_codigo, producto.codigo).\
        filter(producto.producto_id == diccionario.producto_id).first()
        
        valor['diccionario'] = {
            'Descripcion': valor['nombre'],
            'SKU': diccionario.codigo,
            tipo_codigo: codigo
        }
        return valor
    def reg_croquis(_id, muestro_href):
        valor = {}
        valor['titulo'] = valor['nombre'] = 'croquis'
        valor['href'] = '#' if muestro_href else None
        valor['diccionario'] = {}
        return valor
    def reg_producto(_id, muestro_href):
        valor = {}
        tmp1, tmp2 = DBSession.query(producto.fabricante, producto.nombre).\
        filter_by(rastreable_p = _id).first()
        valor['foto'] = DBSession.query(foto.ruta_de_foto).\
        join(describible).\
        join(producto).\
        filter(producto.rastreable_p == _id)
        valor['nombre'] = valor['titulo'] = "{0} {1}".format(tmp1, tmp2)
        
        if muestro_href:
            tmp3 = DBSession.query(producto.producto_id).filter_by(rastreable_p = _id).first()
            tmp4 = tmp3[0] if (tmp3 is not None) else None
            valor['href'] = peticion.route_url('producto', producto_id = tmp4)
        else:
            valor['href'] = None
            
        valor['diccionario'] = {}
        return valor
    def reg_mensaje(_id, muestro_href):
        valor = {}
        valor['nombre'] = valor['titulo'] = 'mensaje'
        valor['href'] = '#' if muestro_href else None
        valor['diccionario'] = {}
        return valor
    def reg_busqueda(_id, muestro_href):
        valor = {}
        valor['nombre'] = valor['titulo'] = 'busqueda'
        valor['href'] = '#' if muestro_href else None
        valor['diccionario'] = {}
        return valor
    def reg_calificacion_resena(_id, muestro_href):
        valor = {}
        valor['nombre'] = valor['titulo'] = 'comentario'
        valor['href'] = '#' if muestro_href else None
        valor['diccionario'] = {}
        return valor
    def reg_seguidor(_id, muestro_href):
        valor = {}
        valor['nombre'] = valor['titulo'] = 'seguidor'
        valor['href'] = '#' if muestro_href else None
        valor['diccionario'] = {}
        return valor
    def reg_descripcion(_id, muestro_href):
        valor = {}
        valor['nombre'] = 'descripcion'
        tmp = DBSession.query(case([
            (descripcion.describible == producto.describible_p, func.concat(producto.fabricante, ' ', producto.nombre)),
            (descripcion.describible == cliente.describible_p, cliente.nombre_legal),
            (descripcion.describible == usuario.describible_p, func.concat(usuario.nombre, ' ', usuario.apellido)),
            (descripcion.describible == publicidad.describible_p, publicidad.nombre),
        ])).\
        filter(and_(
            or_(
                descripcion.describible == producto.describible_p,
                descripcion.describible == cliente.describible_p,
                descripcion.describible == usuario.describible_p,
                descripcion.describible == publicidad.describible_p
            ),
            descripcion.rastreable_p == _id
        )).first()
        valor['titulo'] = tmp[0] if (tmp is not None) else ""
        valor['href'] = '#' if muestro_href else None
        valor['diccionario'] = {}
        return valor
    def reg_publicidad(_id, muestro_href):
        valor = {}
        valor['nombre'] = 'publicidad'
        tmp = DBSession.query(publicidad.nombre).\
        filter_by(rastreable_p = _id).first()
        valor['titulo'] = tmp[0] if (tmp is not None) else ""
        valor['href'] = '#' if muestro_href else None
        valor['diccionario'] = {}
        return valor
    def reg_estadisticas(_id, muestro_href):
        valor = {}
        valor['nombre'] = valor['titulo'] = 'estadisticas'
        valor['href'] = '#' if muestro_href else None
        valor['diccionario'] = {}
        return valor
    def reg_factura(_id, muestro_href):
        valor = {}
        valor['nombre'] = valor['titulo'] = 'factura'
        valor['href'] = '#' if muestro_href else None
        valor['diccionario'] = {}
        return valor
    def depurar_columnas_registro(diccionario):
        return dict((entrada[0].replace('_', ' '), entrada[1]) for entrada in diccionario.items() if entrada[0] not in columnas_no_visibles)
    def pulir_columnas_registro(diccionario):
        return dict((entrada[0].capitalize(), entrada[1]) for entrada in diccionario.items())
    
    por_defecto = {}
    por_defecto['nombre'] = por_defecto['titulo'] = ''
    por_defecto['href'] = None
    
    tipo_activo = rastreable_a_tipo(reg.actor_activo)
    activo = obtener_objeto(tipo_activo, reg.actor_activo, demandante != tipo_activo) if (tipo_activo is not None) else por_defecto
    if 'foto' in activo:
        tmp = activo['foto'].filter(foto.ruta_de_foto.like('%miniaturas%')).first()
        activo['foto'] = tmp[0] if (tmp is not None) else ''
    else:
        activo['foto'] = ''
    
    tipo_pasivo = rastreable_a_tipo(reg.actor_pasivo)
    pasivo = obtener_objeto(tipo_pasivo, reg.actor_pasivo, demandante != tipo_pasivo) if (tipo_pasivo is not None) else por_defecto
    if 'foto' in pasivo:
        tmp = pasivo['foto'].filter(foto.ruta_de_foto.like('%miniaturas%')).first()
        pasivo['foto'] = tmp[0] if (tmp is not None) else ''
    else:
        pasivo['foto'] = ''
    
    entrada = {}
    entrada['actor_activo'] = activo
    entrada['actor_pasivo'] = pasivo
    entrada['accion'] = acciones[reg.accion]
    entrada['info'] = activo if demandante != tipo_activo else pasivo
                    
    columnas = reg.columna.split('<|>') if (reg.columna is not None) else ''
    valores = reg.valor.split('<|>') if (reg.valor is not None) else ''
    diccionario = dict(zip(columnas, valores)) if (len(columnas) == len(valores)) else {'Error': 'Numero de columnas y valores no concuerda'}
    diccionario_depurado = depurar_columnas_registro(diccionario)
    entrada['parametros'] = diccionario_depurado if (entrada['accion'] == 'actualizo') else {}

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
            entrada['tiempo'] = "{0} hora(s)".format(str(diferencia.seconds/3600))
        elif diferencia.seconds < 3600 and diferencia.seconds > 60:
            entrada['tiempo'] = "{0} minuto(s)".format(str(diferencia.seconds/60))
        else:
            entrada['tiempo'] = "{0} segundo(s)".format(str(diferencia.seconds))
    
    return entrada

def rastreable_a_tipo(rastreable_id):
    tmp = DBSession.query(case([(rastreable_id == cliente.rastreable_p, 'cliente')])).\
    filter(rastreable_id == cliente.rastreable_p).first()
    if (tmp is not None):
        return tmp[0]
    
    tmp = DBSession.query(case([(rastreable_id == inventario.rastreable_p, 'inventario')])).\
    filter(rastreable_id == inventario.rastreable_p).first()
    if (tmp is not None):
        return tmp[0]
    
    tmp = DBSession.query(case([(rastreable_id == producto.rastreable_p, 'producto')])).\
    filter(rastreable_id == producto.rastreable_p).first()
    if (tmp is not None):
        return tmp[0]
    
    tmp = DBSession.query(case([(rastreable_id == mensaje.rastreable_p, 'mensaje')])).\
    filter(rastreable_id == mensaje.rastreable_p).first()
    if (tmp is not None):
        return tmp[0]
    
    tmp = DBSession.query(case([(rastreable_id == usuario.rastreable_p, 'usuario')])).\
    filter(rastreable_id == usuario.rastreable_p).first()
    if (tmp is not None):
        return tmp[0]
    
    tmp = DBSession.query(case([(rastreable_id == busqueda.rastreable_p, 'busqueda')])).\
    filter(rastreable_id == busqueda.rastreable_p).first()
    if (tmp is not None):
        return tmp[0]
    
    tmp = DBSession.query(case([(rastreable_id == calificacion_resena.rastreable_p, 'calificacion_resena')])).\
    filter(rastreable_id == calificacion_resena.rastreable_p).first()
    if (tmp is not None):
        return tmp[0]
    
    tmp = DBSession.query(case([(rastreable_id == seguidor.rastreable_p, 'seguidor')])).\
    filter(rastreable_id == seguidor.rastreable_p).first()
    if (tmp is not None):
        return tmp[0]
    
    tmp = DBSession.query(case([(rastreable_id == descripcion.rastreable_p, 'descripcion')])).\
    filter(rastreable_id == descripcion.rastreable_p).first()
    if (tmp is not None):
        return tmp[0]
    
    tmp = DBSession.query(case([(rastreable_id == publicidad.rastreable_p, 'publicidad')])).\
    filter(rastreable_id == publicidad.rastreable_p).first()
    if (tmp is not None):
        return tmp[0]
    
    tmp = DBSession.query(case([(rastreable_id == estadisticas.rastreable_p, 'estadisticas')])).\
    filter(rastreable_id == estadisticas.rastreable_p).first()
    if (tmp is not None):
        return tmp[0]
    
    tmp = DBSession.query(case([(rastreable_id == croquis.rastreable_p, 'croquis')])).\
    filter(rastreable_id == croquis.rastreable_p).first()
    if (tmp is not None):
        return tmp[0]
    
    tmp = DBSession.query(case([(rastreable_id == factura.rastreable_p, 'factura')])).\
    filter(rastreable_id == factura.rastreable_p).first()
    if (tmp is not None):
        return tmp[0]
    
    return None
    """
    tmp = DBSession.query(case([
        (rastreable_id == cliente.rastreable_p, 'cliente'),
        (rastreable_id == inventario.rastreable_p, 'inventario'),
        (rastreable_id == producto.rastreable_p, 'producto'),
        (rastreable_id == mensaje.rastreable_p, 'mensaje'),
        (rastreable_id == usuario.rastreable_p, 'usuario'),
        (rastreable_id == busqueda.rastreable_p, 'busqueda'),
        (rastreable_id == calificacion_resena.rastreable_p, 'calificacion_resena'),
        (rastreable_id == seguidor.rastreable_p, 'seguidor'),
        (rastreable_id == descripcion.rastreable_p, 'descripcion'),
        (rastreable_id == publicidad.rastreable_p, 'publicidad'),
        (rastreable_id == estadisticas.rastreable_p, 'estadisticas'),
        (rastreable_id == croquis.rastreable_p, 'croquis'),
        (rastreable_id == factura.rastreable_p, 'factura')
    ])).\
    filter(or_(
        rastreable_id == cliente.rastreable_p,
        rastreable_id == inventario.rastreable_p,
        rastreable_id == producto.rastreable_p,
        rastreable_id == mensaje.rastreable_p,
        rastreable_id == usuario.rastreable_p,
        rastreable_id == busqueda.rastreable_p,
        rastreable_id == calificacion_resena.rastreable_p,
        rastreable_id == seguidor.rastreable_p,
        rastreable_id == descripcion.rastreable_p,
        rastreable_id == publicidad.rastreable_p,
        rastreable_id == estadisticas.rastreable_p,
        rastreable_id == croquis.rastreable_p,
        rastreable_id == factura.rastreable_p
    )).first()

    return tmp[0] if (tmp is not None) else None
    """

def sql_foto(objeto, objeto_id, tamano):
    def foto_tienda():
        return DBSession.query(foto).\
        join(describible).\
        join(cliente).\
        join(tienda).\
        filter(and_(tienda.tienda_id == objeto_id, foto.ruta_de_foto.like('%' + tamano + '%')))
    def foto_producto():
        return DBSession.query(foto).\
        join(describible).\
        join(producto).\
        filter(and_(producto.producto_id == objeto_id, foto.ruta_de_foto.like('%' + tamano + '%')))
    def foto_patrocinante():
        return DBSession.query(foto).\
        join(describible).\
        join(cliente).\
        join(patrocinante).\
        filter(and_(
            patrocinante.patrocinante_id == objeto_id, 
            foto.ruta_de_foto.like('%' + tamano + '%'))
        )
    def foto_publicidad():
        return DBSession.query(foto).\
        join(describible).\
        join(publicidad).\
        filter(and_(
            publicidad.publicidad_id == objeto_id, 
            foto.ruta_de_foto.like('%' + tamano + '%'))
        )
    def foto_usuario():
        return DBSession.query(foto).\
        join(describible).\
        join(usuario).\
        filter(and_(
            usuario.usuario_id == objeto_id, 
            foto.ruta_de_foto.like('%' + tamano + '%'))
        )

    sql = {
        'tienda': lambda: foto_tienda(), 
        'producto': lambda: foto_producto(), 
        'patrocinante': lambda: foto_patrocinante(), 
        'publicidad': lambda: foto_publicidad(),
        'usuario': lambda: foto_usuario()
    }[objeto]()
    
    return sql

class Comunes(object):
    def __init__(self):
        pass
    
    @reify
    def categorias(self):
        return DBSession.query(categoria).all()
    
    @reify
    def paises(self):
        return DBSession.query(territorio).filter_by(nivel = 1).all()
    
    @reify
    def grados_de_instruccion(self):
        return DBSession.query(grado_de_instruccion).order_by(asc(grado_de_instruccion.orden)).all()
    
    @reify
    def sexos(self):
        return DBSession.query(sexo).all()
    
    @reify
    def codigos_de_error(self):
        return DBSession.query(codigo_de_error).all()
    
    @reify
    def privilegios(self):
        return DBSession.query(privilegios).all()
    
    @reify
    def idiomas(self):
        return DBSession.query(idioma).all()
    
    @reify
    def tipos_de_codigo(self):
        return DBSession.query(tipo_de_codigo).all()
    
    @reify
    def visibilidades(self):
        return DBSession.query(visibilidad).all()
    
    @reify
    def acciones(self):
        return DBSession.query(accion).all()
    
    @reify
    def calificaciones(self):
        return DBSession.query(calificacion).all()
    
    @reify
    def grupos_de_edades(self):
        return DBSession.query(grupo_de_edad).all()

    @reify
    def estatus(self):
        return DBSession.query(estatus).all()
    
    @reify
    def dias(self):
        return DBSession.query(dia).order_by(asc(dia.orden)).all()
    
    @reify
    def turnos(self):
        return ['Abierto', 'Cerrado']
    
    def obtener_foto(self, objeto, objeto_id, tamano):
        return sql_foto(objeto, objeto_id, tamano).first()
    
    def obtener_fotos(self, objeto, objeto_id, tamano):
        return sql_foto(objeto, objeto_id, tamano).all()
    
    def obtener_ruta_territorio(self, terr_id):
        ruta = []
        
        while True:
            terr = self.obtener_territorio(terr_id)
            ruta.append(terr)
            
            if (terr.territorio_padre == terr.territorio_id) \
            or (terr.territorio_padre == None) \
            or (terr.nivel == 1):
                break
            else:
                terr_id = terr.territorio_padre
    
        ruta.reverse()
        return ruta
    
    def obtener_ruta_categoria(self, cat_id):
        ruta = []
        
        while True:
            cat = self.obtener_categoria(cat_id)
            ruta.append(cat)
            if (cat.hijo_de_categoria == cat.categoria_id) or (cat.hijo_de_categoria == None):
                break
            else:
                cat_id = cat.hijo_de_categoria
        
        ruta.reverse()
        return ruta
        
    def obtener_territorio(self, terr_id):
        return DBSession.query(territorio).filter_by(territorio_id = terr_id).first()
    
    def obtener_categoria(self, cat_id):
        return DBSession.query(categoria).filter_by(categoria_id = cat_id).first()
            
    def obtener_cliente(self, cli_id):
        return DBSession.query(cliente).filter_by(rif = cli_id).first()
    
    def obtener_cliente_padre(self, objeto, objeto_id):
        def cli_tienda(_id):
            return DBSession.query(cliente).\
            join(tienda).\
            filter(tienda.tienda_id == _id).first()
        def cli_patrocinante(_id):
            return DBSession.query(cliente).\
            join(patrocinante).\
            filter(patrocinante.patrocinante_id == _id).first()
        
        resultado = {
            'tienda': lambda x: cli_tienda(x), 
            'patrocinante': lambda x: cli_patrocinante(x)
        }[objeto](objeto_id)
        
        return resultado
    
    def obtener_tienda(self, tie_id):
        return DBSession.query(tienda).filter_by(tienda_id = tie_id).first()
    
    def obtener_patrocinante(self, pat_id):
        return DBSession.query(patrocinante).filter_by(patrocinante_id = pat_id).first()
    
    def obtener_producto(self, pro_id):
        return DBSession.query(producto).filter_by(producto_id = pro_id).first()
    
    def obtener_usuario(self, objeto, objeto_id):
        def usu_id(_id):
            return DBSession.query(usuario).filter_by(usuario_id = _id).first()
        def usu_correo(correo):
            return DBSession.query(usuario).\
            join(acceso).\
            filter(acceso.correo_electronico == correo).first()
    
        tmp = {
            'id': lambda x: usu_id(x), 
            'correo_electronico': lambda x: usu_correo(x)
        }[objeto](objeto_id)
        
        return tmp