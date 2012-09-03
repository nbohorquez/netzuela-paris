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
    territorio,
    tipo_de_codigo
)
from datetime import date, timedelta
from formencode import validators
from formencode.api import Invalid
from sqlalchemy import and_

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

class TextoValido(validators.FancyValidator):
    mensaje = unicode('Texto con errores', 'utf-8')
    convertidor = validators.UnicodeString(not_empty=True)
    
    def _to_python(self, valor, estado):
        return valor.strip()
    
    def validate_python(self, valor, estado):
        self.convertidor.to_python(valor)
    
class SexoValido(validators.FancyValidator):
    mensaje = unicode('Sexo no conocido', 'utf-8')
    
    def _to_python(self, valor, estado):
        return valor.strip()
    
    def validate_python(self, valor, estado):
        sexos = DBSession.query(sexo).filter(sexo.valor == valor).first()
        if sexos is None:
            raise Invalid(self.mensaje, valor, estado)

class TipoDeCodigoValido(validators.FancyValidator):
    mensaje = unicode('Tipo de código no conocido', 'utf-8')
    
    def _to_python(self, valor, estado):
        return valor.strip()
    
    def validate_python(self, valor, estado):
        tipos = DBSession.query(tipo_de_codigo).filter(tipo_de_codigo.valor == valor).first()
        if tipos is None:
            raise Invalid(self.mensaje, valor, estado)

class UbicacionExistente(validators.FancyValidator):
    mensaje = unicode('Región no conocida', 'utf-8')
    
    def _to_python(self, valor, estado):
        return valor.strip()
    
    def validate_python(self, valor, estado):
        resultado = DBSession.query(territorio.nombre).filter_by(territorio_id = valor).first()
        if resultado is None:
            raise Invalid(self.mensaje, valor, estado)

class PaisExistente(validators.FancyValidator):
    mensaje = unicode('País no conocido', 'utf-8')
    
    def _to_python(self, valor, estado):
        return valor.strip()
    
    def validate_python(self, valor, estado):
        resultado = DBSession.query(territorio.nombre).\
        filter(and_(territorio.territorio_id == valor, territorio.nivel == 1)).first()
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
    grado_de_instruccion = formencode.All(validators.UnicodeString(not_empty=True), GradoDeInstruccionValido())
    sexo = formencode.All(validators.UnicodeString(not_empty=True), SexoValido())
    fecha_de_nacimiento = formencode.All(validators.UnicodeString(not_empty=True), EdadValida())

class FormularioCrearUsuario(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    correo_electronico = formencode.All(validators.Email(resolve_domain=True), UsuarioUnico())
    contrasena = ContrasenaSegura()
    repetir_contrasena = validators.UnicodeString(not_empty=True)
    nombre = validators.UnicodeString(not_empty=True)
    apellido = validators.UnicodeString(not_empty=True)
    ubicacion = UbicacionExistente(not_empty=False)
    chained_validators = [validators.FieldsMatch('contrasena', 'repetir_contrasena')]

class FormularioCrearConsumidor(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    correo_electronico = formencode.All(validators.Email(resolve_domain=True), UsuarioUnico())
    contrasena = ContrasenaSegura()
    repetir_contrasena = validators.UnicodeString(not_empty=True)
    nombre = validators.UnicodeString(not_empty=True)
    apellido = validators.UnicodeString(not_empty=True)
    grado_de_instruccion = formencode.All(validators.UnicodeString(not_empty=True), GradoDeInstruccionValido())
    ubicacion = UbicacionExistente(not_empty=False)
    sexo = formencode.All(validators.UnicodeString(not_empty=True), SexoValido())
    fecha_de_nacimiento = EdadValida(not_empty=True)
    chained_validators = [validators.FieldsMatch('contrasena', 'repetir_contrasena')]

class FormularioCrearTienda(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    rif = formencode.All(validators.UnicodeString(not_empty=True), RifValido())
    nombre_legal = validators.UnicodeString(not_empty=True)
    nombre_comun = validators.UnicodeString(not_empty=True)
    categoria = formencode.All(validators.UnicodeString(not_empty=True), CategoriaValida())
    telefono = formencode.All(validators.UnicodeString(not_empty=True), validators.Regex(regex='^[1-9][0-9]{2}-[1-9][0-9]{6}$'))
    edificio = validators.UnicodeString(not_empty=False)
    piso = validators.UnicodeString(not_empty=False)
    apartamento = validators.UnicodeString(not_empty=False)
    local_no = validators.UnicodeString(not_empty=False)
    casa = validators.UnicodeString(not_empty=False)
    calle = validators.UnicodeString(not_empty=True)
    urbanizacion = validators.UnicodeString(not_empty=True)
    pagina_web = validators.UnicodeString(not_empty=False)
    facebook = validators.UnicodeString(not_empty=False)
    twitter = validators.UnicodeString(not_empty=False)
    correo_electronico_publico = validators.UnicodeString(not_empty=False)
    ubicacion = UbicacionExistente(not_empty=False)

class FormularioEditarUsuario(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    nombre = validators.UnicodeString(not_empty=True)
    apellido = validators.UnicodeString(not_empty=True)
    ubicacion = UbicacionExistente(not_empty=False)

class FormularioEditarConsumidor(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    grado_de_instruccion = GradoDeInstruccionValido(if_missing=None)
    sexo = SexoValido(if_missing=None)
    fecha_de_nacimiento = EdadValida(if_missing=None)

class FormularioEditarProducto(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    tipo_de_codigo = formencode.All(validators.UnicodeString(not_empty=True, max=7), TipoDeCodigoValido())
    codigo = validators.UnicodeString(not_empty=True, max=15)
    fabricante = validators.UnicodeString(not_empty=True, max=45)
    modelo = validators.UnicodeString(not_empty=False, max=45)
    nombre = validators.UnicodeString(not_empty=True, max=45)
    debut_en_el_mercado = validators.DateConverter(month_style='dd/mm/yyyy', not_empty=False)
    largo = validators.Number(not_empty=False)
    ancho = validators.Number(not_empty=False)
    alto = validators.Number(not_empty=False)
    peso = validators.Number(not_empty=False)
    pais_de_origen = PaisExistente(not_empty=False)

class FormularioEditarDireccion(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    edificio = validators.UnicodeString(not_empty=False)
    piso = validators.UnicodeString(not_empty=False)
    apartamento = validators.UnicodeString(not_empty=False)
    local_no = validators.UnicodeString(not_empty=False)
    casa = validators.UnicodeString(not_empty=False)
    calle = validators.UnicodeString(not_empty=True)
    urbanizacion = validators.UnicodeString(not_empty=True)
    ubicacion = UbicacionExistente(not_empty=False)