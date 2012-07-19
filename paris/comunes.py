# -*- coding: utf-8 -*-
'''
Created on 08/04/2012

@author: nestor
'''

from .constantes import ACCION
from .models import (
    busqueda,
    calificacion_resena,
    categoria,
    cliente,
    consumidor,
    croquis,
    DBSession,
    describible,
    descripcion,
    estadisticas,
    factura,
    foto,
    inventario,
    mensaje,
    patrocinante,
    producto,
    publicidad,
    rastreable,
    seguidor,
    territorio,
    tienda,
    usuario
)
from sqlalchemy import and_, or_, case, func
from datetime import datetime

class comunes(object):
    def __init__(self):
        pass
    
    def formatear_comentarios(self, comentarios):
        resultado = []
        for comentario in comentarios:
            tmp = {}
            tmp['calificacion'] = comentario.calificacion
            tmp['resena'] = comentario.resena
            
            fecha_decimal = DBSession.query(rastreable).\
            filter_by(rastreable_id = comentario.rastreable_p).one().fecha_de_creacion
            
            fecha = str(fecha_decimal)
            tmp['fecha'] = "{0}/{1}/{2} {3}:{4}".format(fecha[6:8], fecha[4:6], fecha[0:4], fecha[8:10], fecha[10:12])
            
            tmp['consumidor'] = DBSession.query(usuario).\
            join(consumidor).\
            filter_by(consumidor_id = comentario.consumidor_id).one()
            
            resultado.append(tmp)
        return resultado
    
    def formatear_entrada_registro(self, reg, peticion):
        def obtener_objeto(tipo, tipo_id):
            return {
                'cliente': lambda x: reg_cliente(x),
                'usuario': lambda x: reg_usuario(x),
                'inventario': lambda x: reg_inventario(x),
                'croquis': lambda x: reg_croquis(x),
                'producto': lambda x: reg_producto(x),
                'mensaje': lambda x: reg_mensaje(x),
                'busqueda': lambda x: reg_busqueda(x),
                'calificacion_resena': lambda x: reg_calificacion_resena(x),
                'seguidor': lambda x: reg_seguidor(x),
                'descripcion': lambda x: reg_descripcion(x),
                'publicidad': lambda x: reg_publicidad(x),
                'estadisticas': lambda x: reg_estadisticas(x),
                'croquis': lambda x: reg_croquis(x),
                'factura': lambda x: reg_factura(x)
            }[tipo](tipo_id)
        def reg_cliente(_id):
            valor = {}
            valor['nombre'], valor['titulo'] = DBSession.query(cliente.nombre_comun, cliente.nombre_legal).\
            filter_by(rastreable_p = _id).one()
            
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
            }[tmp1](tmp2)
            
            return valor
        def reg_usuario(_id):
            valor = {}
            tmp1, tmp2 = DBSession.query(usuario.nombre, usuario.apellido).\
            filter_by(rastreable_p = _id).one()
            valor['nombre'] = "{0} {1}".format(tmp1, tmp2)
            valor['foto'] = DBSession.query(foto.ruta_de_foto).\
            join(describible).\
            join(usuario).\
            filter(usuario.rastreable_p == _id)
            valor['href'] = '#'
            return valor
        def reg_inventario(_id):
            valor = {}
            tmp = DBSession.query(inventario.descripcion).\
            filter_by(rastreable_p = _id).one()
            valor['titulo'] = valor['nombre'] = tmp[0] if (tmp is not None) else None
            valor['foto'] = DBSession.query(foto.ruta_de_foto).\
            join(describible).\
            join(producto).\
            join(inventario).\
            filter(inventario.rastreable_p == _id)
            valor['href'] = '#'
            return valor
        def reg_croquis(_id):
            valor = {}
            valor['titulo'] = valor['nombre'] = 'croquis'
            valor['href'] = '#'
            return valor
        def reg_producto(_id):
            valor = {}
            tmp1, tmp2 = DBSession.query(producto.fabricante, producto.nombre).\
            filter_by(rastreable_p = _id).one()
            valor['foto'] = DBSession.query(foto.ruta_de_foto).\
            join(describible).\
            join(producto).\
            filter(producto.rastreable_p == _id)
            valor['nombre'] = valor['titulo'] = "{0} {1}".format(tmp1, tmp2)
            tmp3 = DBSession.query(producto.producto_id).filter_by(rastreable_p = _id).one()
            tmp4 = tmp3[0] if (tmp3 is not None) else None
            valor['href'] = peticion.route_url('producto', producto_id = tmp4)
            return valor
        def reg_mensaje(_id):
            valor = {}
            valor['nombre'] = 'mensaje'
            valor['href'] = '#'
            return valor
        def reg_busqueda(_id):
            valor = {}
            valor['nombre'] = 'busqueda'
            valor['href'] = '#'
            return valor
        def reg_calificacion_resena(_id):
            valor = {}
            valor['nombre'] = 'comentario'
            valor['href'] = '#'
            return valor
        def reg_seguidor(_id):
            valor = {}
            valor['nombre'] = 'seguidor'
            valor['href'] = '#'
            return valor
        def reg_descripcion(_id):
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
            valor['href'] = '#'
            return valor
        def reg_publicidad(_id):
            valor = {}
            valor['nombre'] = 'publicidad'
            tmp = DBSession.query(publicidad.nombre).\
            filter_by(rastreable_p = _id).one()
            valor['titulo'] = tmp[0] if (tmp is not None) else ""
            valor['href'] = '#'
            return valor
        def reg_estadisticas(_id):
            valor = {}
            valor['nombre'] = 'estadisticas'
            valor['href'] = '#'
            return valor
        def reg_factura(_id):
            valor = {}
            valor['nombre'] = 'factura'
            valor['href'] = '#'
            return valor
        
        por_defecto = {}
        por_defecto['nombre'] = por_defecto['titulo'] = ''
        por_defecto['href'] = '#'
        
        tipo_activo = self.tipo_de_rastreable(reg.actor_activo)
        activo = obtener_objeto(tipo_activo, reg.actor_activo) if (tipo_activo is not None) else por_defecto
        if 'foto' in activo:
            tmp = activo['foto'].filter(foto.ruta_de_foto.like('%miniaturas%')).first()
            activo['foto'] = tmp[0] if (tmp is not None) else ''
        else:
            activo['foto'] = ''
        
        tipo_pasivo = self.tipo_de_rastreable(reg.actor_pasivo)
        pasivo = obtener_objeto(tipo_pasivo, reg.actor_pasivo) if (tipo_pasivo is not None) else por_defecto
        if 'foto' in pasivo:
            tmp = pasivo['foto'].filter(foto.ruta_de_foto.like('%pequenas%')).first()
            pasivo['foto'] = tmp[0] if (tmp is not None) else ''
        else:
            pasivo['foto'] = ''
        
        entrada = {}
        entrada['actor_activo'] = activo
        entrada['actor_pasivo'] = pasivo
        entrada['accion'] = ACCION[reg.accion]
        
        entrada['columnas'] = reg.columna.split(',') if (reg.columna is not None) else '' 
        entrada['contenido'] = reg.valor.split(',') if (reg.valor is not None) else ''
        
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
    
    def tipo_de_rastreable(self, rastreable_id):
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
        return DBSession.query(territorio).filter_by(territorio_id = terr_id).one()
    
    def obtener_categoria(self, cat_id):
        return DBSession.query(categoria).filter_by(categoria_id = cat_id).one()
            
    def obtener_cliente(self, cli_id):
        return DBSession.query(cliente).filter_by(rif = cli_id).one()
    
    def obtener_cliente_padre(self, objeto, objeto_id):
        def cli_tienda():
            return DBSession.query(cliente).\
            join(tienda).\
            filter(tienda.tienda_id == objeto_id).one()
        def cli_patrocinante():
            return DBSession.query(cliente).\
            join(patrocinante).\
            filter(patrocinante.patrocinante_id == objeto_id).one()
        
        resultado = {
            'tienda': lambda: cli_tienda(), 
            'patrocinante': lambda: cli_patrocinante()
        }[objeto]()
        
        return resultado
    
    def obtener_tienda(self, tie_id):
        tmp = DBSession.query(tienda).filter_by(tienda_id = tie_id).first()
        return tmp if (tmp is not None) else {}
    
    def obtener_producto(self, pro_id):
        tmp = DBSession.query(producto).filter_by(producto_id = pro_id).first()
        return tmp if (tmp is not None) \
        else { 
        'codigo': 'no registrado', 
        'nombre': '', 
        'categoria': '0.0A.00.00.00.00' 
        }
        
    def sql_foto(self, objeto, objeto_id, tamano):
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
        
        sql = {
            'tienda': lambda: foto_tienda(), 
            'producto': lambda: foto_producto(), 
            'patrocinante': lambda: foto_patrocinante(), 
            'publicidad': lambda: foto_publicidad()
        }[objeto]()
        
        return sql
            
    def obtener_foto(self, objeto, objeto_id, tamano):
        por_defecto = {}
        por_defecto['ruta_de_foto'] = ''
        por_defecto['foto_id'] = por_defecto['describible'] = 0
        tmp = self.sql_foto(objeto, objeto_id, tamano).first()
        return tmp if (tmp is not None) else por_defecto
    
    def obtener_fotos(self, objeto, objeto_id, tamano):
        resultado = self.sql_foto(objeto, objeto_id, tamano)
        return resultado.all()