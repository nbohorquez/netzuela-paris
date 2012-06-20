# -*- coding: utf-8 -*-
'''
Created on 07/06/2012

@author: nestor
'''

from .comunes import comunes
from .constantes import CREADOR
from .diagramas import diagramas
from .models import DBSession
from .formulario_registro import formulario
from formencode.api import Invalid
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from sqlalchemy.sql import select, func, bindparam
from time import strftime, strptime
import bcrypt

class registro_view(diagramas, comunes):
    def __init__(self, peticion):
        self.peticion = peticion
        registro_url = peticion.route_url('registro')
        self.pagina_actual = peticion.url
        self.referido_por = peticion.url if (peticion.url != registro_url) else '/'

    @reify
    def peticion(self):
        return self.peticion
    
    @reify
    def pagina_actual(self):
        return self.pagina_actual
    
    @reify
    def pagina_anterior(self):
        return self.peticion.params.get('pagina_anterior', self.referido_por)
    
    @view_config(route_name='registro', renderer='plantillas/registro.pt')
    def registro_view(self):
        mensaje = ''
        
        if 'enviar' in self.peticion.params:            
            try:
                valido = formulario.to_python(dict(self.peticion.params))
            except Invalid as e:
                mensaje = e.msg
            else:
                sql = select([func.InsertarConsumidor(
                    bindparam('a_creador'), 
                    bindparam('a_nombre'), 
                    bindparam('a_apellido'),
                    bindparam('a_estatus'),
                    bindparam('a_sexo'),
                    bindparam('a_fecha_de_nacimiento'),
                    bindparam('a_grupo_de_edad'),
                    bindparam('a_grado_de_instruccion'),
                    bindparam('a_ubicacion'),
                    bindparam('a_correo_electronico'),
                    bindparam('a_contrasena')
                )])
                
                """
                Como yo llamo a las funciones de spuria con SELECT, SQLAlchemy automaticamente hace
                un ROLLBACK de todo lo que hizo el SELECT ya que esa instruccion no deberia generar 
                ningun cambio en la base de datos. 
                
                Para anular este comportamiento, hay que encapsular la transaccion entre las instrucciones
                connection.begin() y connection.commit(). Lee:            
                http://stackoverflow.com/questions/7559570/make-sqlalchemy-commit-instead-of-rollback-after-a-select-query
                """
                fecha_time = strptime(valido['fecha_de_nacimiento'], '%d/%m/%Y')
                fecha_string = strftime('%Y-%m-%d', fecha_time)
                
                DBSession.connection().execute('begin')
                resultado = DBSession.connection().execute(sql, 
                    a_creador = CREADOR,
                    a_nombre = valido['nombre'],
                    a_apellido = valido['apellido'],
                    a_estatus = 'Activo',
                    a_sexo = valido['sexo'],
                    a_fecha_de_nacimiento = fecha_string,
                    a_grupo_de_edad = 'Adultos jovenes',
                    a_grado_de_instruccion = valido['grado_de_instruccion'],
                    a_ubicacion = '0.02.01.03.00.00',
                    a_correo_electronico = valido['correo_electronico'],
                    a_contrasena = bcrypt.hashpw(valido['contrasena'], bcrypt.gensalt())
                ).scalar()
                DBSession.connection().execute('commit')
                
                if resultado == 1048:
                    mensaje = 'Error de valor nulo: ¿le faltó por llenar algún campo?'
                elif mensaje == 1452:
                    mensaje = 'Error de clave externa: ¿colocó correctamente todos sus datos?'
                elif mensaje == 1062:
                    mensaje = 'Error de clave duplicada: este usuario ya existe'
                else:
                    mensaje = 'Registro completado con éxito'
        elif 'cancelar' in self.peticion.params:
            return HTTPFound(location = self.pagina_anterior)
            
        return  {'pagina': 'Registro', 'mensaje': mensaje }