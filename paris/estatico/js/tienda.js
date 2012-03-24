$(document).ready(function() {
	var actualizar_periodico = setInterval(tienda.actualizar, 5000);
	tienda.temporizador = $('input[name=tienda_id]').val();
	$.getJSON('/tienda_coordenadas.json', { tienda_id: tienda }, function(data) {
		var latitud = parseFloat(data.latitud.replace(",", "."));
		var longitud = parseFloat(data.longitud.replace(",", "."));
		google_map.marcador(latitud, longitud);
	});
});

$(window).unload(function() {
 	clearInterval(tienda.temporizador);
});

var tienda = {
	temporizador: null
}

tienda.actualizar = function () {
	var dias = ["Domingo", "Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado"];
	var hoy = new Date();
	var tienda = $('input[name=tienda_id]').val();
	
	$.getJSON('/tienda_turno.json', { dia: dias[hoy.getDay()], tienda_id: tienda }, function(data) {
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
		else if (ahorita < cierre && ahorita >= apertura ) {
	 		porcentaje = (100/(cierre - apertura)) * ahorita - 100;
		}
		
        document.getElementById("barra_de_turno").style.width = porcentaje.toString() + "%";
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