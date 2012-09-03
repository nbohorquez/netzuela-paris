# -*- coding: utf-8 -*-
'''
Created on 07/06/2012

@author: nestor
'''

from paris.models.spuria import acceso, DBSession

def obtener_grupos(usuario, peticion):
    tmp = DBSession.query(acceso).filter_by(correo_electronico = usuario).first()
    return ['autorizados'] if (tmp is not None) else None
