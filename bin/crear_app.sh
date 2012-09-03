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

function crear_env {
	virtualenv --no-site-packages --distribute env
	rm *.tar.gz
	source env/bin/activate
	cd ../src/paris
	pip install pyramid
	python setup.py install
	deactivate
	cd ../../bin
}

function instalar_mod_wsgi {
	wget https://modwsgi.googlecode.com/files/mod_wsgi-3.4.tar.gz
	tar -xvfz mod_wsgi-3.4.tar.gz
	cd mod_wsgi-3.4
	./configure
	make
	make install
	rm mod_wsgi-3.4.tar.gz

	if [ ! -f /etc/apache2/mods-enabled/wsgi.load ]
	then
		if [ ! -f /etc/apache2/mods-available/wsgi.load ]
		then
			sh -c "$wsgi_load"
		fi
		ln -s /etc/apache2/mods-available/wsgi.load /etc/apache2/mods-enabled/wsgi.load
	fi

	if [ ! -f /etc/apache2/mods-enabled/wsgi.conf ]
	then
		if [ ! -f /etc/apache2/mods-available/wsgi.conf ]
		then
			sh -c "$wsgi_conf"
		fi
		ln -s /etc/apache2/mods-available/wsgi.conf /etc/apache2/mods-enabled/wsgi.conf
	fi
}

function crear_archivo_wsgi {
	sh -c "$pyramid_wsgi"
	chmod 755 env/pyramid.wsgi
}

function crear_archivo_ini {
	ln -s `pwd`/../src/paris/production.ini env/production.ini
}

function crear_archivo_apache {
	if [ ! -f /etc/apache2/sites-available/redireccion ]
	then
		sh -c "$apache_paris"
	fi
	ln -s /etc/apache2/sites-available/paris /etc/apache2/sites-enabled/paris
}

function crear_archivo_redireccion {
	if [ ! -f /etc/apache2/sites-available/redireccion ]
	then
		sh -c "$apache_redireccion"
	fi
	ln -s /etc/apache2/sites-available/redireccion /etc/apache2/sites-enabled/redireccion
}

function configurar_var_www {
	ln -s `pwd`/env/ /var/www/paris
}

if [ "$USER" != "root" ]
then
	echo "Error: Debe correr este script como root"
	exit 1
fi

if [ ! -f env/bin/python ]
then
	echo "No existe el ambiente virtual, creandolo..."
	crear_env
	echo "Ambiente virtual creado"
fi

if [ ! -f /usr/lib/apache2/modules/mod_wsgi.so ]
then
	instalar_mod_wsgi
	echo "mod_wsgi instalado"
fi

if [ ! -f env/pyramid.wsgi ]
then
	crear_archivo_wsgi
	echo "Archivo wsgi creado"
fi

if [ ! -L env/production.ini ]
then
	crear_archivo_ini
	echo "Archivo de configuracion inicial copiado"
fi

if [ ! -f /etc/apache2/sites-available/paris ]
then
	crear_archivo_apache
	echo "Archivo de configuracion de apache creado"
fi

if [ ! -f /etc/apache2/sites-enabled/redireccion ]
then
	crear_archivo_redireccion
	echo "Archivo de redireccion creado"
fi

if [ ! -L /var/www/paris ]
then
	configurar_var_www
	echo "Directorio /var/www/ configurado"
fi

sudo service apache2 restart
