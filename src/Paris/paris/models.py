from sqlalchemy import MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, mapper
from zope.sqlalchemy import ZopeTransactionExtension
from .spuria import TABLAS_A_OBJETOS

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
	
# Codigo tomado de: http://danielkaes.wordpress.com/2009/07/30/create-new-classes-with-python-at-runtime/	
def mixIn(classname, parentclasses):
	if len(parentclasses) > 0:
		parents = map(lambda p:p.__name__, parentclasses)
		createclass = "class %s (%s):\n\tpass" % (classname, ",".join(parents))
	else:
		createclass = "class %s:\n\tpass" % classname
	exec createclass
	globals()[classname] = eval(classname)