# -*- coding: utf-8 -*-
'''
Created on 08/04/2012

@author: nestor
'''

from datetime import datetime
from models.funciones import acciones, columnas_no_visibles
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
    Sexo,
    Visibilidad
)
from spuria.orm.descripciones_fotos import DescribibleAsociacion
from pyramid.decorator import reify
from sqlalchemy import and_, case, func
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

        fecha = str(comentario.rastreable.fecha_de_creacion)
        """
        fecha_decimal = DBSession.query(Rastreable.fecha_de_creacion).\
        filter_by(rastreable_id = comentario.rastreable_p).first()[0]
        fecha = str(fecha_decimal)
        """
        tmp['fecha'] = "{0}/{1}/{2} {3}:{4}".format(
            fecha[6:8], fecha[4:6], fecha[0:4], fecha[8:10], fecha[10:12]
        )

        tmp['consumidor'] = DBSession.query(Consumidor).\
        filter_by(consumidor_id = comentario.consumidor_id).first()

        resultado.append(tmp)
    return resultado

def formatear_entrada_registro(reg, peticion, demandante):
    def obtener_objeto(tipo, tipo_id, muestro_href):
        return {
            'Cliente': lambda x, y: reg_cliente(x, y),
            'Usuario': lambda x, y: reg_usuario(x, y),
            'Inventario': lambda x, y: reg_inventario(x, y),
            'Croquis': lambda x, y: reg_croquis(x, y),
            'Producto': lambda x, y: reg_producto(x, y),
            'Mensaje': lambda x, y: reg_mensaje(x, y),
            'Busqueda': lambda x, y: reg_busqueda(x, y),
            'CalificacionResena': lambda x, y: reg_calificacion_resena(x, y),
            'Seguimiento': lambda x, y: reg_seguimiento(x, y),
            'Descripcion': lambda x, y: reg_descripcion(x, y),
            'Publicidad': lambda x, y: reg_publicidad(x, y),
            'Estadisticas': lambda x, y: reg_estadisticas(x, y),
            'Factura': lambda x, y: reg_factura(x, y)
        }[tipo](tipo_id, muestro_href)
    def reg_cliente(_id, muestro_href):
        valor = {}
        diccionario = DBSession.query(Cliente).\
        filter_by(rastreable_p = _id).first()
        
        valor['nombre'] = diccionario.nombre_comun
        valor['titulo'] = diccionario.nombre_legal
        
        valor['foto'] = DBSession.query(Foto.ruta_de_foto).\
        join(Describible).\
        join(Cliente).\
        filter(Cliente.rastreable_p == _id)

        x1 = DBSession.query(
            case([(Cliente.rif == Tienda.cliente_p, 'Tienda')]),
            case([(Cliente.rif == Tienda.cliente_p, Tienda.tienda_id)])
        ).filter(and_(
            Cliente.rif == Tienda.cliente_p, 
            Cliente.rastreable_p == _id
        ))
        
        x2 = DBSession.query(
            case([(Cliente.rif == Patrocinante.cliente_p, 'Patrocinante')]),
            case([(
                Cliente.rif == Patrocinante.cliente_p, 
                Patrocinante.patrocinante_id
            )])
        ).filter(and_(
            Cliente.rif == Patrocinante.cliente_p,
            Cliente.rastreable_p == _id
        ))
        
        tmp1, tmp2 = x1.union(x2).first()
        
        valor['href'] = {
            'Tienda': lambda x: peticion.route_url('tienda', tienda_id = x),
            'Patrocinante': lambda x: peticion.route_url(
                'patrocinante', patrocinante_id = x
            )
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
        diccionario = DBSession.query(Usuario).\
        filter_by(rastreable_p = _id).first()
        valor['nombre'] = valor['titulo'] = "{0} {1}".format(
            diccionario.nombre, diccionario.apellido
        )
        valor['foto'] = DBSession.query(Foto.ruta_de_foto).\
        join(Describible).\
        join(Usuario).\
        filter(Usuario.rastreable_p == _id)
        
        valor['href'] = peticion.route_url(
            'usuario', usuario_id = diccionario.usuario_id
        ) if muestro_href else None
        
        valor['diccionario'] = {
            'Nombre': valor['nombre'],
            'Estatus': diccionario.estatus,
            'Ubicacion': diccionario.ubicacion
        }
        return valor
    def reg_inventario(_id, muestro_href):
        valor = {}
        diccionario = DBSession.query(Inventario).\
        filter_by(rastreable_p = _id).first()
        valor['titulo'] = valor['nombre'] = diccionario.descripcion
        valor['foto'] = DBSession.query(Foto.ruta_de_foto).\
        join(Describible).\
        join(Producto).\
        join(Inventario).\
        filter(Inventario.rastreable_p == _id)
        
        valor['href'] = peticion.route_url(
            'producto', producto_id = diccionario.producto_id
        ) if muestro_href else None
        
        tipo_codigo, codigo = DBSession.query(
            Producto.tipo_de_codigo, Producto.codigo
        ).filter(Producto.producto_id == diccionario.producto_id).first()
        
        valor['diccionario'] = {
            'Descripcion': valor['nombre'],
            'SKU': diccionario.codigo,
            tipo_codigo: codigo
        }
        return valor
    def reg_croquis(_id, muestro_href):
        valor = {}
        valor['titulo'] = valor['nombre'] = 'Croquis'
        valor['href'] = '#' if muestro_href else None
        valor['diccionario'] = {}
        return valor
    def reg_producto(_id, muestro_href):
        valor = {}
        tmp1, tmp2 = DBSession.query(Producto.fabricante, Producto.nombre).\
        filter_by(rastreable_p = _id).first()
        valor['foto'] = DBSession.query(Foto.ruta_de_foto).\
        join(Describible).\
        join(Producto).\
        filter(Producto.rastreable_p == _id)
        valor['nombre'] = valor['titulo'] = "{0} {1}".format(tmp1, tmp2)
        
        if muestro_href:
            tmp3 = DBSession.query(Producto.producto_id).\
            filter_by(rastreable_p = _id).first()
            tmp4 = tmp3[0] if (tmp3 is not None) else None
            valor['href'] = peticion.route_url('producto', producto_id = tmp4)
        else:
            valor['href'] = None
            
        valor['diccionario'] = {}
        return valor
    def reg_mensaje(_id, muestro_href):
        valor = {}
        valor['nombre'] = valor['titulo'] = 'Mensaje'
        valor['href'] = '#' if muestro_href else None
        valor['diccionario'] = {}
        return valor
    def reg_busqueda(_id, muestro_href):
        valor = {}
        valor['nombre'] = valor['titulo'] = 'Busqueda'
        valor['href'] = '#' if muestro_href else None
        valor['diccionario'] = {}
        return valor
    def reg_calificacion_resena(_id, muestro_href):
        valor = {}
        valor['nombre'] = valor['titulo'] = 'comentario'
        valor['href'] = '#' if muestro_href else None
        valor['diccionario'] = {}
        return valor
    def reg_seguimiento(_id, muestro_href):
        valor = {}
        valor['nombre'] = valor['titulo'] = 'Seguimiento'
        valor['href'] = '#' if muestro_href else None
        valor['diccionario'] = {}
        return valor
    def reg_descripcion(_id, muestro_href):
        valor = {}
        valor['nombre'] = 'Descripcion'
        
        x1 = DBSession.query(case([(
            Descripcion.describible == Producto.describible_p, 
            func.concat(Producto.fabricante, ' ', Producto.nombre)
        )])).filter(and_(
            Descripcion.describible == Producto.describible_p,
            Descripcion.rastreable_p == _id
        ))
        
        x2 = DBSession.query(case([(
            Descripcion.describible == Cliente.describible_p, 
            Cliente.nombre_legal
        )])).filter(and_(
            Descripcion.describible == Cliente.describible_p,
            Descripcion.rastreable_p == _id
        ))
        
        x3 = DBSession.query(case([(
            Descripcion.describible == Usuario.describible_p, 
            func.concat(Usuario.nombre, ' ', Usuario.apellido)
        )])).filter(and_(
            Descripcion.describible == Usuario.describible_p,
            Descripcion.rastreable_p == _id
        ))
        
        x4 = DBSession.query(case([(
            Descripcion.describible == Publicidad.describible_p, 
            Publicidad.nombre
        )])).filter(and_(
            Descripcion.describible == Publicidad.describible_p,
            Descripcion.rastreable_p == _id
        ))
        
        tmp = x1.union(x2, x3, x4).first()
        valor['titulo'] = tmp[0] if (tmp is not None) else ""
        valor['href'] = '#' if muestro_href else None
        valor['diccionario'] = {}
        return valor
    def reg_publicidad(_id, muestro_href):
        valor = {}
        valor['nombre'] = 'Publicidad'
        tmp = DBSession.query(Publicidad.nombre).\
        filter_by(rastreable_p = _id).first()
        valor['titulo'] = tmp[0] if (tmp is not None) else ""
        valor['href'] = '#' if muestro_href else None
        valor['diccionario'] = {}
        return valor
    def reg_estadisticas(_id, muestro_href):
        valor = {}
        valor['nombre'] = valor['titulo'] = 'Estadisticas'
        valor['href'] = '#' if muestro_href else None
        valor['diccionario'] = {}
        return valor
    def reg_factura(_id, muestro_href):
        valor = {}
        valor['nombre'] = valor['titulo'] = 'Factura'
        valor['href'] = '#' if muestro_href else None
        valor['diccionario'] = {}
        return valor
    def depurar_columnas_registro(diccionario):
        return dict((entrada[0].replace('_', ' '), entrada[1]) \
        for entrada in diccionario.items() \
        if entrada[0] not in columnas_no_visibles)
    def pulir_columnas_registro(diccionario):
        return dict((entrada[0].capitalize(), entrada[1]) \
        for entrada in diccionario.items())
    
    por_defecto = {}
    por_defecto['nombre'] = por_defecto['titulo'] = ''
    por_defecto['href'] = None
    
    tipo_activo = rastreable_a_tipo(reg.actor_activo)
    activo = obtener_objeto(
        tipo_activo, reg.actor_activo, demandante != tipo_activo
    ) if (tipo_activo is not None) else por_defecto
    
    if 'foto' in activo:
        tmp = activo['foto'].filter(
            Foto.ruta_de_foto.like('%miniaturas%')
        ).first()
        activo['foto'] = tmp[0] if (tmp is not None) else ''
    else:
        activo['foto'] = ''
    
    tipo_pasivo = rastreable_a_tipo(reg.actor_pasivo)
    pasivo = obtener_objeto(
        tipo_pasivo, reg.actor_pasivo, demandante != tipo_pasivo
    ) if (tipo_pasivo is not None) else por_defecto
    
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
    entrada['accion'] = acciones[reg.accion]
    entrada['info'] = activo if demandante != tipo_activo else pasivo
                    
    columnas = reg.columna.split('<|>') if (reg.columna is not None) else ''
    valores = reg.valor.split('<|>') if (reg.valor is not None) else ''
    
    diccionario = dict(zip(columnas, valores)) \
    if (len(columnas) == len(valores)) \
    else {'Error': 'Numero de columnas y valores no concuerda'}
    
    diccionario_depurado = depurar_columnas_registro(diccionario)
    entrada['parametros'] = diccionario_depurado \
    if (entrada['accion'] == 'actualizo') else {}

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

def rastreable_a_tipo(rastreable_id):
    tmp1 = DBSession.query(case([(
        rastreable_id == Cliente.rastreable_p, 'Cliente'
    )])).filter(rastreable_id == Cliente.rastreable_p)
    
    tmp2 = DBSession.query(case([(
        rastreable_id == Inventario.rastreable_p, 'Inventario'
    )])).filter(rastreable_id == Inventario.rastreable_p)
    
    tmp3 = DBSession.query(case([(
        rastreable_id == Producto.rastreable_p, 'Producto'
    )])).filter(rastreable_id == Producto.rastreable_p)
    
    tmp4 = DBSession.query(case([(
        rastreable_id == Mensaje.rastreable_p, 'Mensaje'
    )])).filter(rastreable_id == Mensaje.rastreable_p)
    
    tmp5 = DBSession.query(case([(
        rastreable_id == Usuario.rastreable_p, 'Usuario'
    )])).filter(rastreable_id == Usuario.rastreable_p)
    
    tmp6 = DBSession.query(case([(
        rastreable_id == Busqueda.rastreable_p, 'Busqueda'
    )])).filter(rastreable_id == Busqueda.rastreable_p)
    
    tmp7 = DBSession.query(case([(
        rastreable_id == CalificacionResena.rastreable_p, 'CalificacionResena'
    )])).filter(rastreable_id == CalificacionResena.rastreable_p)
    
    tmp8 = DBSession.query(case([(
        rastreable_id == Seguimiento.rastreable_p, 'Seguimiento'
    )])).filter(rastreable_id == Seguimiento.rastreable_p)
    
    tmp9 = DBSession.query(case([(
        rastreable_id == Descripcion.rastreable_p, 'Descripcion'
    )])).filter(rastreable_id == Descripcion.rastreable_p)
    
    tmp10 = DBSession.query(case([(
        rastreable_id == Publicidad.rastreable_p, 'Publicidad'
    )])).filter(rastreable_id == Publicidad.rastreable_p)
    
    tmp11 = DBSession.query(case([(
        rastreable_id == Estadisticas.rastreable_p, 'Estadisticas'
    )])).filter(rastreable_id == Estadisticas.rastreable_p)
    
    tmp12 = DBSession.query(case([(
        rastreable_id == Croquis.rastreable_p, 'Croquis'
    )])).filter(rastreable_id == Croquis.rastreable_p)
        
    tmp13 = DBSession.query(case([(
        rastreable_id == Factura.rastreable_p, 'Factura'
    )])).filter(rastreable_id == Factura.rastreable_p)
    
    tmp = tmp1.union(
        tmp2, tmp3, tmp4, tmp5, tmp6, tmp7, tmp8, tmp9, tmp10, tmp11, tmp12, 
        tmp13
    ).first()

    return tmp[0] if (tmp is not None) else None

def sql_foto(objeto, objeto_id, tamano):
    def foto_tienda():
        return DBSession.query(Foto).\
        join(Describible).\
        join(DescribibleAsociacion).\
        join(Cliente).\
        join(Tienda).\
        filter(and_(
            Tienda.tienda_id == objeto_id, 
            Foto.ruta_de_foto.like('%' + tamano + '%')
        ))
    def foto_producto():
        return DBSession.query(Foto).\
        join(Describible).\
        join(DescribibleAsociacion).\
        join(Producto).\
        filter(and_(
            Producto.producto_id == objeto_id, 
            Foto.ruta_de_foto.like('%' + tamano + '%')
        ))
    def foto_patrocinante():
        return DBSession.query(Foto).\
        join(Describible).\
        join(DescribibleAsociacion).\
        join(Cliente).\
        join(Patrocinante).\
        filter(and_(
            Patrocinante.patrocinante_id == objeto_id, 
            Foto.ruta_de_foto.like('%' + tamano + '%')
        ))
    def foto_publicidad():
        return DBSession.query(Foto).\
        join(Describible).\
        join(DescribibleAsociacion).\
        join(Publicidad).\
        filter(and_(
            Publicidad.publicidad_id == objeto_id, 
            Foto.ruta_de_foto.like('%' + tamano + '%')
        ))
    def foto_usuario():
        return DBSession.query(Foto).\
        join(Describible).\
        join(DescribibleAsociacion).\
        join(Usuario).\
        filter(and_(
            Usuario.usuario_id == objeto_id, 
            Foto.ruta_de_foto.like('%' + tamano + '%')
        ))

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
        return DBSession.query(Categoria).all()
    
    @reify
    def paises(self):
        return DBSession.query(Territorio).filter_by(nivel = 1).all()
    
    @reify
    def grados_de_instruccion(self):
        return DBSession.query(GradoDeInstruccion).\
        order_by(asc(GradoDeInstruccion.orden)).all()
    
    @reify
    def sexos(self):
        return DBSession.query(Sexo).all()
    
    @reify
    def codigos_de_error(self):
        return DBSession.query(CodigoDeError).all()
    
    @reify
    def privilegios(self):
        return DBSession.query(Privilegios).all()
    
    @reify
    def idiomas(self):
        return DBSession.query(Idioma).all()
    
    @reify
    def tipos_de_codigo(self):
        return DBSession.query(TipoDeCodigo).all()
    
    @reify
    def visibilidades(self):
        return DBSession.query(Visibilidad).all()
    
    @reify
    def acciones(self):
        return DBSession.query(Accion).all()
    
    @reify
    def calificaciones(self):
        return DBSession.query(Calificacion).all()
    
    @reify
    def grupos_de_edades(self):
        return DBSession.query(GrupoDeEdad).all()

    @reify
    def estatus(self):
        return DBSession.query(Estatus).all()
    
    @reify
    def dias(self):
        return DBSession.query(Dia).order_by(asc(Dia.orden)).all()
    
    @reify
    def turnos(self):
        return ['Abierto', 'Cerrado']
    
    @reify
    def fotos_grandes(self):
        return self.obtener_fotos(
            self.tipo_de_peticion, self.peticion_id, 'grandes'
        )
    
    @reify
    def fotos_medianas(self):
        return self.obtener_fotos(
            self.tipo_de_peticion, self.peticion_id, 'medianas'
        )
    
    @reify
    def fotos_pequenas(self):
        return self.obtener_fotos(
            self.tipo_de_peticion, self.peticion_id, 'pequenas'
        )
    
    @reify
    def fotos_miniaturas(self):
        return self.obtener_fotos(
            self.tipo_de_peticion, self.peticion_id, 'miniaturas'
        )
    
    def obtener_foto(self, objeto, objeto_id, tamano):
        return sql_foto(objeto, objeto_id, tamano).first()
    
    def obtener_fotos(self, objeto, objeto_id, tamano):
        return sql_foto(objeto, objeto_id, tamano).all()
    
    def obtener_ruta_territorio(self, territorio):
        ruta = []
        
        while True:
            ruta.append(territorio)
            
            if (territorio.territorio_padre == territorio.territorio_id) \
            or (territorio.territorio_padre == None) \
            or (territorio.nivel == 1):
                break
            else:
                territorio = territorio.territorio_padre
    
        ruta.reverse()
        return ruta
    
    def obtener_ruta_categoria(self, categoria):
        ruta = []
        
        while True:
            ruta.append(categoria)
            if (categoria.hijo_de_categoria == categoria.categoria_id) or \
            (categoria.hijo_de_categoria == None):
                break
            else:
                categoria = categoria.padre
        
        ruta.reverse()
        return ruta
        
    def obtener_territorio(self, terr_id):
        return DBSession.query(Territorio).filter_by(territorio_id = terr_id).\
        first()
    
    def obtener_categoria(self, cat_id):
        return DBSession.query(Categoria).filter_by(categoria_id = cat_id).\
        first()

    def obtener_cliente(self, cli_id):
        return DBSession.query(Cliente).filter_by(rif = cli_id).first()
    
    def obtener_cliente_padre(self, objeto, objeto_id):
        def cli_tienda(_id):
            return DBSession.query(Cliente).\
            join(Tienda).\
            filter(Tienda.tienda_id == _id).first()
        def cli_patrocinante(_id):
            return DBSession.query(Cliente).\
            join(Patrocinante).\
            filter(Patrocinante.patrocinante_id == _id).first()
        
        resultado = {
            'tienda': lambda x: cli_tienda(x), 
            'patrocinante': lambda x: cli_patrocinante(x)
        }[objeto](objeto_id)
        
        return resultado
    
    def obtener_tienda(self, tie_id):
        return DBSession.query(Tienda).filter_by(tienda_id = tie_id).first()
    
    def obtener_patrocinante(self, pat_id):
        return DBSession.query(Patrocinante).filter_by(
            patrocinante_id = pat_id
        ).first()
    
    def obtener_producto(self, pro_id):
        return DBSession.query(Producto).filter_by(producto_id = pro_id).first()
    
    def obtener_usuario(self, objeto, objeto_id):
        def usu_id(_id):
            return DBSession.query(Usuario).filter_by(usuario_id = _id).first()
        def usu_correo(correo):
            return DBSession.query(Usuario).\
            join(Acceso).\
            filter(Acceso.correo_electronico == correo).first()
    
        tmp = {
            'id': lambda x: usu_id(x), 
            'correo_electronico': lambda x: usu_correo(x)
        }[objeto](objeto_id)
        
        return tmp