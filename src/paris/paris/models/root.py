'''
Created on 31/07/2012

@author: nestor
'''

from pyramid.security import Allow

class RootFactory(object):
    # Los 'autorizados' tienen permitido 'entrar' 
    __acl__ = [ (Allow, 'autorizados', 'entrar') ]
    
    def __init__(self, request):
        pass