from .models import (
	calificable_seguible,
	calificacion_resena,
	categoria,
	cliente,
	consumidor,
	DBSession,
	describible,
	descripcion,	
	estado, 
	foto,
	horario_de_trabajo,
	inventario_reciente,
	municipio, 
	parroquia,
	patrocinante,
	producto,
	publicidad,
	rastreable,
	region_geografica,
	tamano_reciente,
	tienda,
	turno,
	usuario
)
from diagramas import diagramas
from pyramid.decorator import reify
from pyramid.httpexceptions import (HTTPNotFound)
from pyramid.view import view_config
from sqlalchemy import and_
import string, random

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
		pass
	
	def obtener_cliente(self):
		def cli_tienda():
			return DBSession.query(cliente).join(tienda).filter(tienda.tienda_id == self.peticion_id).first()
		def cli_patrocinante():
			return DBSession.query(cliente).join(patrocinante).filter(patrocinante.patrocinante_id == self.peticion_id).first()
		resultado = ({'tienda': lambda: cli_tienda(), 'patrocinante': lambda: cli_patrocinante()}[self.tipo_de_peticion])()
		return resultado
	
	@reify
	def peticion(self):
		return self.peticion
	
	# Esta verga hay que quitarla...
	@reify
	def categorias(self):
		return DBSession.query(categoria).all()		 
	
	@reify
	def inventario_reciente(self):
		def inv_tienda():
			return DBSession.query(inventario_reciente).filter_by(tienda_id = self.peticion_id).all()
		def inv_producto():
			return DBSession.query(inventario_reciente).filter_by(producto_id = self.peticion_id).all()
		
		var_inventario = ({'tienda': lambda: inv_tienda(), 'producto': lambda: inv_producto()}[self.tipo_de_peticion])()
		resultado = [{""}] if (var_inventario is None) else var_inventario
		return resultado

	@reify
	def cliente(self):
		resultado = self.obtener_cliente()
		return {""} if (resultado is None) else resultado		 

	@reify
	def region_geografica(self):
		var_cliente = self.obtener_cliente()
		
		if var_cliente is not None:
			var_parroquia = DBSession.query(parroquia).join(usuario).filter(usuario.usuario_id == var_cliente.usuario_p).first()
			var_municipio = DBSession.query(municipio).filter_by(municipio_id = parroquia.municipio).first()
			var_estado = DBSession.query(estado).filter_by(estado_id = municipio.estado).first()
			
			reg_geo_parroquia = DBSession.query(region_geografica).filter_by(region_geografica_id = var_parroquia.region_geografica_p).first()
			reg_geo_municipio = DBSession.query(region_geografica).filter_by(region_geografica_id = var_municipio.region_geografica_p).first()
			reg_geo_estado = DBSession.query(region_geografica).filter_by(region_geografica_id = var_estado.region_geografica_p).first()

			resultado = {'parroquia': reg_geo_parroquia.nombre, 'municipio': reg_geo_municipio.nombre, 'estado': reg_geo_estado.nombre }
		else:
			resultado = {'parroquia': 'N/D', 'municipio': 'N/D', 'estado': 'N/D' }
			
		return resultado
		
	@reify
	def descripciones(self):
		def desc_tienda():
			return DBSession.query(descripcion).join(describible).join(cliente).join(tienda).filter(tienda.tienda_id == self.peticion_id).all()
		def desc_producto():
			return DBSession.query(descripcion).join(describible).join(producto).filter(producto.producto_id == self.peticion_id).all()
		def desc_patrocinante():
			return DBSession.query(descripcion).join(describible).join(cliente).join(patrocinante).filter(patrocinante.patrocinante_id == self.peticion_id).all()
		
		var_descripciones = ({'tienda': lambda: desc_tienda(), 'producto': lambda: desc_producto(), 'patrocinante': lambda: desc_patrocinante()}[self.tipo_de_peticion])()
		resultado = [ {'contenido': ""} ] if var_descripciones is None else var_descripciones
		return resultado
	
	@reify
	def horarios(self):
		if self.tipo_de_peticion == 'tienda':
			var_horario = DBSession.query(horario_de_trabajo).filter_by(tienda_id = self.peticion_id).all()
		
		if var_horario is not None:
			resultado = list()
			for jornada in var_horario:
				horario = {}
				horario['dia'] = jornada.dia
				horario['laborable'] = jornada.laborable
				turnos = DBSession.query(turno).filter(and_(turno.tienda_id == self.peticion_id, turno.dia == jornada.dia)).all()
				horario['turnos'] = string.join(["{0.hora_de_apertura} - {0.hora_de_cierre} ".format(t) for t in turnos])
				resultado.append(horario)
		else:
			resultado = [{""}]

		return resultado
	
	@reify
	def tamano_reciente(self):
		if self.tipo_de_peticion == 'tienda':
			var_tamano = DBSession.query(tamano_reciente).filter(tamano_reciente.tienda_id == self.peticion_id).first()
		resultado = {'numero_total_de_productos': 'ND', 'cantidad_total_de_productos': 'ND', 'valor': 'ND'} if (var_tamano is None) else var_tamano
		return resultado
	
	@reify
	def foto(self):
		def foto_tienda():
			return DBSession.query(foto).join(describible).join(cliente).join(tienda).filter(tienda.tienda_id == self.peticion_id).first()
		def foto_producto():
			return DBSession.query(foto).join(describible).join(producto).filter(producto.producto_id == self.peticion_id).first()
		def foto_patrocinante():
			return DBSession.query(foto).join(describible).join(cliente).join(patrocinante).filter(patrocinante.patrocinante_id == self.peticion_id).first()
		def foto_publicidad():
			return DBSession.query(foto).join(describible).join(publicidad).filter(publicidad.publicidad_id == self.peticion_id).first()
		
		var_foto = ({'tienda': lambda: foto_tienda(), 'producto': lambda: foto_producto(), 'patrocinante': lambda: foto_patrocinante(), 'publicidad': lambda: foto_publicidad()}[self.tipo_de_peticion])()
		resultado = {'ruta_de_foto': ''} if (var_foto is None) else var_foto
		
		return resultado
	
	@reify
	def comentarios(self):
		def cal_producto():
			return DBSession.query(calificacion_resena).join(calificable_seguible).join(producto).filter(producto.producto_id == self.peticion_id).all()
		def cal_tienda():
			return DBSession.query(calificacion_resena).join(calificable_seguible).join(tienda).filter(tienda.tienda_id == self.peticion_id).all()
		
		resultado = {}
		var_comentarios = ({'tienda': lambda: cal_tienda(), 'producto': lambda: cal_producto()}[self.tipo_de_peticion])()
		
		if var_comentarios is not None:
			resultado = list()
			for comentario in var_comentarios:
				tmp = {}
				tmp['calificacion'] = comentario.calificacion
				tmp['resena'] = comentario.resena
				fecha_decimal = DBSession.query(rastreable).filter_by(rastreable_id = comentario.rastreable_p).first().fecha_de_creacion
				fecha = str(fecha_decimal) + ''
				tmp['fecha'] = "{0}/{1}/{2} {3}:{4}".format(fecha[6:8], fecha[4:6], fecha[0:4], fecha[8:10], fecha[10:12])
				tmp['consumidor'] = DBSession.query(consumidor).filter_by(consumidor_id = comentario.consumidor_id).first()
				resultado.append(tmp)
		else:
			resultado = [{""}]
				
		return resultado
	
	@view_config(route_name="aleatorio", renderer="json")
	def updates_view(self):
		return random.randint(1, 100)
	
	@view_config(route_name='inicio', renderer='plantillas/inicio.pt')
	def inicio_view(self):
		return {'nombre_pagina': 'Inicio'}
	
	@view_config(route_name='producto', renderer='plantillas/producto.pt')
	def producto_view(self):
		if self.tipo_de_peticion == 'producto':
			var_producto = DBSession.query(producto).filter_by(producto_id = self.peticion_id).first()
		resultado = HTTPNotFound(MENSAJE_DE_ERROR) if (var_producto is None) else {'nombre_pagina': 'Producto', 'producto': var_producto}
		return resultado
	
	@view_config(route_name='tienda', renderer='plantillas/tienda.pt')
	def tienda_view(self):
		if self.tipo_de_peticion == 'tienda':
			var_tienda = DBSession.query(tienda).filter_by(tienda_id = self.peticion_id).first()
		resultado = HTTPNotFound(MENSAJE_DE_ERROR) if (var_tienda is None) else {'nombre_pagina': 'Tienda', 'tienda': var_tienda}
		return resultado

	@view_config(route_name='listado_productos', renderer='plantillas/listado.pt')
	def listado_productos_view(self):
		productos = DBSession.query(producto).all()
		return {'nombre_pagina': 'Productos', 'lista': productos}
	
	@view_config(route_name='listado_tiendas', renderer='plantillas/listado.pt')
	def listado_tiendas_view(self):
		clientes = DBSession.query(cliente).join(tienda).all()
		return {'nombre_pagina': 'Tiendas', 'lista': clientes}
		
	@view_config(route_name='inventario_producto', renderer='plantillas/inventario.pt')
	def inventario_producto_view(self):
		return { 'nombre_pagina': 'Inventario', 'tipo': 'producto_id' }
		
	@view_config(route_name='inventario_tienda', renderer='plantillas/inventario.pt')
	def inventario_tienda_view(self):
		return { 'nombre_pagina': 'Inventario', 'tipo': 'tienda_id' }