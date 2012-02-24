from sqlalchemy import MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, mapper
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

# Aqui van las clases
class Acceso(object):
	pass

# Asocia las tablas de la base de datos con clases en python
def cargar_tablas(engine):
	metadata = MetaData(engine)
	moz_acceso = Table('acceso', metadata, autoload=True)
	mapper(Acceso, moz_acceso)