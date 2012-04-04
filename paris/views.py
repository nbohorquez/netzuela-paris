from .models import (
	calificable_seguible,
	calificacion_resena,
	categoria,
	cliente,
	consumidor,
	croquis,
	DBSession,
	describible,
	descripcion,
	dibujable,	
	foto,
	horario_de_trabajo,
	inventario_reciente,
	patrocinante,
	producto,
	publicidad,
	punto,
	punto_de_croquis,
	rastreable,
	tamano_reciente,
	territorio,
	tienda,
	turno,
	usuario
)
from diagramas import diagramas
from pyramid.decorator import reify
from pyramid.httpexceptions import (HTTPNotFound)
from pyramid.view import view_config
from sqlalchemy import and_
from sqlalchemy.orm import aliased
import string

MENSAJE_DE_ERROR = 'Vos lo que estais es loco! Esa verga no existe'

# Aptana siempre va a decir que las clases de Spuria (Tienda, Producto, etc) no estan 
# definidas explicitamente en ninguna parte. Lo que ocurre es que yo las cargo de forma 
# dinamica cuando inicia la aplicacion.

class paris_views(diagramas):
	def __init__(self, peticion):
		self.peticion = peticion
		if 'tienda_id' in self.peticion.matchdict:
			self.peticion_id = self.peticion.matchdict['tienda_id']
			self.tipo_de_peticion = 'tienda'
		elif 'producto_id' in self.peticion.matchdict:
			self.peticion_id = self.peticion.matchdict['producto_id']
			self.tipo_de_peticion = 'producto'
		elif 'patrocinante_id' in self.peticion.matchdict:
			self.peticion_id = self.peticion.matchdict['patrocinante_id']
			self.tipo_de_peticion = 'patrocinante'
		elif 'categoria_id' in self.peticion.matchdict and 'territorio_id' in self.peticion.matchdict:
			self.categoria_id = self.peticion.matchdict['categoria_id']
			self.territorio_id = self.peticion.matchdict['territorio_id']
			self.tipo_de_peticion = 'listado'
	
	@reify
	def peticion(self):
		return self.peticion
	
	@reify
	def peticion_id(self):
		return self.peticion_id if self.tipo_de_peticion != 'listado' else None
	
	@reify
	def categoria_id(self):
		return self.categoria_id if self.tipo_de_peticion == 'listado' else None
	
	@reify
	def territorio_id(self):
		return self.territorio_id if self.tipo_de_peticion == 'listado' else None
	
	@reify
	def tipo_de_peticion(self):
		return self.tipo_de_peticion
	
	@reify
	def inventario_reciente(self):
		def inv_tienda():
			return DBSession.query(inventario_reciente).\
			filter_by(tienda_id = self.peticion_id).all()
		def inv_producto():
			return DBSession.query(inventario_reciente).\
			filter_by(producto_id = self.peticion_id).all()
		
		var_inventario = {
			'tienda': lambda: inv_tienda(), 
			'producto': lambda: inv_producto()
		}[self.tipo_de_peticion]()
		
		resultado = [{""}] if (var_inventario is None) else var_inventario
		return resultado

	@reify
	def cliente_padre(self):
		resultado = self.obtener_cliente_padre(self.tipo_de_peticion, self.peticion_id)
		return {""} if (resultado is None) else resultado	 

	@reify
	def direccion(self):
		var_cliente = self.obtener_cliente_padre(self.tipo_de_peticion, self.peticion_id)
		
		if var_cliente is not None:
			padre = aliased(territorio)
			hijo = aliased(territorio)
			
			p = DBSession.query(territorio).\
			join(usuario).\
			filter_by(usuario_id = var_cliente.usuario_p).one()
			
			m = DBSession.query(padre).\
			join(hijo, padre.territorio_id == hijo.territorio_padre).\
			filter_by(territorio_id = p.territorio_id).one()
			
			e = DBSession.query(padre).\
			join(hijo, padre.territorio_id == hijo.territorio_padre).\
			filter_by(territorio_id = m.territorio_id).one()
			
			resultado = {
				'parroquia': p.nombre, 
				'municipio': m.nombre, 
				'estado': e.nombre 
			}
		else:
			resultado = {'parroquia': 'N/D', 'municipio': 'N/D', 'estado': 'N/D' }
			
		return resultado
		
	@reify
	def descripciones(self):
		def desc_tienda():
			return DBSession.query(descripcion).\
			join(describible).\
			join(cliente).\
			join(tienda).\
			filter(tienda.tienda_id == self.peticion_id).all()
		def desc_producto():
			return DBSession.query(descripcion).\
			join(describible).\
			join(producto).\
			filter(producto.producto_id == self.peticion_id).all()
		def desc_patrocinante():
			return DBSession.query(descripcion).\
			join(describible).\
			join(cliente).\
			join(patrocinante).\
			filter(patrocinante.patrocinante_id == self.peticion_id).all()
		
		var_descripciones = {
			'tienda': lambda: desc_tienda(), 
			'producto': lambda: desc_producto(), 
			'patrocinante': lambda: desc_patrocinante()
		}[self.tipo_de_peticion]()
		
		resultado = [ {'contenido': ""} ] if var_descripciones is None else var_descripciones
		return resultado
	
	@reify
	def horarios(self):
		if self.tipo_de_peticion == 'tienda':
			var_horario = DBSession.query(horario_de_trabajo).\
			filter_by(tienda_id = self.peticion_id).all()
		
		if var_horario is not None:
			resultado = []
			for jornada in var_horario:
				horario = {}
				horario['dia'] = jornada.dia
				horario['laborable'] = jornada.laborable
				turnos = DBSession.query(turno).\
				filter(and_(turno.tienda_id == self.peticion_id, turno.dia == jornada.dia)).all()
				horario['turnos'] = string.join(["{0.hora_de_apertura} - {0.hora_de_cierre} ".format(t) for t in turnos])
				resultado.append(horario)
		else:
			resultado = [{""}]

		return resultado
	
	@reify
	def tamano_reciente(self):
		if self.tipo_de_peticion == 'tienda':
			var_tamano = DBSession.query(tamano_reciente).\
			filter(tamano_reciente.tienda_id == self.peticion_id).one()
		
		resultado = {
			'numero_total_de_productos': 'ND', 
			'cantidad_total_de_productos': 'ND', 
			'valor': 'ND'
		} if (var_tamano is None) else var_tamano
		
		return resultado
	
	@reify
	def fotos_grandes(self):
		var_fotos = self.obtener_fotos(self.tipo_de_peticion, self.peticion_id, 'grandes')
		resultado = [{'ruta_de_foto': ''}] if (var_fotos is None) else var_fotos
		return resultado
	
	@reify
	def fotos_medianas(self):
		var_fotos = self.obtener_fotos(self.tipo_de_peticion, self.peticion_id, 'medianas')
		resultado = [{'ruta_de_foto': ''}] if (var_fotos is None) else var_fotos
		return resultado
	
	@reify
	def fotos_pequenas(self):
		var_fotos = self.obtener_fotos(self.tipo_de_peticion, self.peticion_id, 'pequenas')
		resultado = [{'ruta_de_foto': ''}] if (var_fotos is None) else var_fotos
		return resultado
	
	@reify
	def calificaciones_resenas(self):
		def cal_producto():
			return DBSession.query(calificacion_resena).\
			join(calificable_seguible).\
			join(producto).\
			filter(producto.producto_id == self.peticion_id).all()
		def cal_tienda():
			return DBSession.query(calificacion_resena).\
			join(calificable_seguible).join(tienda).\
			filter(tienda.tienda_id == self.peticion_id).all()
		
		var_comentarios = {
			'tienda': lambda: cal_tienda(), 
			'producto': lambda: cal_producto()
		}[self.tipo_de_peticion]()
		
		if var_comentarios is not None:
			resultado = []
			for comentario in var_comentarios:
				tmp = {}
				tmp['calificacion'] = comentario.calificacion
				tmp['resena'] = comentario.resena
				
				fecha_decimal = DBSession.query(rastreable).\
				filter_by(rastreable_id = comentario.rastreable_p).one().fecha_de_creacion
				
				fecha = str(fecha_decimal)
				tmp['fecha'] = "{0}/{1}/{2} {3}:{4}".format(fecha[6:8], fecha[4:6], fecha[0:4], fecha[8:10], fecha[10:12])
				
				tmp['consumidor'] = DBSession.query(consumidor).\
				filter_by(consumidor_id = comentario.consumidor_id).one()
				
				resultado.append(tmp)
		else:
			resultado = [{""}]
				
		return resultado
	
	@reify
	def territorios_hijos(self):
		if self.tipo_de_peticion == 'listado':
			resultado = DBSession.query(territorio).\
			filter_by(territorio_padre = self.territorio_id).all()
		else:
			resultado = None
		return resultado

	@reify
	def ruta_territorio_actual(self):
		def reg_listado():
			return self.territorio_id
		
		terr_id = {
			'listado': lambda: reg_listado(), 
		}[self.tipo_de_peticion]()
		
		return self.obtener_ruta_territorio(terr_id)
	
	@reify
	def categorias_hijas(self):
		def cat_listado():
			return DBSession.query(categoria).\
			filter(and_(
				categoria.hijo_de_categoria == self.categoria_id, 
				categoria.categoria_id != categoria.hijo_de_categoria)
			).all()
		
		cats = {
			'listado': lambda: cat_listado()
		}[self.tipo_de_peticion]()
		
		return cats

	@reify
	def ruta_categoria_actual(self):
		def cat_producto():
			return DBSession.query(producto.categoria).\
			filter_by(producto_id = self.peticion_id).one()[0]
		def cat_tienda():
			return DBSession.query(cliente.categoria).\
			join(tienda).\
			filter(tienda.tienda_id == self.peticion_id).one()[0]
		def cat_patrocinante():
			return DBSession.query(cliente.categoria).\
			join(patrocinante).\
			filter(patrocinante.patrocinante_id == self.peticion_id).one()[0]
		def cat_listado():
			return self.categoria_id
		
		cat_padre = {
			'producto': lambda: cat_producto(), 
			'tienda': lambda: cat_tienda(), 
			'patrocinante': lambda: cat_patrocinante(), 
			'listado': lambda: cat_listado()
		}[self.tipo_de_peticion]()
		
		return self.obtener_ruta_categoria(cat_padre)
	
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
			cat = DBSession.query(categoria).filter_by(categoria_id = cat_id).one()
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
	
	@view_config(route_name='inicio', renderer='plantillas/inicio.pt')
	def inicio_view(self):
		return {'nombre_pagina': 'Inicio'}
	
	@view_config(route_name='producto', renderer='plantillas/producto.pt')
	def producto_view(self):
		if self.tipo_de_peticion == 'producto':
			var_producto = DBSession.query(producto).filter_by(producto_id = self.peticion_id).one()
		resultado = HTTPNotFound(MENSAJE_DE_ERROR) if (var_producto is None) else {'pagina': 'Producto', 'producto': var_producto}
		return resultado
	
	@view_config(route_name='tienda', renderer='plantillas/tienda.pt')
	def tienda_view(self):
		if self.tipo_de_peticion == 'tienda':
			var_tienda = DBSession.query(tienda).filter_by(tienda_id = self.peticion_id).one()
		resultado = HTTPNotFound(MENSAJE_DE_ERROR) if (var_tienda is None) else {'pagina': 'Tienda', 'tienda': var_tienda}
		return resultado

	@view_config(route_name='productos', renderer='plantillas/listado.pt')
	def listado_productos_view(self):
		i = aliased(inventario_reciente)
		p = aliased(producto)
		t = aliased(tienda)
		c = aliased(cliente)
		u = aliased(usuario)
		
		# Este metodo me permite saber rapidamente si una
		# categoria o territorio es hijo de otro(a).
		cat = self.categoria_id.replace('.00', '')
		terr = self.territorio_id.replace('.00', '')
				
		productos = DBSession.query(i).\
		join(p, i.producto_id == p.producto_id).\
		join(t, i.tienda_id == t.tienda_id).\
		join(c, t.cliente_p == c.rif).\
		join(u, c.usuario_p == u.usuario_id).\
		filter(and_(
			p.categoria.contains(cat),
			u.ubicacion.contains(terr)
		)).all()
		
		return {'pagina': 'Productos', 'lista': productos}
	
	@view_config(route_name='tiendas', renderer='plantillas/listado.pt')
	def listado_tiendas_view(self):
		t = aliased(tienda)
		c = aliased(cliente)
		u = aliased(usuario)
		
		cat = self.categoria_id.replace('.00', '')
		terr = self.territorio_id.replace('.00', '')
		
		tiendas = DBSession.query(t).\
		join(c, t.cliente_p == c.rif).\
		join(u, c.usuario_p == u.usuario_id).\
		filter(and_(
			c.categoria.contains(cat),
			u.ubicacion.contains(terr)
		)).all()

		return {'pagina': 'Tiendas', 'lista': tiendas}
		
	@view_config(route_name='inventario_producto', renderer='plantillas/inventario.pt')
	def inventario_producto_view(self):
		return { 'pagina': 'Inventario', 'tipo': 'producto_id' }
		
	@view_config(route_name='inventario_tienda', renderer='plantillas/inventario.pt')
	def inventario_tienda_view(self):
		return { 'pagina': 'Inventario', 'tipo': 'tienda_id' }
	
	@view_config(route_name="tienda_turno", renderer="json")
	def tienda_turno_view(self):
		var_dia = self.peticion.params['dia']
		var_tienda = self.peticion.params['tienda_id']
		
		apertura, cierre = DBSession.query(turno.hora_de_apertura, turno.hora_de_cierre).\
		filter(and_(
			turno.tienda_id == var_tienda, 
			turno.dia == var_dia)
		).one()
		
		return { 'apertura': "{0}".format(str(apertura)), 'cierre': "{0}".format(str(cierre)) } 
		
	@view_config(route_name="tienda_coordenadas", renderer="json")
	def tienda_coordenadas_view(self):
		var_tienda = self.peticion.params['tienda_id']
		
		latitud, longitud = DBSession.query(punto.latitud, punto.longitud).\
		join(punto_de_croquis).\
		join(croquis).\
		join(dibujable).\
		join(tienda).\
		filter_by(tienda_id = var_tienda).one()
		
		return { 'latitud': "{0}".format(str(latitud)), 'longitud': "{0}".format(str(longitud)) }
	"""
	@view_config(route_name="categorias", renderer="json")
	def categorias_view(self):
		var_categoria = self.peticion.params['categoria_id']
		var_categorias = DBSession.query(categoria).filter_by(hijo_de_categoria = var_categoria).all()
		resultado = []
		
		for cat in var_categorias:
			info = {}
			info['categoria_id'] = cat.categoria_id
			info['nombre'] = cat.nombre
			resultado.append(info)
			
		return { 'categorias': resultado }
	"""