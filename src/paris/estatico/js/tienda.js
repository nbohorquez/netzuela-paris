/**
 * @author Nestor Bohorquez
 */

function Tienda (opciones) {
    this.id = ('id' in opciones) ? opciones.id : null;
    this.puntos = ('puntos' in opciones) ? opciones.puntos : new Array();
    var intervalo = ('temporizador' in opciones) ? opciones.temporizador : null;
    var contexto = this;
    this.temporizador = setInterval(function () { Tienda.prototype.actualizar.call(contexto); }, intervalo);
}

Tienda.prototype.actualizar = function () {
    var dias = ["Domingo", "Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado"];
    var hoy = new Date();
    var milisegundos_a_horas = 1/(1000*60*60);

    $.getJSON('/tienda/' + this.id + '/turno.json', { dia: dias[hoy.getDay()] }, function (data) {
        var porcentaje;
        var comentario = '';

        var inicio_dia = new Date();
        inicio_dia.setHours(0);
        inicio_dia.setMinutes(0);
        inicio_dia.setSeconds(0);
        inicio_dia = inicio_dia.getTime();
        
        var ahorita = new Date().getTime() - inicio_dia;
        ahorita = redondear(ahorita * milisegundos_a_horas, 2);
        
        var turno = null;
        var apertura = new Array();
        var cierre = new Array(); 
        
        /* Revisamos cual de los turnos que nos envian es el que aplica para la hora actual */
        for (var i = 0, len_data = data.length; i < len_data; i++) {
            tmp_apertura = string2date(data[i].apertura).getTime() - inicio_dia;
            tmp_cierre = string2date(data[i].cierre).getTime() - inicio_dia;
            apertura.push(redondear(tmp_apertura * milisegundos_a_horas, 0));
            cierre.push(redondear(tmp_cierre * milisegundos_a_horas, 0));

            if (ahorita < apertura[i] || (ahorita < cierre[i] && ahorita >= apertura[i])) {
                turno = i;
                break;
            }
            else if (ahorita >= cierre[i] && (i == len_data - 1)) {
                turno = i;
                break;
            }
        }

        /* Tomamos el turno pertinente */
        apertura = apertura[turno];
        cierre = cierre[turno];

        /* Logica de la barra de turno */
        if (cierre == apertura) {
            porcentaje = 0;
            comentario = 'Hoy no abre la tienda';
        }
        else if (ahorita < apertura) {
            porcentaje = 0;
            var minutos = ((apertura - ahorita) % 1);
            var horas = (apertura - ahorita) - minutos;
            
            if (horas > 0) {
                comentario = horas.toString() + 'h';
            }
             
            comentario +=  Math.floor(minutos * 60).toString() + 'min para que abra';
        }
        else if (ahorita >= cierre) {
            porcentaje = 100;
            comentario = 'Turno terminado';
        }
        else if (ahorita < cierre && ahorita >= apertura) {
            porcentaje = (100/(cierre - apertura)) * ahorita - 100;
            var minutos = ((cierre - ahorita) % 1);
            var horas = (cierre - ahorita) - minutos;
            
            if (horas > 0) {
                comentario = horas.toString() + 'h';
            }
            
            comentario += Math.floor(minutos * 60).toString() + 'min para que cierre';
        }
        
        $('#comentario_turno').text(comentario);
        $("#barra_de_turno").css({'width': porcentaje.toString() + "%"});
    });
    
    function string2date (str) {
        var date = new Date();
        date.setHours(str.substr(0,2));
        date.setMinutes(str.substr(3,2));
        date.setSeconds(str.substr(6,2));
        return date;
    }
    
    function redondear (numero, decimales) {
        return parseFloat(new Number(numero+'').toFixed(parseInt(decimales)));
    }
}

$(document).ready(function () {
    var tienda = new Tienda({
        id: $('input[name=tienda_id]').val(),
        temporizador: 60000
    });
    
    tienda.actualizar();
    $('#mapa').dibujar_poligono_tienda(tienda.id);
});

$(window).unload(function () {
    clearInterval(tienda.temporizador);
});