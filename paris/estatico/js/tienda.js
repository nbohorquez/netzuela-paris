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

	$.getJSON('/tienda/' + this.id + '/turno.json', { dia: dias[hoy.getDay()] }, function (data) {
		var milisegundos_a_horas = 1/(1000*60*60);
		var porcentaje;

		var inicio_dia = new Date();
		inicio_dia.setHours(0);
		inicio_dia.setMinutes(0);
		inicio_dia.setSeconds(0);
		inicio_dia = inicio_dia.getTime()*milisegundos_a_horas;
		
		var apertura = string2date(data.apertura).getTime()*milisegundos_a_horas - inicio_dia;
		var cierre = string2date(data.cierre).getTime()*milisegundos_a_horas - inicio_dia;
		var ahorita = new Date().getTime()*milisegundos_a_horas - inicio_dia;
		
		apertura = redondear(apertura, 2);
		cierre = redondear(cierre, 2);
		ahorita = redondear(ahorita, 2);
		
		if (cierre == apertura || ahorita < apertura) {
			porcentaje = 0;
		}
		else if (ahorita >= cierre) {
			porcentaje = 100;
		}
		else if (ahorita < cierre && ahorita >= apertura) {
	 		porcentaje = (100/(cierre - apertura)) * ahorita - 100;
		}
		
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
		var uno = 10^decimales;
		return Math.round(numero*uno)/uno;
	}
}

$(document).ready(function () {
	var tienda = new Tienda({
		id: $('input[name=tienda_id]').val(),
		temporizador: 60000
	});
	
	tienda.actualizar();
	$('#mapa').dibujar_poligono_tienda(tienda.id);

	// Esto activa los popover sobre los dias de la semana en el horario de la tienda
	$('a[rel="popover"]').popover();
});

$(window).unload(function () {
 	clearInterval(tienda.temporizador);
});