'''
Created on 25/02/2012

@author: Nestor
'''

# Si estais en Windows descomenta este segemento:

"""
TABLAS_A_OBJETOS = [
                    {'tabla': 'acceso',                     'objeto': 'Acceso'},
                    {'tabla': 'accion',                     'objeto': 'Accion'},
                    {'tabla': 'administrador',              'objeto': 'Administrador'},
                    {'tabla': 'buscable',                   'objeto': 'Buscable'},
                    {'tabla': 'busqueda',                   'objeto': 'Busqueda'},
                    {'tabla': 'calificableseguible',        'objeto': 'CalificableSeguible'},
                    {'tabla': 'calificacion',               'objeto': 'Calificacion'},
                    {'tabla': 'calificacionresena',         'objeto': 'CalificacionResena'},
                    {'tabla': 'categoria',                  'objeto': 'Categoria'},
                    {'tabla': 'ciudad',                     'objeto': 'Ciudad'},
                    {'tabla': 'cliente',                    'objeto': 'Cliente'},
                    {'tabla': 'cobrable',                   'objeto': 'Cobrable'},
                    {'tabla': 'codigodeerror',              'objeto': 'CodigoDeError'},
                    {'tabla': 'consumidor',                 'objeto': 'Consumidor'},
                    {'tabla': 'consumidorobjetivo',         'objeto': 'ConsumidorObjetivo'},
                    {'tabla': 'contadordeexhibiciones',     'objeto': 'ContadorDeExhibiciones'},
                    {'tabla': 'continente',                 'objeto': 'Continente'},
                    {'tabla': 'croquis',                    'objeto': 'Croquis'},
                    {'tabla': 'describible',                'objeto': 'Describible'},
                    {'tabla': 'descripcion',                'objeto': 'Descripcion'},
                    {'tabla': 'dia',                        'objeto': 'Dia'},
                    {'tabla': 'dibujable',                  'objeto': 'Dibujable'},
                    {'tabla': 'estadisticas',               'objeto': 'Estadisticas'},
                    {'tabla': 'estadisticasdeinfluencia',   'objeto': 'EstadisticasDeInfluencia'},
                    {'tabla': 'estadisticasdepopularidad',  'objeto': 'EstadisticasDePopularidad'},
                    {'tabla': 'estadisticasdevisitas',      'objeto': 'EstadisticasDeVisitas'},
                    {'tabla': 'estadisticastemporales',     'objeto': 'EstadisticasTemporales'},
                    {'tabla': 'estado',                     'objeto': 'Estado'},
                    {'tabla': 'estatus',                    'objeto': 'Estatus'},
                    {'tabla': 'etiqueta',                   'objeto': 'Etiqueta'},
                    {'tabla': 'etiquetable',                'objeto': 'Etiquetable'},
                    {'tabla': 'factura',                    'objeto': 'Factura'},
                    {'tabla': 'foto',                       'objeto': 'Foto'},
                    {'tabla': 'gradodeinstruccion',         'objeto': 'GradoDeInstruccion'},
                    {'tabla': 'gradodeinstruccionobjetivo', 'objeto': 'GradoDeInstruccionObjetivo'},
                    {'tabla': 'grupodeedad',                'objeto': 'GrupoDeEdad'},
                    {'tabla': 'grupodeedadobjetivo',        'objeto': 'GrupoDeEdadObjetivo'},
                    {'tabla': 'horariodetrabajo',           'objeto': 'HorarioDeTrabajo'},
                    {'tabla': 'husohorario',                'objeto': 'HusoHorario'},
                    {'tabla': 'idioma',                     'objeto': 'Idioma'},
                    {'tabla': 'interlocutor',               'objeto': 'Interlocutor'},
                    {'tabla': 'inventario',                 'objeto': 'Inventario'},
                    #{'tabla': 'inventariotienda',           'objeto': 'InventarioTienda'},
                    #{'tabla': 'inventarioReciente',         'objeto': 'InventarioReciente'},
                    {'tabla': 'mensaje',                    'objeto': 'Mensaje'},
                    {'tabla': 'municipio',                  'objeto': 'Municipio'},
                    {'tabla': 'pais',                       'objeto': 'Pais'},
                    {'tabla': 'palabra',                    'objeto': 'Palabra'},
                    {'tabla': 'parroquia',                  'objeto': 'Parroquia'},
                    {'tabla': 'patrocinante',               'objeto': 'Patrocinante'},
                    {'tabla': 'preciocantidad',             'objeto': 'PrecioCantidad'},
                    {'tabla': 'privilegios',                'objeto': 'Privilegios'},
                    {'tabla': 'producto',                   'objeto': 'Producto'},
                    {'tabla': 'publicidad',                 'objeto': 'Publicidad'},
                    {'tabla': 'punto',                      'objeto': 'Punto'},
                    {'tabla': 'puntodecroquis',             'objeto': 'PuntoDeCroquis'},
                    {'tabla': 'rastreable',                 'objeto': 'Rastreable'},
                    {'tabla': 'regiongeografica',           'objeto': 'RegionGeografica'},
                    {'tabla': 'regiongeograficaobjetivo',   'objeto': 'RegionGeograficaObjetivo'},
                    {'tabla': 'registro',                   'objeto': 'Registro'},
                    {'tabla': 'relaciondepalabras',         'objeto': 'RelacionDePalabras'},
                    {'tabla': 'resultadodebusqueda',        'objeto': 'ResultadoDeBusqueda'},
                    {'tabla': 'seguidor',                   'objeto': 'Seguidor'},
                    {'tabla': 'serviciovendido',            'objeto': 'ServicioVendido'},
                    {'tabla': 'sexo',                       'objeto': 'Sexo'},
                    {'tabla': 'sexoobjetivo',               'objeto': 'SexoObjetivo'},
                    {'tabla': 'subcontinente',              'objeto': 'Subcontinente'},
                    {'tabla': 'tamano',                     'objeto': 'Tamano'},
                    {'tabla': 'tienda',                     'objeto': 'Tienda'},
                    {'tabla': 'tiendasconsumidores',        'objeto': 'TiendasConsumidores'},
                    {'tabla': 'tipodecodigo',               'objeto': 'TipoDeCodigo'},
                    {'tabla': 'turno',                      'objeto': 'Turno'},
                    {'tabla': 'usuario',                    'objeto': 'Usuario'},
                    {'tabla': 'visibilidad',                'objeto': 'Visibilidad'},
]
"""

