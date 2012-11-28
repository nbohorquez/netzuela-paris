#!/bin/bash

sitio_dummy="/etc/apache2/sites-enabled/000-default"
dir_log="/var/log/netzuela"
dir_simbolico_www="/var/www/paris"
paris_available="/etc/apache2/sites-available/paris"
paris_enabled="/etc/apache2/sites-enabled/paris"
redireccion_available="/etc/apache2/sites-available/redireccion"
redireccion_enabled="/etc/apache2/sites-enabled/redireccion"
wsgi_load_available="/etc/apache2/mods-available/wsgi.load"
wsgi_load_enabled="/etc/apache2/mods-enabled/wsgi.load"
wsgi_conf_available="/etc/apache2/mods-available/wsgi.conf"
wsgi_conf_enabled="/etc/apache2/mods-enabled/wsgi.conf"
mod_wsgi_so="/usr/lib/apache2/modules/mod_wsgi.so"
wsgi_load="echo LoadModule wsgi_module $mod_wsgi_so >> $wsgi_load_available"
wsgi_conf="cat > $wsgi_conf_available << EOF
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
apache_paris="cat > $paris_available << EOF
<VirtualHost *:80>
    ServerName www.netzuela.com
    ServerAdmin tca7410nb@gmail.com

    WSGIDaemonProcess pyramid processes=1 threads=4 python-path=$dir_simbolico_www/lib/python2.7/site-packages
    WSGIScriptAlias / $dir_simbolico_www/pyramid.wsgi

    <Directory $dir_simbolico_www>
        WSGIProcessGroup pyramid
        Order allow,deny
        Allow from all
    </Directory>

    #ErrorLog \${APACHE_LOG_DIR}/paris_error.log
    ErrorLog $dir_log/paris_error.log
    # Possible values include: debug, info, notice, warn, error, crit,
    # alert, emerg.
    LogLevel warn

    #CustomLog \${APACHE_LOG_DIR}/paris_access.log combined
    CustomLog $dir_log/paris_access.log combined
</VirtualHost>
EOF
"
apache_redireccion="cat > $redireccion_available << EOF
<VirtualHost *:80>
    ServerName redireccion.netzuela.com
    ServerAlias netzuela.com
    Redirect / http://www.netzuela.com/
</VirtualHost>
EOF
"

crear_env () {
    virtualenv --no-site-packages --distribute env
    rm *.tar.gz
    dir=`pwd`
    source env/bin/activate
    easy_install -U distribute
    pip install pyramid
    cd ../src/paris
    python setup.py develop
    cd "$pwd"
    cd ../../spuria/src/orm
    python setup.py develop
    deactivate
    cd "$pwd"
}

instalar_mod_wsgi () {
    dir=`pwd`
    cd /tmp
    wget https://modwsgi.googlecode.com/files/mod_wsgi-3.4.tar.gz
    tar -xvf mod_wsgi-3.4.tar.gz
    cd mod_wsgi-3.4
    ./configure
    make
    make install
    cd ..
    rm mod_wsgi-3.4.tar.gz
    rm -rf mod_wsgi-3.4
    cd "$dir"
}

crear_archivo_wsgi_load () {
    if [ ! -f "$wsgi_load_available" ]; then
        bash -c "$wsgi_load"
    fi
    ln -s "$wsgi_load_available" "$wsgi_load_enabled"
}

crear_archivo_wsgi_conf () {
    if [ ! -f "$wsgi_conf_available" ]; then
        bash -c "$wsgi_conf"
    fi
    ln -s "$wsgi_conf_available" "$wsgi_conf_enabled"
}

crear_archivo_pyramid_wsgi () {
    bash -c "$pyramid_wsgi"
    chmod 755 env/pyramid.wsgi
}

crear_archivo_production_ini () {
    ln -s `pwd`/../src/paris/production.ini env/production.ini
}

crear_archivo_apache () {
    if [ ! -f "$paris_available" ]; then
        bash -c "$apache_paris"
    fi
    ln -s "$paris_available" "$paris_enabled"
}

crear_archivo_redireccion () {
    if [ ! -f "$redireccion_available" ]; then
        bash -c "$apache_redireccion"
    fi
    ln -s "$redireccion_available" "$redireccion_enabled"
}

configurar_var_www () {
    ln -s `pwd`/env/ "$dir_simbolico_www"
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

if [ ! -f "$mod_wsgi_so" ]; then
    echo "mod_wsgi no esta instalado, instalando..."
    instalar_mod_wsgi
fi
echo "mod_wsgi instalado"

if [ ! -f "$wsgi_load_enabled" ]; then
    echo "El archivo wsgi.load no existe, creandolo..."
    crear_archivo_wsgi_load
fi
echo "wsgi.load creado"

if [ ! -f "$wsgi_conf_enabled" ]; then
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
    crear_archivo_production_ini
fi
echo "production.ini creado"

if [ -f "$sitio_dummy" ]; then
    echo "El sitio por defecto existe, borrandolo..."
    rm "$sitio_dummy" 
fi
echo "sitio por defecto borrado"

if [ ! -f "$paris_enabled" ]; then
    echo "El archivo paris no existe, creandolo..."
    crear_archivo_apache
fi
echo "paris creado"

if [ ! -f "$redireccion_enabled" ]; then
    echo "El archivo redireccion no existe, creandolo..."
    crear_archivo_redireccion
fi
echo "redireccion creado"

if [ ! -L "$dir_simbolico_www" ]; then
    echo "El directorio /var/www/ no esta configurado, trabajando..."
    configurar_var_www
fi
echo "Directorio /var/www/ configurado"

sudo service apache2 restart
exit 0
