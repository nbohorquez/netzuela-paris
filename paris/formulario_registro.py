# -*- coding: utf-8 -*-
'''
Created on 19/06/2012

@author: nestor
'''

import formencode, re
from .constantes import EDAD_MINIMA
from .models import acceso, DBSession, grado_de_instruccion, sexo
from datetime import date, timedelta
from formencode import validators
from formencode.api import Invalid

class contrasena_segura(validators.FancyValidator):
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

class usuario_unico(validators.FancyValidator):
    mensaje = unicode('El usuario especificado ya existe en la base de datos', 'utf-8')
    
    def _to_python(self, valor, estado):
        return valor.strip()
    
    def validate_python(self, valor, estado):
        existe = DBSession.query(acceso).filter_by(correo_electronico = valor).first()
        if existe is not None:
            raise Invalid(self.mensaje, valor, estado)
    
class grado_de_instruccion_valido(validators.FancyValidator):
    mensaje = unicode('Grado de instrucción no conocido', 'utf-8')
    
    def _to_python(self, valor, estado):
        return valor.strip()
    
    def validate_python(self, valor, estado):
        resultados = DBSession.query(grado_de_instruccion.valor).all()
        grados = [resultado[0] for resultado in resultados]
        if valor not in grados:
            raise Invalid(self.mensaje, valor, estado)
    
class sexo_valido(validators.FancyValidator):
    mensaje = unicode('Sexo no conocido', 'utf-8')
    
    def _to_python(self, valor, estado):
        return valor.strip()
    
    def validate_python(self, valor, estado):
        resultados = DBSession.query(sexo.valor).all()
        sexos = [resultado[0] for resultado in resultados]
        if valor not in sexos:
            raise Invalid(self.mensaje, valor, estado)

class edad_valida(validators.FancyValidator):
    convertidor = validators.DateConverter(month_style='dd/mm/yyyy')
    validador = validators.DateValidator(latest_date=date.today()-timedelta(days=EDAD_MINIMA*365.24))
    
    def _to_python(self, valor, estado):
        return valor.strip()
    
    def validate_python(self, valor, estado):
        convertida = self.convertidor.to_python(valor)
        self.validador.to_python(convertida)
        
class formulario(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    correo_electronico = formencode.All(validators.Email(resolve_domain=True), usuario_unico())
    contrasena = contrasena_segura()
    repetir_contrasena = validators.String(not_empty=True)
    nombre = validators.String(not_empty=True)
    apellido = validators.String(not_empty=True)
    grado_de_instruccion = formencode.All(validators.String(not_empty=True), grado_de_instruccion_valido())
    sexo = formencode.All(validators.String(not_empty=True), sexo_valido())
    fecha_de_nacimiento = edad_valida()
    chained_validators = [validators.FieldsMatch('contrasena', 'repetir_contrasena')]