# Si estais en Linux descomenta este segemento:
TABLAS_A_OBJETOS = [
                    {'tabla': 'Acceso',                     'objeto': 'Acceso'},
                    {'tabla': 'Accion',                     'objeto': 'Accion'},
                    {'tabla': 'Administrador',              'objeto': 'Administrador'},
                    {'tabla': 'Buscable',                   'objeto': 'Buscable'},
                    {'tabla': 'Busqueda',                   'objeto': 'Busqueda'},
                    {'tabla': 'CalificableSeguible',        'objeto': 'CalificableSeguible'},
                    {'tabla': 'Calificacion',               'objeto': 'Calificacion'},
                    {'tabla': 'CalificacionResena',         'objeto': 'CalificacionResena'},
                    {'tabla': 'Categoria',                  'objeto': 'Categoria'},
                    {'tabla': 'Ciudad',                     'objeto': 'Ciudad'},
                    {'tabla': 'Cliente',                    'objeto': 'Cliente'},
                    {'tabla': 'Cobrable',                   'objeto': 'Cobrable'},
                    {'tabla': 'CodigoDeError',              'objeto': 'CodigoDeError'},
                    {'tabla': 'Consumidor',                 'objeto': 'Consumidor'},
                    {'tabla': 'ConsumidorObjetivo',         'objeto': 'ConsumidorObjetivo'},
                    {'tabla': 'ContadorDeExhibiciones',     'objeto': 'ContadorDeExhibiciones'},
                    {'tabla': 'Continente',                 'objeto': 'Continente'},
                    {'tabla': 'Croquis',                    'objeto': 'Croquis'},
                    {'tabla': 'Describible',                'objeto': 'Describible'},
                    {'tabla': 'Descripcion',                'objeto': 'Descripcion'},
                    {'tabla': 'Dia',                        'objeto': 'Dia'},
                    {'tabla': 'Dibujable',                  'objeto': 'Dibujable'},
                    {'tabla': 'Estadisticas',               'objeto': 'Estadisticas'},
                    {'tabla': 'EstadisticasDeInfluencia',   'objeto': 'EstadisticasDeInfluencia'},
                    {'tabla': 'EstadisticasDePopularidad',  'objeto': 'EstadisticasDePopularidad'},
                    {'tabla': 'EstadisticasDeVisitas',      'objeto': 'EstadisticasDeVisitas'},
                    {'tabla': 'EstadisticasTemporales',     'objeto': 'EstadisticasTemporales'},
                    {'tabla': 'Estado',                     'objeto': 'Estado'},
                    {'tabla': 'Estatus',                    'objeto': 'Estatus'},
                    {'tabla': 'Etiqueta',                   'objeto': 'Etiqueta'},
                    {'tabla': 'Etiquetable',                'objeto': 'Etiquetable'},
                    {'tabla': 'Factura',                    'objeto': 'Factura'},
                    {'tabla': 'Foto',                       'objeto': 'Foto'},
                    {'tabla': 'GradoDeInstruccion',         'objeto': 'GradoDeInstruccion'},
                    {'tabla': 'GradoDeInstruccionObjetivo', 'objeto': 'GradoDeInstruccionObjetivo'},
                    {'tabla': 'GrupoDeEdad',                'objeto': 'GrupoDeEdad'},
                    {'tabla': 'GrupoDeEdadObjetivo',        'objeto': 'GrupoDeEdadObjetivo'},
                    {'tabla': 'HorarioDeTrabajo',           'objeto': 'HorarioDeTrabajo'},
                    {'tabla': 'HusoHorario',                'objeto': 'HusoHorario'},
                    {'tabla': 'Idioma',                     'objeto': 'Idioma'},
                    {'tabla': 'Interlocutor',               'objeto': 'Interlocutor'},
                    {'tabla': 'Inventario',                 'objeto': 'Inventario'},
                    #{'tabla': 'InventarioTienda',           'objeto': 'InventarioTienda'},
                    #{'tabla': 'InventarioReciente',         'objeto': 'InventarioReciente'},
                    {'tabla': 'Mensaje',                    'objeto': 'Mensaje'},
                    {'tabla': 'Municipio',                  'objeto': 'Municipio'},
                    {'tabla': 'Pais',                       'objeto': 'Pais'},
                    {'tabla': 'Palabra',                    'objeto': 'Palabra'},
                    {'tabla': 'Parroquia',                  'objeto': 'Parroquia'},
                    {'tabla': 'Patrocinante',               'objeto': 'Patrocinante'},
                    {'tabla': 'PrecioCantidad',             'objeto': 'PrecioCantidad'},
                    {'tabla': 'Privilegios',                'objeto': 'Privilegios'},
                    {'tabla': 'Producto',                   'objeto': 'Producto'},
                    {'tabla': 'Publicidad',                 'objeto': 'Publicidad'},
                    {'tabla': 'Punto',                      'objeto': 'Punto'},
                    {'tabla': 'PuntoDeCroquis',             'objeto': 'PuntoDeCroquis'},
                    {'tabla': 'Rastreable',                 'objeto': 'Rastreable'},
                    {'tabla': 'RegionGeografica',           'objeto': 'RegionGeografica'},
                    {'tabla': 'RegionGeograficaObjetivo',   'objeto': 'RegionGeograficaObjetivo'},
                    {'tabla': 'Registro',                   'objeto': 'Registro'},
                    {'tabla': 'RelacionDePalabras',         'objeto': 'RelacionDePalabras'},
                    {'tabla': 'ResultadoDeBusqueda',        'objeto': 'ResultadoDeBusqueda'},
                    {'tabla': 'Seguidor',                   'objeto': 'Seguidor'},
                    {'tabla': 'ServicioVendido',            'objeto': 'ServicioVendido'},
                    {'tabla': 'Sexo',                       'objeto': 'Sexo'},
                    {'tabla': 'SexoObjetivo',               'objeto': 'SexoObjetivo'},
                    {'tabla': 'Subcontinente',              'objeto': 'Subcontinente'},
                    {'tabla': 'Tamano',                     'objeto': 'Tamano'},
                    {'tabla': 'Tienda',                     'objeto': 'Tienda'},
                    {'tabla': 'TiendasConsumidores',        'objeto': 'TiendasConsumidores'},
                    {'tabla': 'TipoDeCodigo',               'objeto': 'TipoDeCodigo'},
                    {'tabla': 'Turno',                      'objeto': 'Turno'},
                    {'tabla': 'Usuario',                    'objeto': 'Usuario'},
                    {'tabla': 'Visibilidad',                'objeto': 'Visibilidad'},
]

