from .models import DBSession, cargar_tablas
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

def main(global_config, **settings):
	""" This function returns a Pyramid WSGI application.
	"""
	# Cargamos de forma dinamica todas las tablas desde la base de datos
	engine = engine_from_config(settings, 'sqlalchemy.')
	cargar_tablas(engine)
	DBSession.configure(bind=engine)
	
	"""
	Tengo que cargar paris.seguridad.obtener_grupos de forma dinamica porque depende de una clase
	(acceso) que tambien fue cargada de forma dinamica en el paso anterior.
	Tome el codigo de aqui: http://stackoverflow.com/questions/547829/how-to-dynamically-load-a-python-class
	"""
	modulo = __import__('paris.seguridad', fromlist=['obtener_grupos'])
	obtener_grupos = getattr(modulo, 'obtener_grupos')
	"""
	Esta forma que explican aqui: http://technogeek.org/python-module.html es mucho mas sencilla
	y directa
	"""	
	# exec 'from .seguridad import obtener_grupos'
	authn_policy = AuthTktAuthenticationPolicy('iuahxN151_!=QSC?', callback=obtener_grupos)
	authz_policy = ACLAuthorizationPolicy()
	
	# Configuramos la aplicacion WSGI
	config = Configurator(settings=settings, root_factory='paris.models.root_factory')
	config.set_authentication_policy(authn_policy)
	config.set_authorization_policy(authz_policy)
	config.add_static_view('estatico', 'estatico', cache_max_age=3600)
	config.add_route('inicio', '/')
	config.add_route('producto', '/producto/{producto_id}')
	config.add_route('tienda', '/tienda/{tienda_id}')
	config.add_route('productos', '/productos/cat{categoria_id}geo{territorio_id}')
	config.add_route('tiendas', '/tiendas/cat{categoria_id}geo{territorio_id}')
	config.add_route('tienda_turno', '/tienda_turno.json')
	config.add_route('tienda_coordenadas', '/tienda_coordenadas.json')
	config.add_route('territorio_coordenadas', '/territorio_coordenadas.json')
	config.add_route('ingresar', '/ingresar')
	config.add_route('salir', '/salir')
	config.scan()
	return config.make_wsgi_app()