from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import DBSession, cargar_tablas

def main(global_config, **settings):
	""" This function returns a Pyramid WSGI application.
	"""
	engine = engine_from_config(settings, 'sqlalchemy.')
	cargar_tablas(engine)
	#globals()['motor'] = engine
	DBSession.configure(bind=engine)
	config = Configurator(settings=settings)
	config.add_static_view('estatico', 'estatico', cache_max_age=3600)
	config.add_route('inicio', '/')
	config.add_route('producto', '/producto/{producto_id}')
	config.add_route('tienda', '/tienda/{tienda_id}')
	config.add_route('productos', '/productos/cat{categoria_id}geo{territorio_id}')
	config.add_route('tiendas', '/tiendas/cat{categoria_id}geo{territorio_id}')
	config.add_route('tienda_turno', '/tienda_turno.json')
	config.add_route('tienda_coordenadas', '/tienda_coordenadas.json')
	config.scan()
	return config.make_wsgi_app()