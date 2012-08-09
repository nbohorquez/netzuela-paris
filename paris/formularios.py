# -*- coding: utf-8 -*-
'''
Created on 19/06/2012

@author: nestor
'''

import formencode, re
from .constantes import EDAD_MINIMA
from paris.models.spuria import (
    acceso, 
    categoria, 
    DBSession, 
    grado_de_instruccion, 
    sexo, 
    territorio
)
from datetime import date, timedelta
from formencode import validators
from formencode.api import Invalid

class ContrasenaSegura(validators.FancyValidator):
    minimo = 8
    minimo_no_letras = 2
    letras = re.compile(r'[a-zA-Z]')
    diccionario = '/usr/share/dict/words'
    messages = {
        'corto': unicode('La contraseña debe tener más de %(minimo)i carácteres', 'utf-8'),
        'solo_letras': unicode('La contraseña debe incluir al menos %(minimo_no_letras)i carácter(es) que no sea(n) letra(s)', 'utf-8'),
        'diccionario': unicode('No base su contraseña en una palabra del diccionario', 'utf-8')
    }

    def _to_python(self, valor, estado):
        return valor.strip()

    def validate_python(self, valor, estado):
        # Chequeamos la longitud de la contraseña
        if len(valor) < self.minimo:
            raise Invalid(self.message("corto", estado, minimo=self.minimo), valor, estado)
        
        # Chequeamos que no sea una palabra facil de ubicar en un diccionario
        f = open(self.diccionario)
        valor_minuscula = valor.strip().lower()
        for line in f:
            if line.strip().lower() == valor_minuscula:
                raise Invalid(self.message("diccionario", None), valor, estado)
            
        # Chequeamos que tenga por lo menos dos caracteres que no sean letras
        no_letras = self.letras.sub('', valor)
        if len(no_letras) < self.minimo_no_letras:
            raise Invalid(self.message("solo_letras", estado, minimo_no_letras=self.minimo_no_letras), valor, estado)

class UsuarioUnico(validators.FancyValidator):
    mensaje = unicode('El usuario especificado ya existe en la base de datos', 'utf-8')
    
    def _to_python(self, valor, estado):
        return valor.strip()
    
    def validate_python(self, valor, estado):
        existe = DBSession.query(acceso).filter_by(correo_electronico = valor).first()
        if existe is not None:
            raise Invalid(self.mensaje, valor, estado)
    
class GradoDeInstruccionValido(validators.FancyValidator):
    mensaje = unicode('Grado de instrucción no conocido', 'utf-8')
    
    def _to_python(self, valor, estado):
        return valor.strip()
    
    def validate_python(self, valor, estado):
        grados = DBSession.query(grado_de_instruccion).filter(grado_de_instruccion.valor == valor).first()
        if grados is None:
            raise Invalid(self.mensaje, valor, estado)
        
class CategoriaValida(validators.FancyValidator):
    mensaje = unicode('Categoria no conocida', 'utf-8')
    
    def _to_python(self, valor, estado):
        return valor.strip()
    
    def validate_python(self, valor, estado):
        categorias = DBSession.query(categoria).filter(categoria.categoria_id == valor).first()
        if categorias is None:
            raise Invalid(self.mensaje, valor, estado)
    
class SexoValido(validators.FancyValidator):
    mensaje = unicode('Sexo no conocido', 'utf-8')
    
    def _to_python(self, valor, estado):
        return valor.strip()
    
    def validate_python(self, valor, estado):
        sexos = DBSession.query(sexo).filter(sexo.valor == valor).first()
        if sexos is None:
            raise Invalid(self.mensaje, valor, estado)
        
class UbicacionExistente(validators.FancyValidator):
    mensaje = unicode('Región no conocida', 'utf-8')
    if_missing = None
    
    def _to_python(self, valor, estado):
        return valor.strip()
    
    def validate_python(self, valor, estado):
        resultado = DBSession.query(territorio.nombre).filter_by(territorio_id = valor).first()
        if resultado is None:
            raise Invalid(self.mensaje, valor, estado)
    
class EdadValida(validators.FancyValidator):
    convertidor = validators.DateConverter(month_style='dd/mm/yyyy')
    validador = validators.DateValidator(latest_date=date.today()-timedelta(days=EDAD_MINIMA*365.24))
    
    def _to_python(self, valor, estado):
        return valor.strip()
    
    def validate_python(self, valor, estado):
        convertida = self.convertidor.to_python(valor)
        self.validador.to_python(convertida)
        
class RifValido(validators.FancyValidator):
    validador = validators.Regex(regex='^[JVG]-[0-9]{8}-[0-9]$')
    
    def _to_python(self, valor, estado):
        return valor.strip()
    
    def validate_python(self, valor, estado):
        self.validador.to_python(valor)
        
class NullableString(validators.FancyValidator):
    if_missing = None
    
    def _to_python(self, valor, estado):
        return valor.strip()
    
    def validate_python(self, valor, estado):
        self.validador.to_python(valor)

class FormularioAgregarConsumidor(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    grado_de_instruccion = formencode.All(validators.String(not_empty=True), GradoDeInstruccionValido())
    sexo = formencode.All(validators.String(not_empty=True), SexoValido())
    fecha_de_nacimiento = EdadValida()
    
class FormularioCrearConsumidor(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    correo_electronico = formencode.All(validators.Email(resolve_domain=True), UsuarioUnico())
    contrasena = ContrasenaSegura()
    repetir_contrasena = validators.String(not_empty=True)
    nombre = validators.String(not_empty=True)
    apellido = validators.String(not_empty=True)
    grado_de_instruccion = formencode.All(validators.String(not_empty=True), GradoDeInstruccionValido())
    ubicacion = UbicacionExistente()
    sexo = formencode.All(validators.String(not_empty=True), SexoValido())
    fecha_de_nacimiento = EdadValida()
    chained_validators = [validators.FieldsMatch('contrasena', 'repetir_contrasena')]
    
class FormularioCrearUsuario(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    correo_electronico = formencode.All(validators.Email(resolve_domain=True), UsuarioUnico())
    contrasena = ContrasenaSegura()
    repetir_contrasena = validators.String(not_empty=True)
    nombre = validators.String(not_empty=True)
    apellido = validators.String(not_empty=True)
    ubicacion = UbicacionExistente()
    chained_validators = [validators.FieldsMatch('contrasena', 'repetir_contrasena')]
    
class FormularioCrearTienda(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    rif = formencode.All(validators.String(not_empty=True), RifValido())
    nombre_legal = validators.String(not_empty=True)
    nombre_comun = validators.String(not_empty=True)
    categoria = formencode.All(validators.String(not_empty=True), CategoriaValida())
    telefono = formencode.All(validators.String(not_empty=True), validators.Regex(regex='^[1-9][0-9]{2}-[1-9][0-9]{6}$'))
    edificio_cc = NullableString()
    piso = NullableString()
    apartamento = NullableString()
    local_no = NullableString()
    casa = NullableString()
    calle = validators.String(not_empty=True)
    urbanizacion = validators.String(not_empty=True)
    pagina_web = NullableString()
    facebook = NullableString()
    twitter = NullableString()
    correo_electronico_publico = NullableString()
    ubicacion = UbicacionExistente()
    
class FormularioEditarUsuario(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    nombre = validators.String(not_empty=True)
    apellido = validators.String(not_empty=True)
    ubicacion = UbicacionExistente()
    
class FormularioEditarConsumidor(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    grado_de_instruccion = GradoDeInstruccionValido(if_missing=None)
    sexo = SexoValido(if_missing=None)
    fecha_de_nacimiento = EdadValida(if_missing=None)