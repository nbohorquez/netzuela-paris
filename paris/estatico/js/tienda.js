/**
 * @author Nestor Bohorquez
 */

$(document).ready(function() {
	tienda.temporizador = setInterval(tienda.actualizar, 5000);
	tienda.id = $('input[name=tienda_id]').val();
	$.getJSON('/tienda_coordenadas.json', { tienda_id: tienda.id }, function(data) {
		for (var i = 0; i < data.puntos.length; i++) {
			var punto = new Array();
			punto['latitud'] = data.puntos[i].latitud.replace(",", ".");
			punto['longitud'] = data.puntos[i].longitud.replace(",", ".");
			google_map.extender_borde(punto['latitud'], punto['longitud']);
			tienda.puntos.push(punto);
		}
		google_map.agregar_marcador(tienda.puntos[0]['latitud'], tienda.puntos[0]['longitud']);		
	});
	
	$('a[rel="popover"]').popover();
});

$(window).unload(function() {
 	clearInterval(tienda.temporizador);
});

var tienda = {
	id: null,
	puntos: new Array(),
	temporizador: null
};

tienda.actualizar = function () {
	var dias = ["Domingo", "Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado"];
	var hoy = new Date();
	//var tienda = $('input[name=tienda_id]').val();
	
	$.getJSON('/tienda_turno.json', { dia: dias[hoy.getDay()], tienda_id: tienda.id }, function(data) {
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
}

function string2date(str) {
	var date = new Date();	
	date.setHours(str.substr(0,2));
 	date.setMinutes(str.substr(3,2));
 	date.setSeconds(str.substr(6,2));
 	return date;
}

function redondear(numero, decimales) {
	var uno = 10^decimales;
	return Math.round(numero*uno)/uno;
}