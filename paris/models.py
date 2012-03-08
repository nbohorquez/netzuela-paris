from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, mapper
from zope.sqlalchemy import ZopeTransactionExtension
from .spuria import TABLAS_A_OBJETOS
#from .__init__ import motor

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

# Asocia las tablas de la base de datos con clases en python
def cargar_tablas(motor):
	metadata = MetaData(motor)
	for asociacion in TABLAS_A_OBJETOS:
		tabla = asociacion['tabla']
		objeto = asociacion['objeto']
		esquema_tabla = Table(tabla, metadata, autoload=True)
		mixIn(objeto, [object])
		mapper(globals()[objeto], esquema_tabla)
	# Cargamos el "diferente": la vista InventarioReciente. Esta no tiene PK definida.
	# Descomentar este segemento si estais en Windows:
	"""
	esquema_tabla = Table('inventarioreciente', metadata,
						Column("TiendaID", Integer, primary_key=True),
						Column("Codigo", String, primary_key=True),
						autoload=True)
	"""
	# Descomentar este segemento si estais en Linux:
	esquema_tabla = Table('InventarioReciente', metadata,
						Column("TiendaID", Integer, primary_key=True),
						Column("Codigo", String, primary_key=True),
						autoload=True)
	mixIn('InventarioReciente', [object])
	mapper(globals()['InventarioReciente'], esquema_tabla)

# Codigo tomado de: http://danielkaes.wordpress.com/2009/07/30/create-new-classes-with-python-at-runtime/	
def mixIn(classname, parentclasses):
	if len(parentclasses) > 0:
		parents = map(lambda p:p.__name__, parentclasses)
		createclass = "class %s (%s):\n\tpass" % (classname, ",".join(parents))
	else:
		createclass = "class %s:\n\tpass" % classname
	exec createclass
	globals()[classname] = eval(classname)