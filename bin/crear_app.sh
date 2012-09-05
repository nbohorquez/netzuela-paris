#/bin/bash

wsgi_load="echo LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so >> /etc/apache2/mods-available/wsgi.load"

wsgi_conf="cat > /etc/apache2/mods-available/wsgi.conf << EOF
WSGIApplicationGroup %{GLOBAL}
WSGIPassAuthorization On
EOF
"

pyramid_wsgi="cat > env/pyramid.wsgi << EOF
from os import path
production_ini = path.abspath(path.join(path.dirname(__file__), 'production.ini'))
from pyramid.paster import get_app
application = get_app(production_ini, 'main')
EOF
"

apache_paris="cat > /etc/apache2/sites-available/paris << EOF
<VirtualHost *:80>
	ServerName www.netzuela.com
	ServerAdmin tca7410nb@gmail.com

	WSGIDaemonProcess pyramid processes=1 threads=4 python-path=/var/www/paris/lib/python2.7/site-packages
   	WSGIScriptAlias / /var/www/paris/pyramid.wsgi

	<Directory /var/www/paris>
		WSGIProcessGroup pyramid
		Order allow,deny
 		Allow from all
	</Directory>

	#ErrorLog ${APACHE_LOG_DIR}/paris_error.log
	ErrorLog /var/log/netzuela/paris_error.log
	# Possible values include: debug, info, notice, warn, error, crit,
	# alert, emerg.
	LogLevel warn

	#CustomLog ${APACHE_LOG_DIR}/paris_access.log combined
	CustomLog /var/log/netzuela/paris_access.log combined
</VirtualHost>
EOF
"

apache_redireccion="cat > /etc/apache2/sites-available/redireccion << EOF
<VirtualHost *:80>
	ServerName redireccion.netzuela.com
	ServerAlias netzuela.com
	Redirect / http://www.netzuela.com/
</VirtualHost>
EOF
"

crear_env() {
	virtualenv --no-site-packages --distribute env
	rm *.tar.gz
	source env/bin/activate
	cd ../src/paris
	pip install pyramid
	python setup.py install
	deactivate
	cd ../../bin
}

instalar_mod_wsgi() {
	wget https://modwsgi.googlecode.com/files/mod_wsgi-3.4.tar.gz
	tar -xvfz mod_wsgi-3.4.tar.gz
	cd mod_wsgi-3.4
	./configure
	make
	make install
	rm mod_wsgi-3.4.tar.gz
}

crear_archivo_wsgi_load() {
	if [ ! -f /etc/apache2/mods-available/wsgi.load ]; then
		sh -c "$wsgi_load"
	fi
	ln -s /etc/apache2/mods-available/wsgi.load /etc/apache2/mods-enabled/wsgi.load
}

crear_archivo_wsgi_conf() {
	if [ ! -f /etc/apache2/mods-available/wsgi.conf ]; then
		sh -c "$wsgi_conf"
	fi
	ln -s /etc/apache2/mods-available/wsgi.conf /etc/apache2/mods-enabled/wsgi.conf
}
crear_archivo_pyramid_wsgi() {
	sh -c "$pyramid_wsgi"
	chmod 755 env/pyramid.wsgi
}

crear_production_ini() {
	ln -s `pwd`/../src/paris/production.ini env/production.ini
}

crear_archivo_apache() {
	if [ ! -f /etc/apache2/sites-available/redireccion ]; then
		sh -c "$apache_paris"
	fi
	ln -s /etc/apache2/sites-available/paris /etc/apache2/sites-enabled/paris
}

crear_archivo_redireccion() {
	if [ ! -f /etc/apache2/sites-available/redireccion ]; then
		sh -c "$apache_redireccion"
	fi
	ln -s /etc/apache2/sites-available/redireccion /etc/apache2/sites-enabled/redireccion
}

configurar_var_www() {
	ln -s `pwd`/env/ /var/www/paris
}

if [ "$USER" != "root" ]; then
	echo "Error: Debe correr este script como root"
	exit 1;
fi
echo "Ejecutando script como root"

if [ ! -f env/bin/python ]; then
	echo "No existe el ambiente virtual, creandolo..."
	crear_env
fi
echo "Ambiente virtual creado"

if [ ! -f /usr/lib/apache2/modules/mod_wsgi.so ]; then
	echo "mod_wsgi no esta instalado, instalando..."
	instalar_mod_wsgi
fi
echo "mod_wsgi instalado"

if [ ! -f /etc/apache2/mods-enabled/wsgi.load ]; then
	echo "El archivo wsgi.load no existe, creandolo..."
	crear_archivo_wsgi_load
fi
echo "wsgi.load creado"

if [ ! -f /etc/apache2/mods-enabled/wsgi.conf ]; then
	echo "El archivo wsgi.conf no existe, creandolo..."
	crear_archivo_wsgi_conf
fi
echo "wsgi.conf creado"

if [ ! -f env/pyramid.wsgi ]; then
	echo "El archivo pyramid.wsgi no existe, creandolo..."
	crear_archivo_pyramid_wsgi
fi
echo "pyramid.wsgi creado"

if [ ! -f env/production.ini ]; then
	echo "El archivo production.ini no existe, creandolo..."
	crear_production_ini
fi
echo "production.ini creado"

if [ ! -f /etc/apache2/sites-available/paris ]; then
	echo "El archivo paris no existe, creandolo..."
	crear_archivo_apache
fi
echo "paris creado"

if [ ! -f /etc/apache2/sites-enabled/redireccion ]; then
	echo "El archivo redireccion no existe, creandolo..."
	crear_archivo_redireccion
fi
echo "redireccion creado"

if [ ! -L /var/www/paris ]; then
	echo "El directorio /var/www/ no esta configurado, trabajando..."
	configurar_var_www
fi
echo "Directorio /var/www/ configurado"

sudo service apache2 restart
