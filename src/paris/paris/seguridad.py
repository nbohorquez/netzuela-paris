# -*- coding: utf-8 -*-
'''
Created on 07/06/2012

@author: nestor
'''

#from paris.models.spuria import acceso, DBSession
from spuria.orm import Acceso, DBSession

def obtener_grupos(usuario, peticion):
    # Hasta ahorita simplemente decimos que cualquier persona registrada en la 
    # base de datos pertenece al grupo de los 'autorizados'
    tmp = DBSession.query(Acceso).filter_by(correo_electronico = usuario).first()
    return ['autorizados'] if (tmp is not None) else None
