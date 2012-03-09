from .models import (
	DBSession, 
	Tienda, 
	Producto, 
	Cliente, 
	InventarioReciente, 
	Categoria,
	Patrocinante
)
from diagramas import Diagramas
from pyramid.decorator import reify
from pyramid.httpexceptions import (HTTPNotFound)
from pyramid.view import view_config

MENSAJE_DE_ERROR = 'Vos lo que estais es loco! Esa verga no existe'

# Aptana siempre va a decir que las clases de Spuria (Tienda, Producto, etc) no estan 
# definidas explicitamente en ninguna parte. Lo que ocurre es que yo las cargo de forma 
# dinamica cuando inicia la aplicacion.

class ParisViews(Diagramas):
	def __init__(self, peticion):
		self.peticion = peticion
		pass
	
	@reify
	def peticion(self):
		peticion = self.peticion
		return peticion
	
	# Esta verga hay que quitarla...
	@reify
	def categorias(self):
		categorias = DBSession.query(Categoria).all()
		return categorias
	
	@reify
	def inventario(self):
		if 'tienda_id' in self.peticion.matchdict:
			tienda_id = self.peticion.matchdict['tienda_id']
			inventario = DBSession.query(InventarioReciente).filter_by(TiendaID = tienda_id).all()
		elif 'producto_id' in self.peticion.matchdict:
			producto_id = self.peticion.matchdict['producto_id']
			inventario = DBSession.query(InventarioReciente).filter_by(ProductoID = producto_id).all()
	
		resultado = HTTPNotFound(MENSAJE_DE_ERROR) if (inventario is None) else inventario
		return resultado

	@reify
	def cliente(self):
		if 'tienda_id' in self.peticion.matchdict:
			tienda_id = self.peticion.matchdict['tienda_id']
			cliente = DBSession.query(Cliente).join(Tienda).filter(Tienda.TiendaID == tienda_id).first()
		elif 'patrocinante_id' in self.peticion.matchdict:
			patrocinante_id = self.peticion.matchdict['patrocinante_id']
			cliente = DBSession.query(Cliente).join(Patrocinante).filter(Patrocinante.PatrocinanteID == patrocinante_id).first()
		
		resultado = HTTPNotFound(MENSAJE_DE_ERROR) if (cliente is None) else cliente
		return resultado

	@view_config(route_name='inicio', renderer='plantillas/inicio.pt')
	def inicio_view(self):
		return {'nombre_pagina': 'Inicio'}
	
	@view_config(route_name='producto', renderer='plantillas/producto.pt')
	def producto_view(self):
		producto_id = self.peticion.matchdict['producto_id']
		producto = DBSession.query(Producto).filter_by(ProductoID = producto_id).first()
		
		resultado = HTTPNotFound(MENSAJE_DE_ERROR) if (producto is None) else {'nombre_pagina': 'Producto', 'producto': producto} 
		return resultado
	
	@view_config(route_name='tienda', renderer='plantillas/tienda.pt')
	def tienda_view(self):
		tienda_id = self.peticion.matchdict['tienda_id']
		tienda = DBSession.query(Tienda).filter_by(TiendaID = tienda_id).first()
		
		resultado = HTTPNotFound(MENSAJE_DE_ERROR) if (tienda is None) else {'nombre_pagina': 'Tienda', 'tienda': tienda} 
		return resultado

	@view_config(route_name='listado_productos', renderer='plantillas/listado.pt')
	def listado_productos_view(self):
		productos = DBSession.query(Producto).all()
		return {'nombre_pagina': 'Productos', 'lista': productos}
	
	@view_config(route_name='listado_tiendas', renderer='plantillas/listado.pt')
	def listado_tiendas_view(self):
		clientes = DBSession.query(Cliente).join(Tienda).all()
		return {'nombre_pagina': 'Tiendas', 'lista': clientes}
		
	@view_config(route_name='inventario_producto', renderer='plantillas/inventario.pt')
	def inventario_producto_view(self):
		return { 'nombre_pagina': 'Inventario', 'tipo': 'ProductoID' }
		
	@view_config(route_name='inventario_tienda', renderer='plantillas/inventario.pt')
	def inventario_tienda_view(self):
		return { 'nombre_pagina': 'Inventario', 'tipo': 'TiendaID' }