INVENTARIO_RECIENTE = [
                       'TiendaID',
                       'ProductoID',
                       'Codigo',
                       'Descripcion',
                       'Precio',
                       'Cantidad' 
]

PRODUCTO = [ 
            'Rastreable_P', 
            'Describible_P', 
            'Buscable_P',
            'CalificableSeguible_P',
            'ProductoID',
            'TipoDeCodigo',
            'Codigo',
            'Estatus',
            'Fabricante',
            'Modelo',
            'Nombre',
            'Categoria',
            'DebutEnElMercado',
            'Largo',
            'Ancho',
            'Alto',
            'Peso',
            'PaisDeOrigen'
]

PRODUCTO_REDUCIDO = [
                     'ProductoID',
                     'Codigo',
                     'Categoria',
                     'Fabricante',
                     'Modelo',
                     'Nombre',                     
]

TIENDA = [
          'Buscable_P',
          'Cliente_P',
          'CalificableSeguible_P',
          'Interlocutor_P',
          'Dibujable_P',
          'TiendaID',
          'Abierto'
]

CLIENTE = [
           'Rastreable_P',
           'Describible_P',
           'Usuario_P',
           'RIF',
           'Categoria',
           'Estatus',
           'NombreLegal',
           'NombreComun',
           'Telefono',
           'Edificio_CC',
           'Piso',
           'Apartamento',
           'LocalNo',
           'Casa',
           'Calle',
           'Sector_Urb_Barrio',
           'PaginaWeb',
           'Facebook',
           'Twitter'
]

CLIENTE_REDUCIDO = [
                    'RIF',
                    'Categoria',
                    'NombreLegal',
                    'NombreComun',
                    'Telefono',
]