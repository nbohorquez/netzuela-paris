# -*- coding: utf-8 -*-
from constantes import TABLAS
from pyramid.security import Allow, Everyone
from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker, mapper
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

# Asocia las tablas de la base de datos con clases en python
def cargar_tablas(motor):
	metadata = MetaData(motor)
	for asociacion in TABLAS:
		tabla = asociacion
		objeto = asociacion
		esquema_tabla = Table(tabla, metadata, autoload=True)
		mixIn(objeto, [object])
		mapper(globals()[objeto], esquema_tabla)
	# Cargamos el primer "diferente": la vista inventario_reciente. Esta no tiene PK definida.
	esquema_tabla = Table('inventario_reciente', metadata,
						Column("tienda_id", Integer, primary_key=True),
						Column("codigo", String, primary_key=True),
						autoload=True)
	mixIn('inventario_reciente', [object])
	mapper(globals()['inventario_reciente'], esquema_tabla)
	
	# Cargamos el segundo "diferente": la vista tamano_reciente. Tampoco tiene PK definida.
	esquema_tabla = Table('tamano_reciente', metadata,
						Column("tienda_id", Integer, primary_key=True),
						Column("fecha_inicio", String, primary_key=True),
						autoload=True)
	mixIn('tamano_reciente', [object])
	mapper(globals()['tamano_reciente'], esquema_tabla)

# Codigo tomado de: http://danielkaes.wordpress.com/2009/07/30/create-new-classes-with-python-at-runtime/	
def mixIn(classname, parentclasses):
	if len(parentclasses) > 0:
		parents = map(lambda p:p.__name__, parentclasses)
		createclass = "class %s (%s):\n\tpass" % (classname, ",".join(parents))
	else:
		createclass = "class %s:\n\tpass" % classname
	exec createclass
	globals()[classname] = eval(classname)

class root_factory(object):
	__acl__ = [ (Allow, Everyone, 'ver'),
                (Allow, 'groupo:tiendas', 'editar_tienda'),
				(Allow, 'groupo:consumidores', 'editar_consumidor') ]
	
	def __init__(self, request):
		pass