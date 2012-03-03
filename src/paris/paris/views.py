from .models import (DBSession, Tienda, Producto, Cliente, InventarioReciente)
from esquemas import Esquemas
from pyramid.decorator import reify
from pyramid.httpexceptions import (HTTPFound, HTTPNotFound)
from pyramid.view import view_config

# Aptana siempre va a decir que las clases de Spuria (Tienda, Producto, etc) no estan 
# definidas explicitamente en ninguna parte. Lo que ocurre es que yo las cargo de forma 
# dinamica cuando inicia la aplicacion.

class ParisViews(Esquemas):
	def __init__(self, peticion):
		self.peticion = peticion
		pass
	
	@reify
	def peticion(self):
		peticion = self.peticion
		return peticion
	
	@view_config(route_name='inicio', renderer='plantillas/inicio.pt')
	def inicio_view(self):
		return {'nombre_pagina': 'Inicio'}
	
	@view_config(route_name='listado_productos', renderer='plantillas/listado.pt')
	def listado_productos_view(self):
		productos = DBSession.query(Producto).all()
		return {'nombre_pagina': 'Productos', 'lista': productos}
	
	@view_config(route_name='producto', renderer='plantillas/producto.pt')
	def producto_view(self):
		producto_id = self.peticion.matchdict['producto_id']
		producto = DBSession.query(Producto).filter_by(ProductoID = producto_id).first()
		
		if producto is None:
			return HTTPNotFound('Vos lo que estais es loco! Esa verga no existe')
		
		inventario_url = self.peticion.route_url('inventario_producto', producto_id = producto_id)
		return { 'nombre_pagina': 'Producto', 'producto': producto, 'inventario_url': inventario_url }
	
	@view_config(route_name='listado_tiendas', renderer='plantillas/listado.pt')
	def listado_tiendas_view(self):
		clientes = DBSession.query(Cliente).join(Tienda).all()
		return {'nombre_pagina': 'Tiendas', 'lista': clientes}
	
	@view_config(route_name='tienda', renderer='plantillas/tienda.pt')
	def tienda_view(self):
		tienda_id = self.peticion.matchdict['tienda_id']
		tienda = DBSession.query(Tienda).filter_by(TiendaID = tienda_id).first()
		
		if tienda is None:
			return HTTPNotFound('Vos lo que estais es loco! Esa verga no existe')
		
		cliente = DBSession.query(Cliente).filter_by(RIF = tienda.Cliente_P).first()
		inventario_url = self.peticion.route_url('inventario_tienda', tienda_id = tienda_id)
		return { 'nombre_pagina': 'Tienda', 'cliente': cliente, 'abierto': tienda.Abierto, 'inventario_url': inventario_url }
	
	@view_config(route_name='inventario_producto', renderer='plantillas/inventario.pt')
	def inventario_producto_view(self):
		producto_id = self.peticion.matchdict['producto_id']
		inventario = DBSession.query(InventarioReciente).filter_by(ProductoID = producto_id).all()
		
		if inventario is None:
			return HTTPNotFound('Vos lo que estais es loco! Esa verga no existe')
		else:
			return { 'nombre_pagina': 'Inventario', 'inventario': inventario, 'tipo': 'ProductoID' }
		
	@view_config(route_name='inventario_tienda', renderer='plantillas/inventario.pt')
	def inventario_tienda_view(self):
		tienda_id = self.peticion.matchdict['tienda_id']
		inventario = DBSession.query(InventarioReciente).filter_by(TiendaID = tienda_id).all()
	
		if inventario is None:
			return HTTPNotFound('Vos lo que estais es loco! Esa verga no existe')
		else:
			return { 'nombre_pagina': 'Inventario', 'inventario': inventario, 'tipo': 'TiendaID' }