# -*- coding: utf-8 -*-
'''
Created on 08/04/2012

@author: nestor
'''

from spuria.orm import (
    Acceso,
    Accion,
    Administrador,
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
from paris.constantes import MENSAJE_DE_ERROR
from paris.formatos import formatear_objeto_teaser
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config
from sqlalchemy import and_, func
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import asc

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
    def __init__(self, peticion, *args, **kwargs):
        super(Comunes, self).__init__(*args, **kwargs)
        self.peticion = peticion
        self.pagina_actual = peticion.url
    
    """
    <PETICION>
    """
    
    @reify
    def peticion(self):
        return self.peticion

    @reify
    def pagina_actual(self):
        return self.pagina_actual
    
    @reify
    def categoria_id(self):
        return self.categoria_id
    
    @reify
    def categoria_base(self):
        return self.categoria_id.replace('.00', '')
    
    @reify
    def territorio_id(self):
        return self.territorio_id
    
    @reify
    def territorio_base(self):
        return self.territorio_id.replace('.00', '')
    
    """
    </PETICION>
    <TABLAS CONSTANTES>
    """
    
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
    
    """
    </TABLAS CONSTANTES>
    <FOTOS>
    """
    
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
    """
    </FOTOS>
    """

    @reify
    def territorios_hijos(self):
        try:
            if self.subtipo_de_peticion == 'tiendas':
                trr_sub = DBSession.query(Territorio).\
                join(Tienda).\
                filter(and_(
                    Tienda.categoria_id.contains(self.categoria_base),
                    Tienda.ubicacion_id.contains(self.territorio_base)
                )).subquery()
            elif self.subtipo_de_peticion == 'productos':
                trr_sub = DBSession.query(Territorio).\
                join(Tienda).\
                join(Inventario).\
                join(Producto).\
                filter(and_(
                    Producto.categoria_id.contains(self.categoria_base),
                    Tienda.ubicacion_id.contains(self.territorio_base)
                )).subquery()
        except AttributeError:
            if self.tipo_de_peticion == 'producto':
                trr_sub = DBSession.query(Territorio).\
                join(Tienda).\
                join(Inventario).\
                join(Producto).\
                filter(and_(
                    Producto.producto_id == self.producto_id,
                    Tienda.ubicacion_id.contains(self.territorio_base)
                )).subquery()

        trr = aliased(Territorio, trr_sub)
        
        territorios = DBSession.query(Territorio).\
        filter(and_(
            Territorio.territorio_padre_id == self.territorio_id,
            Territorio.territorio_padre_id != Territorio.territorio_id,
            trr.territorio_id.contains(
                func.replace(Territorio.territorio_id, '.00', '')
            )
        )).all()
        
        return territorios
    
    @reify
    def ruta_territorio_actual(self):
        return self.obtener_ruta_territorio(
            self.obtener_territorio(self.territorio_id), 1, True
        )
        
    @reify
    def categorias_hijas(self):
        try:
            if self.subtipo_de_peticion == 'tiendas':
                cat_sub = DBSession.query(Categoria).\
                join(Tienda).\
                filter(and_(
                    Tienda.categoria_id.contains(self.categoria_base),
                    Tienda.ubicacion_id.contains(self.territorio_base)
                )).subquery()
            elif self.subtipo_de_peticion == 'productos':
                cat_sub = DBSession.query(Categoria).\
                join(Producto).\
                join(Inventario).\
                join(Tienda).\
                filter(and_(
                    Producto.categoria_id.contains(self.categoria_base),
                    Tienda.ubicacion_id.contains(self.territorio_base)
                )).subquery()
        except AttributeError:
            if self.tipo_de_peticion == 'tienda':
                cat_sub = DBSession.query(Categoria).\
                join(Producto).\
                join(Inventario).\
                join(Tienda).\
                filter(and_(
                    Producto.categoria_id.contains(self.categoria_base),
                    Tienda.tienda_id == self.tienda_id
                )).subquery()
                
        cat = aliased(Categoria, cat_sub)
        categorias = DBSession.query(Categoria).\
        filter(and_(
            Categoria.hijo_de_categoria == self.categoria_id,
            Categoria.hijo_de_categoria != Categoria.categoria_id,
            cat.categoria_id.contains(
                func.replace(Categoria.categoria_id, '.00', '')
            )
        )).all()

        return categorias
    
    @reify
    def ruta_categoria_actual(self):
        return self.obtener_ruta_categoria(
            self.obtener_categoria(self.categoria_id), 1, True
        )

    def obtener_foto(self, objeto, objeto_id, tamano):
        return sql_foto(objeto, objeto_id, tamano).first()
    
    def obtener_fotos(self, objeto, objeto_id, tamano):
        return sql_foto(objeto, objeto_id, tamano).all()
    
    def obtener_ruta_territorio(self, territorio, nivel_tope, invertir):
        ruta = []
        
        while True:
            ruta.append(territorio)
            
            if (territorio.territorio_padre == territorio.territorio_id) \
            or (territorio.territorio_padre == None) \
            or (territorio.nivel == nivel_tope):
                break
            else:
                territorio = territorio.territorio_padre
        
        if invertir:
            ruta.reverse()
        
        return ruta
    
    def obtener_ruta_categoria(self, categoria, nivel_tope, invertir):
        ruta = []
        
        while True:
            ruta.append(categoria)
            if (categoria.hijo_de_categoria == categoria.categoria_id) \
            or (categoria.hijo_de_categoria == None) \
            or (categoria.nivel == nivel_tope):
                break
            else:
                categoria = categoria.padre
        
        if invertir:
            ruta.reverse()
        
        return ruta
        
    def obtener_territorio(self, terr_id):
        return DBSession.query(Territorio).filter_by(territorio_id = terr_id).\
        first()
    
    def obtener_categoria(self, cat_id):
        return DBSession.query(Categoria).filter_by(categoria_id = cat_id).\
        first()
    """
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
    """
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
    
    def obtener_administrador(self, objeto, objeto_id):
        def adm_id(_id):
            return DBSession.query(Administrador).filter_by(
                administrador_id = _id
            ).first()
        def adm_correo(correo):
            return DBSession.query(Administrador).\
            join(Acceso).\
            filter(Acceso.correo_electronico == correo).first()
    
        tmp = {
            'id': lambda x: adm_id(x), 
            'correo_electronico': lambda x: adm_correo(x)
        }[objeto](objeto_id)
        
        return tmp
    
    def obtener_consumidor(self, objeto, objeto_id):
        def con_id(_id):
            return DBSession.query(Consumidor).filter_by(consumidor_id = _id).\
            first()
        def con_correo(correo):
            return DBSession.query(Consumidor).\
            join(Acceso).\
            filter(Acceso.correo_electronico == correo).first()
    
        tmp = {
            'id': lambda x: con_id(x), 
            'correo_electronico': lambda x: con_correo(x)
        }[objeto](objeto_id)
        
        return tmp
    
    def obtener_inventario(self, tie_id, cod):
        return DBSession.query(Inventario).filter(and_(
            Inventario.tienda_id == tie_id,
            Inventario.codigo == cod
        )).first()

    def obtener_croquis(self, cro_id):
        return DBSession.query(Croquis).filter_by(croquis_id=cro_id).first()

    def obtener_mensaje(self, men_id):
        return DBSession.query(Mensaje).filter_by(mensaje_id=men_id).first()
    
    def obtener_busqueda(self, bus_id):
        return DBSession.query(Busqueda).filter_by(busqueda_id=bus_id).first()
    
    def obtener_calificacion_resena(self, cal_id, con_id):
        return DBSession.query(CalificacionResena).filter(and_(
            CalificacionResena.calificable_seguible==cal_id,
            CalificacionResena.consumidor_id==con_id
        )).first()
    
    def obtener_seguimiento(self, cal_id, con_id):
        return DBSession.query(Seguimiento).filter(and_(
            Seguimiento.calificable_seguible==cal_id,
            Seguimiento.consumidor_id==con_id
        )).first()
        
    def obtener_descripcion(self, des_id):
        return DBSession.query(Descripcion).filter_by(descripcion_id=des_id).\
        first()
        
    def obtener_publicidad(self, pub_id):
        return DBSession.query(Publicidad).filter_by(publicidad_id=pub_id).\
        first()
        
    def obtener_estadisticas(self, est_id):
        return DBSession.query(Estadisticas).filter_by(estadisticas_id=est_id).\
        first()
        
    def obtener_factura(self, fac_id):
        return DBSession.query(Factura).filter_by(factura_id=fac_id).first()
        
    @view_config(route_name="territorio_coordenadas", renderer="json")
    def territorio_coordenadas_view(self):
        self.territorio_id = self.peticion.matchdict['territorio_id']
        self.nivel = self.peticion.matchdict['nivel']
        
        nivel_terr = DBSession.query(Territorio.nivel).\
        filter_by(territorio_id = self.territorio_id).first()[0]
        
        if nivel_terr + int(self.nivel) < 0:
            return HTTPNotFound(MENSAJE_DE_ERROR)

        terrs = DBSession.query(Territorio).\
        filter(and_(
            Territorio.nivel == nivel_terr + int(self.nivel),
            Territorio.territorio_id.contains(self.territorio_base)
        )).all()
        
        resultado = []
        for terr in terrs:
            poligonos = []
            for crq in terr.dibujable.croquis:
                poligono = ''
                for pto in crq.puntos:
                    poligono += "{0}:{1} ".format(
                        str(pto.latitud), str(pto.longitud)
                    )
                poligonos.append(poligono.strip(' '))
            resultado.append({
                'nombre': terr.nombre,
                'id': terr.territorio_id,
                'poligonos': poligonos
            })

        return { 'territorios': resultado }

    @view_config(route_name="objeto_teaser", renderer="json")
    def objeto_teaser_view(self):
        self.objeto_tipo = self.peticion.matchdict['objeto_tipo']
        self.objeto_id = self.peticion.matchdict['objeto_id']
        
        objeto = {
            'tienda': lambda x: self.obtener_tienda(x),
            'patrocinante': lambda x: self.obtener_patrocinante(x),
            'administrador': lambda x: self.obtener_administrador('id', x),
            'consumidor': lambda x: self.obtener_consumidor('id', x),
            'usuario': lambda x: self.obtener_usuario('id', x),
            'inventario': lambda x: self.obtener_inventario(
                x.split(':')[0], x.split(':')[1]
            ),
            'croquis': lambda x: self.obtener_croquis(x),
            'producto': lambda x: self.obtener_producto(x),
            'mensaje': lambda x: self.obtener_mensaje(x),
            'busqueda': lambda x: self.obtener_busqueda(x),
            'calificacion_resena': lambda x: self.obtener_calificacion_resena(
                x.split(':')[0], x.split(':')[1]
            ),
            'seguimiento': lambda x: self.obtener_seguimiento(
                x.split(':')[0], x.split(':')[1]
            ),
            'descripcion': lambda x: self.obtener_descripcion(x),
            'publicidad': lambda x: self.obtener_publicidad(x),
            'estadisticas': lambda x: self.obtener_estadisticas(x),
            'factura': lambda x: self.obtener_factura(x)
        }[self.objeto_tipo](self.objeto_id)
        
        return formatear_objeto_teaser(objeto)