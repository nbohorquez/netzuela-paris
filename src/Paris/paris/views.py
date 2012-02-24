from pyramid.view import view_config
from .models import DBSession, Acceso

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
	accesos = DBSession.query(Acceso).all()
	return {'accesos': accesos}
