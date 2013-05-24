#!/bin/bash

# Tomado de http://tldp.org/LDP/abs/html/colorizing.html
black='\E[30;40m'
red='\E[31;40m'
green='\E[32;40m'
yellow='\E[33;40m'
blue='\E[34;40m'
magenta='\E[35;40m'
cyan='\E[36;40m'
white='\E[37;40m'

cecho() {
    local default_msg="Sin mensaje para mostrar"

    message=${1:-$default_msg}   # Defaults to default message.
    color=${2:-$black}           # Defaults to black, if not specified.

    echo -e "$color""$message"
    #echo -ne \E[0m
    tput sgr0

    return
}

info() {
    cecho "$1" "$green"
}

warning() {
    cecho "$1" "$yellow"
}

debug() {
    cecho "$1" "$blue"
}

error() {
    cecho "$1" "$red"
}
