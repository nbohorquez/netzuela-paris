from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, mapper
from zope.sqlalchemy import ZopeTransactionExtension
from .spuria import TABLAS_A_OBJETOS
#from .__init__ import motor

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

"""
class Acceso(Base):
	__tablename__ = 'acceso'
	__table_args__ = {'autoload': True}

class Accion(Base):
    __tablename__ = 'accion'
    __table_args__ = {'autoload':True}
    
class Administrador(Base):
    __tablename__ = 'administrador'
    __table_args__ = {'autoload':True}

class Buscable(Base):
    __tablename__ = 'buscable'
    __table_args__ = {'autoload':True}

class Busqueda(Base):
    __tablename__ = 'busqueda'
    __table_args__ = {'autoload':True}

class CalificableSeguible(Base):
    __tablename__ = 'calificableseguible'
    __table_args__ = {'autoload':True}

class Calificacion(Base):
    __tablename__ = 'calificacion'
    __table_args__ = {'autoload':True}

class CalificacionResena(Base):
    __tablename__ = 'calificacionresena'
    __table_args__ = {'autoload':True}

class Categoria(Base):
    __tablename__ = 'categoria'
    __table_args__ = {'autoload':True}

class Ciudad(Base):
    __tablename__ = 'ciudad'
    __table_args__ = {'autoload':True}

class Cliente(Base):
    __tablename__ = 'cliente'
    __table_args__ = {'autoload':True}

class Cobrable(Base):
    __tablename__ = 'cobrable'
    __table_args__ = {'autoload':True}

class CodigoDeError(Base):
    __tablename__ = 'codigodeerror'
    __table_args__ = {'autoload':True}

class Consumidor(Base):
    __tablename__ = 'consumidor'
    __table_args__ = {'autoload':True}

class ConsumidorObjetivo(Base):
    __tablename__ = 'consumidorobjetivo'
    __table_args__ = {'autoload':True}

class ContadorDeExhibiciones(Base):
    __tablename__ = 'contadordeexhibiciones'
    __table_args__ = {'autoload':True}

class Continente(Base):
    __tablename__ = 'continente'
    __table_args__ = {'autoload':True}

class Croquis(Base):
    __tablename__ = 'croquis'
    __table_args__ = {'autoload':True}

class Describible(Base):
    __tablename__ = 'describible'
    __table_args__ = {'autoload':True}

class Descripcion(Base):
    __tablename__ = 'descripcion'
    __table_args__ = {'autoload':True}

class Dia(Base):
    __tablename__ = 'dia'
    __table_args__ = {'autoload':True}

class Dibujable(Base):
    __tablename__ = 'dibujable'
    __table_args__ = {'autoload':True}

class Estadisticas(Base):
    __tablename__ = 'estadisticas'
    __table_args__ = {'autoload':True}

class EstadisticasDeInfluencia(Base):
    __tablename__ = 'estadisticasdeinfluencia'
    __table_args__ = {'autoload':True}

class EstadisticasDePopularidad(Base):
    __tablename__ = 'estadisticasdepopularidad'
    __table_args__ = {'autoload':True}

class EstadisticasDeVisitas(Base):
    __tablename__ = 'estadisticasdevisitas'
    __table_args__ = {'autoload':True}

class EstadisticasTemporales(Base):
    __tablename__ = 'estadisticastemporales'
    __table_args__ = {'autoload':True}

class Estado(Base):
    __tablename__ = 'estado'
    __table_args__ = {'autoload':True}

class Estatus(Base):
    __tablename__ = 'estatus'
    __table_args__ = {'autoload':True}

class Etiqueta(Base):
    __tablename__ = 'etiqueta'
    __table_args__ = {'autoload':True}

class Etiquetable(Base):
    __tablename__ = 'etiquetable'
    __table_args__ = {'autoload':True}

class Factura(Base):
    __tablename__ = 'factura'
    __table_args__ = {'autoload':True}

class Foto(Base):
    __tablename__ = 'foto'
    __table_args__ = {'autoload':True}

class GradoDeInstruccion(Base):
    __tablename__ = 'gradodeinstruccion'
    __table_args__ = {'autoload':True}

class GradoDeInstruccionObjetivo(Base):
    __tablename__ = 'gradodeinstruccionobjetivo'
    __table_args__ = {'autoload':True}

class GrupoDeEdad(Base):
    __tablename__ = 'grupodeedad'
    __table_args__ = {'autoload':True}

class GrupoDeEdadObjetivo(Base):
    __tablename__ = 'grupodeedadobjetivo'
    __table_args__ = {'autoload':True}

class HorarioDeTrabajo(Base):
    __tablename__ = 'horariodetrabajo'
    __table_args__ = {'autoload':True}

class HusoHorario(Base):
    __tablename__ = 'husohorario'
    __table_args__ = {'autoload':True}

class Idioma(Base):
    __tablename__ = 'idioma'
    __table_args__ = {'autoload':True}

class Inventario(Base):
    __tablename__ = 'inventario'
    __table_args__ = {'autoload':True}

class Mensaje(Base):
    __tablename__ = 'mensaje'
    __table_args__ = {'autoload':True}

class Municipio(Base):
    __tablename__ = 'municipio'
    __table_args__ = {'autoload':True}

class Pais(Base):
    __tablename__ = 'pais'
    __table_args__ = {'autoload':True}

class Palabra(Base):
    __tablename__ = 'palabra'
    __table_args__ = {'autoload':True}

class Parroquia(Base):
    __tablename__ = 'parroquia'
    __table_args__ = {'autoload':True}

class Patrocinante(Base):
    __tablename__ = 'patrocinante'
    __table_args__ = {'autoload':True}

class PrecioCantidad(Base):
    __tablename__ = 'preciocantidad'
    __table_args__ = {'autoload':True}

class Privilegios(Base):
    __tablename__ = 'privilegios'
    __table_args__ = {'autoload':True}

class Producto(Base):
    __tablename__ = 'producto'
    __table_args__ = {'autoload':True}

class Publicidad(Base):
    __tablename__ = 'publicidad'
    __table_args__ = {'autoload':True}

class Punto(Base):
    __tablename__ = 'punto'
    __table_args__ = {'autoload':True}

class PuntoDeCroquis(Base):
    __tablename__ = 'puntodecroquis'
    __table_args__ = {'autoload':True}

class Rastreable(Base):
    __tablename__ = 'rastreable'
    __table_args__ = {'autoload':True}

class RegionGeografica(Base):
    __tablename__ = 'regiongeografica'
    __table_args__ = {'autoload':True}

class RegionGeograficaObjetivo(Base):
    __tablename__ = 'regiongeograficaobjetivo'
    __table_args__ = {'autoload':True}

class Registro(Base):
    __tablename__ = 'registro'
    __table_args__ = {'autoload':True}

class RelacionDePalabras(Base):
    __tablename__ = 'relaciondepalabras'
    __table_args__ = {'autoload':True}

class ResultadoDeBusqueda(Base):
    __tablename__ = 'resultadodebusqueda'
    __table_args__ = {'autoload':True}

class Seguidor(Base):
    __tablename__ = 'seguidor'
    __table_args__ = {'autoload':True}

class ServicioVendido(Base):
    __tablename__ = 'serviciovendido'
    __table_args__ = {'autoload':True}

class Sexo(Base):
    __tablename__ = 'sexo'
    __table_args__ = {'autoload':True}

class SexoObjetivo(Base):
    __tablename__ = 'sexoobjetivo'
    __table_args__ = {'autoload':True}

class Tamano(Base):
    __tablename__ = 'tamano'
    __table_args__ = {'autoload':True}

class Tienda(Base):
    __tablename__ = 'tienda'
    __table_args__ = {'autoload':True}

class TiendasConsumidores(Base):
    __tablename__ = 'tiendasconsumidores'
    __table_args__ = {'autoload':True}

class TipoDeCodigo(Base):
    __tablename__ = 'tipodecodigo'
    __table_args__ = {'autoload':True}

class Turno(Base):
    __tablename__ = 'turno'
    __table_args__ = {'autoload':True}

class Usuario(Base):
    __tablename__ = 'usuario'
    __table_args__ = {'autoload':True}

class Visibilidad(Base):
    __tablename__ = 'visibilidad'
    __table_args__ = {'autoload':True}
    
"""
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
	esquema_tabla = Table('inventarioreciente', metadata,
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