#!/bin/bash

source color-echo.sh

archivo_config="config.ini"

parse_config() {
    if [ ! -f "$1" ]; then
        error "$1 no existe"
        return 1
    fi

    # Hay muchas formas de leer un config file sin usar source:
    # http://stackoverflow.com/questions/4434797/read-a-config-file-in-bash-without-using-source
    while read linea; do
    if [[ "$linea" =~ ^[^#]*= ]]; then
        variable=`echo $linea | cut -d'=' -f 1 | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//'`
        #variable=`echo $linea | cut -d'=' -f 1 | tr -d ' '`
        valor=`echo $linea | cut -d'=' -f 2- | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//'`
        #valor=`echo $linea | cut -d'=' -f 2- | tr -d ' '`
        eval "$variable"="'$valor'"
    fi
    done < "$1"
}

crear_env() {
    alias rollback="rm -rf env 2>/dev/null; return 1"

    if [ ! -f env/bin/python ]; then
        virtualenv --no-site-packages --distribute env 2>&1 || rollback
        rm *.tar.gz 2>/dev/null
    fi
    
    # Instalamos el site-package de spuria
    source ../../spuria/bin/env/bin/activate
    spuria_site_packages="`python -c "import distutils; print(distutils.sysconfig.get_python_lib())"`"
    deactivate

    source env/bin/activate
    paris_site_packages="`python -c "import distutils; print(distutils.sysconfig.get_python_lib())"`"
    spuria_pth="$paris_site_packages/_spuria.pth"
    deactivate

    echo "import sys; sys.__plen = len(sys.path)" > "$spuria_pth" || rollback
    for i in $( find "$spuria_site_packages" -maxdepth 1 -type d )
    do
        if [ ! "$i" == "$spuria_site_packages" ]; then
            echo "$i" >> "$spuria_pth" || rollback
        fi
    done
    echo "import sys; new=sys.path[sys.__plen:]; del sys.path[sys.__plen:]; p=getattr(sys,'__egginsert',0); sys.path[p:p]=new; sys.__egginsert = p+len(new)" >> "$spuria_pth" || rollback

    # Instalamos pyramid
    source env/bin/activate
    easy_install -U distribute || { deactivate; rollback; }
    pip install pyramid || { deactivate; rollback; }
    pip install python-dateutil || { deactivate; rollback; }

    # Instalamos paris
    dir=`pwd`
    cd ../src/
    python setup.py install || { deactivate; cd "$dir"; rollback; }
    deactivate
    cd "$dir"
}

abortar() {
    echo "ERROR: $1. Abortando"
    exit 1
}
