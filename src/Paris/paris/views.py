from pyramid.view import view_config
from pyramid.httpexceptions import ( 
	HTTPFound,
    HTTPNotFound,
)
from .models import (
	DBSession, 
	Tienda, 
	Producto, 
	Cliente,
)

# Aptana siempre va a decir que las clases de Spuria (Tienda, Producto, etc) no estan 
# definidas explicitamente en ninguna parte. Lo que ocurre es que yo las cargo de forma 
# dinamica cuando inicia la aplicacion.

@view_config(route_name='inicio', renderer='plantillas/inicio.pt')
def inicio_view(peticion):
	return { 'nombre_pagina': 'Inicio' }

@view_config(route_name='producto', renderer='plantillas/producto.pt')
def producto_view(peticion):
	producto_id = peticion.matchdict['producto_id']
	producto = DBSession.query(Producto).filter_by(ProductoID = producto_id).first()
	
	if producto is None:
		return HTTPNotFound('Vos lo que estais es loco! Esa verga no existe')
	
	return { 'nombre_pagina': 'Producto', 'producto': producto }

@view_config(route_name='tienda', renderer='plantillas/tienda.pt')
def tienda_view(peticion):
	tienda_id = peticion.matchdict['tienda_id']
	tienda = DBSession.query(Tienda).filter_by(TiendaID = tienda_id).first()
	
	if tienda is None:
		return HTTPNotFound('Vos lo que estais es loco! Esa verga no existe')
	
	cliente = DBSession.query(Cliente).filter_by(RIF = tienda.Cliente_P).first()
	return { 'nombre_pagina': 'Tienda', 'tienda_id': tienda.TiendaID, 'cliente': cliente}