/**
 * @author Nestor Bohorquez
 */

var tiendas = [];

function Tienda (opciones) {
    EventObject.call(this);
    
    this.id = ('id' in opciones) ? opciones.id : null;
    //this.puntos = ('puntos' in opciones) ? opciones.puntos : new Array();
    this.coordenadas = this.marcador = this.turnos = null;
}

Tienda.prototype = new EventObject();
Tienda.prototype.constructor = Tienda;

Tienda.prototype.actualizar_turno = function () {
    var contexto = this;
    
    var milisegundos_a_horas = 1/(1000*60*60);
    var inicio_dia = new Date();
    inicio_dia.setHours(0);
    inicio_dia.setMinutes(0);
    inicio_dia.setSeconds(0);
    inicio_dia = inicio_dia.getTime();
    
    var ahorita = new Date().getTime() - inicio_dia;
    ahorita = redondear(ahorita * milisegundos_a_horas, 2);
    
    if (!this.turnos) {
        this.turnos = [];
        var dias = ["Domingo", "Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado"];
        var hoy = new Date();
        
        $.getJSON('/tienda/' + this.id + '/turno.json', { dia: dias[hoy.getDay()] }, function (data) {
            for (var i = 0, len_data = data.length; i < len_data; i++) {
                tmp_apertura = string2date(data[i].apertura).getTime() - inicio_dia;
                tmp_cierre = string2date(data[i].cierre).getTime() - inicio_dia;
                turno = {
                    apertura: redondear(tmp_apertura * milisegundos_a_horas, 0),
                    cierre: redondear(tmp_cierre * milisegundos_a_horas, 0)
                };
                contexto.turnos.push(turno);
            }

            actualizar();
        });
    } else {
        actualizar();
    }
    
    function actualizar () {
        var porcentaje;
        var comentario = '';
        var turno = null;

        /* Revisamos cual de los turnos que nos envian es el que aplica para la hora actual */
        for (var i = 0, len_turnos = contexto.turnos.length; i < len_turnos; i++) {
            if (ahorita < contexto.turnos[i].apertura || (ahorita < contexto.turnos[i].cierre && ahorita >= contexto.turnos[i].apertura)) {
                turno = i;
                break;
            }
            else if (ahorita >= contexto.turnos[i].cierre && (i == len_turnos - 1)) {
                turno = i;
                break;
            }
        }
        
        /* Tomamos el turno pertinente */
        var apertura = contexto.turnos[turno].apertura;
        var cierre = contexto.turnos[turno].cierre;
        
        /* Logica de la barra de turno */
        if (cierre == apertura) {
            porcentaje = 0;
            comentario = 'Hoy no abre la tienda';
        } else if (ahorita < apertura) {
            porcentaje = 0;
            var minutos = ((apertura - ahorita) % 1);
            var horas = (apertura - ahorita) - minutos;
            
            if (horas > 0) {
                comentario = horas.toString() + 'h';
            }
             
            comentario +=  Math.floor(minutos * 60).toString() + 'min para que abra';
        } else if (ahorita >= cierre) {
            porcentaje = 100;
            comentario = 'Turno terminado';
        } else if (ahorita < cierre && ahorita >= apertura) {
            porcentaje = (100/(cierre - apertura)) * ahorita - 100;
            var minutos = ((cierre - ahorita) % 1);
            var horas = (cierre - ahorita) - minutos;
            
            if (horas > 0) {
                comentario = horas.toString() + 'h';
            }
            
            comentario += Math.floor(minutos * 60).toString() + 'min para que cierre';
        }
        
        contexto.raiseEvent('turno_actualizado', {
            comentario: comentario,
            porcentaje: porcentaje.toString()
        });
    }
    
    function string2date (str) {
        var date = new Date();
        date.setHours(str.substr(0,2));
        date.setMinutes(str.substr(3,2));
        date.setSeconds(str.substr(6,2));
        return date;
    }
    
    function redondear (numero, decimales) {
        return parseFloat(new Number(numero + '').toFixed(parseInt(decimales)));
    }
}

Tienda.prototype.obtener_coordenadas = function () {
    var contexto = this;
    $.getJSON('/tienda/' + this.id + '/coordenadas.json', function (data) {
        contexto.coordenadas = {
            latitud: data.puntos[0].latitud.replace(",", "."),
            longitud: data.puntos[0].longitud.replace(",", ".")
        };
        
        contexto.raiseEvent('coordenadas_obtenidas', {
            latitud: contexto.coordenadas.latitud,
            longitud: contexto.coordenadas.longitud
        });
    });
}

var icono_azul = new google.maps.MarkerImage(
    '/estatico/img/blue-dot.png',
    new google.maps.Size(32, 32),
    new google.maps.Point(0, 0),
    new google.maps.Point(16, 32)
);
var icono_rojo = new google.maps.MarkerImage(
    '/estatico/img/red-dot.png',
    new google.maps.Size(32, 32),
    new google.maps.Point(0, 0),
    new google.maps.Point(16, 32)
);
var sombra = new google.maps.MarkerImage(
    '/estatico/img/msmarker.shadow.png',
    new google.maps.Size(59, 32),
    new google.maps.Point(0, 0),
    new google.maps.Point(16, 32)
);

$(document).ready(function () {
    $('input[name=tienda_id]').each(function () {
        var tienda = new Tienda({id: $(this).val()});
        
        if (pagina == 'Tienda') {
            var contexto = tienda;
            var temporizador = setInterval(function () { 
                Tienda.prototype.actualizar_turno.call(contexto); 
            }, 60000);
            
            tienda.actualizar_turno();
            tienda.attachEvent('turno_actualizado', function (remitente, args) {
                $('#comentario_turno').text(args.comentario);
                $("#barra_de_turno").css({'width': args.porcentaje + "%"});
            });
        }

        tienda.obtener_coordenadas();
        tienda.attachEvent('coordenadas_obtenidas', function (remitente, args) {
            $('#mapa').dibujar_marcador({
                latitud: args.latitud,
                longitud: args.longitud,
                propietario: remitente,
                opciones: { 
                    icon: icono_rojo,
                    shadow: sombra
                }
            });

            // La propiedad 'marcador' no se crea aqui sino al llamar a la funcion
            // $.fn.dibujar_marcador de #mapa. Es feo y poco elegante... hay que
            // cambiarlo despues            
            google.maps.event.addListener(remitente.marcador, "mouseover", function () {
                remitente.marcador.setOptions({
                    icon: icono_azul,
                    shadow: sombra
                });
            });
            
            google.maps.event.addListener(remitente.marcador, "mouseout", function () {
                remitente.marcador.setOptions({
                    icon: icono_rojo,
                    shadow: sombra
                });
            });
            
            google.maps.event.addListener(remitente.marcador, "click", function () {
                $('input[name=tienda_id][value=' + remitente.id + ']').each(function () {
                    var $fila = $(this).parents('tr:first');
                    var $tbody = $(this).parents('tbody:first');
                    $tbody.prepend($fila);
                });
            });
        });
    });
});

$(window).unload(function () {
    for (var i = 0, len_tiendas = tiendas.length; i < len_tiendas; i++) {
        clearInterval(tiendas[i].temporizador);
    }
});