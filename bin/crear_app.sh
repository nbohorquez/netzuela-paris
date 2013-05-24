#!/bin/bash

source comunes.sh
parse_config "$archivo_config" || warning "Advertencia: error al leer $archivo_config"

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

instalar_mod_wsgi () {
    if [ -f "$mod_wsgi_so" ]; then
        return 0
    fi

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

    if [ ! -f "$mod_wsgi_so" ]; then
        return 1
    else
        return 0
    fi
}

crear_archivo_wsgi_load () {
    rm "$wsgi_load_available" 2>/dev/null
    rm "$wsgi_load_enabled" 2>/dev/null 
    bash -c "$wsgi_load"
    ln -s "$wsgi_load_available" "$wsgi_load_enabled"
    if [ ! -f "$wsgi_load_available" -o ! -f $wsgi_load_enabled ]; then
        return 1
    fi
    return 0
}

crear_archivo_wsgi_conf () {
    rm "$wsgi_conf_available" 2>/dev/null
    rm "$wsgi_conf_enabled" 2>/dev/null 
    bash -c "$wsgi_conf"
    ln -s "$wsgi_conf_available" "$wsgi_conf_enabled"
    if [ ! -f "$wsgi_conf_available" -o ! -f $wsgi_conf_enabled ]; then
        return 1
    fi
    return 0
}

crear_archivo_pyramid_wsgi () {
    rm env/pyramid.wsgi 2>/dev/null
    bash -c "$pyramid_wsgi"
    if [ ! -f env/pyramid.wsgi ]; then
        return 1
    fi
    chmod 755 env/pyramid.wsgi
    return 0
}

crear_archivo_production_ini () {
    rm env/production.ini 2>/dev/null
    src_production_ini=`pwd`/../src/production.ini 
    ln -s "$src_production_ini" env/production.ini
    if [ ! -f env/production.ini -o ! -f "$src_production_ini" ]; then
        return 1
    fi
    return 0
}

crear_archivo_apache () {
    rm "$paris_available" 2>/dev/null 
    rm "$paris_enabled" 2>/dev/null 
    bash -c "$apache_paris"
    ln -s "$paris_available" "$paris_enabled"
    if [ ! -f "$paris_available" -o ! -f "$paris_enabled" ]; then
        return 1
    fi
    return 0
}

crear_archivo_redireccion () {
    rm "$redireccion_available" 2>/dev/null 
    rm "$redireccion_enabled" 2>/dev/null 
    bash -c "$apache_redireccion"
    ln -s "$redireccion_available" "$redireccion_enabled"
    if [ ! -f "$redireccion_available" -o ! -f "$redireccion_enabled" ]; then
        return 1
    fi
    return 0
}

configurar_var_www () {
    rm "$dir_simbolico_www" 2>/dev/null
    ln -s `pwd`/env/ "$dir_simbolico_www"
    if [ ! -L "$dir_simbolico_www" ]; then
        return 1
    fi
    return 0
}

if [ "$USER" != "root" ]; then
    abortar "Error: Debe correr este script como root"
fi
info "Ejecutando script como root"

crear_env || abortar "No se pudo crear el ambiente virtual"
#if [ ! -f env/bin/python ]; then
#    echo "No existe el ambiente virtual, creandolo..."
#    crear_env
#fi
info "Ambiente virtual creado"

instalar_mod_wsgi || {
    abortar "No se pudo instalar mod_wsgi en el servidor apache"
}
#if [ ! -f "$mod_wsgi_so" ]; then
#    echo "mod_wsgi no esta instalado, instalando..."
#    instalar_mod_wsgi
#fi
info "mod_wsgi instalado"

crear_archivo_wsgi_load || {
    abortar "No se pudo crear el archivo $wsgi_load_enabled"
}
#if [ ! -f "$wsgi_load_enabled" ]; then
#    echo "El archivo wsgi.load no existe, creandolo..."
#    crear_archivo_wsgi_load
#fi
info "$wsgi_load_enabled creado"

crear_archivo_wsgi_conf || {
    abortar "No se pudo crear el archivo $wsgi_conf_enabled"
}
#if [ ! -f "$wsgi_conf_enabled" ]; then
#    echo "El archivo wsgi.conf no existe, creandolo..."
#    crear_archivo_wsgi_conf
#fi
info "$wsgi_conf_enabled creado"

crear_archivo_pyramid_wsgi || {
    abortar "No se pudo crear el archivo env/pyramid.wsgi"
}
#if [ ! -f env/pyramid.wsgi ]; then
#    echo "El archivo pyramid.wsgi no existe, creandolo..."
#    crear_archivo_pyramid_wsgi
#fi
info "env/pyramid.wsgi creado"

crear_archivo_production_ini || {
    abortar "No se pudo crear el archivo env/production.ini"
}
#if [ ! -f env/production.ini ]; then
#    echo "El archivo production.ini no existe, creandolo..."
#    crear_archivo_production_ini
#fi
info "env/production.ini creado"

rm "$sitio_dummy" 2>/dev/null
#if [ -f "$sitio_dummy" ]; then
#    echo "El sitio por defecto existe, borrandolo..."
#    rm "$sitio_dummy" 
#fi
info "sitio por defecto borrado"

crear_archivo_apache || { 
    abortar "No se pudo crear el archivo $paris_enabled"
}
#if [ ! -f "$paris_enabled" ]; then
#    echo "El archivo paris no existe, creandolo..."
#    crear_archivo_apache
#fi
info "$paris_enabled creado"

crear_archivo_redireccion || { 
    abortar "No se pudo crear el archivo $redireccion_enabled"
}
#if [ ! -f "$redireccion_enabled" ]; then
#    echo "El archivo redireccion no existe, creandolo..."
#    crear_archivo_redireccion
#fi
info "$redireccion_enabled creado"

configurar_var_www || {
    abortar "No se pudo crear el directorio simbolico $dir_simbolico_www"
}
# if [ ! -L "$dir_simbolico_www" ]; then
#    echo "El directorio /var/www/ no esta configurado, trabajando..."
#    configurar_var_www
#fi
info "Directorio simbolico $dir_simbolico_www configurado"

sudo service apache2 restart
exit 0
