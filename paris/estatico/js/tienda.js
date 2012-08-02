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
		
		var apertura = string2date(data.apertura).getTime() - inicio_dia;
		var cierre = string2date(data.cierre).getTime() - inicio_dia;
		var ahorita = new Date().getTime() - inicio_dia;
		
		apertura = redondear(apertura * milisegundos_a_horas, 0);
		cierre = redondear(cierre * milisegundos_a_horas, 0);
		ahorita = redondear(ahorita * milisegundos_a_horas, 2);

		if (cierre == apertura || ahorita < apertura) {
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

	// Esto activa los popover sobre los dias de la semana en el horario de la tienda
	$('a[rel="popover"]').popover();
});

$(window).unload(function () {
 	clearInterval(tienda.temporizador);
});