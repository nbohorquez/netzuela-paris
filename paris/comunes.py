'''
Created on 08/04/2012

@author: nestor
'''

from .models import (
    categoria,
    cliente,
    consumidor,
    DBSession,
    describible,
    foto,
    patrocinante,
    producto,
    publicidad,
    rastreable,
    territorio,
    tienda,
    usuario
)
from sqlalchemy import and_

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
    
    def formatear_entrada_registro(self, reg):
        entrada = {}
        entrada['actor_activo'] = reg.actor_activo
        entrada['actor_pasivo'] = reg.actor_pasivo 
        entrada['accion'] = reg.accion 
        entrada['parametros'] = reg.parametros
        entrada['codigo_de_error'] = reg.codigo_de_error 
        fecha = str(reg.fecha_hora)
        entrada['fecha_hora'] = "{0}/{1}/{2} {3}:{4}".format(fecha[6:8], fecha[4:6], fecha[0:4], fecha[8:10], fecha[10:12])
        return entrada

                
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
        return DBSession.query(tienda).filter_by(tienda_id = tie_id).one()
    
    def obtener_producto(self, pro_id):
        return DBSession.query(producto).filter_by(producto_id = pro_id).one()
        
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
        resultado = self.sql_foto(objeto, objeto_id, tamano)
        return resultado.first()
    
    def obtener_fotos(self, objeto, objeto_id, tamano):
        resultado = self.sql_foto(objeto, objeto_id, tamano)
        return resultado.all()