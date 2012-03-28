/**
 * @author Nestor Bohorquez
 */

$(document).ready(function() {
	var latLng = new google.maps.LatLng(10.40, -71.44);
  	google_map.inicializar('#mapa', latLng, 11);
});

var google_map = {
  	mapa: null,
  	borde: null
}

google_map.inicializar = function(ubicacion, latLng, zoom) {
	var opciones = {
	    zoom:zoom,
	    center: latLng,
	    mapTypeId: google.maps.MapTypeId.ROADMAP
  	}
  	this.mapa = new google.maps.Map($(ubicacion)[0], opciones);
	this.borde = new google.maps.LatLngBounds();
}

google_map.agregar_marcador = function(latitud, longitud) {
	var punto = new google.maps.LatLng(parseFloat(latitud),parseFloat(longitud));
	var marcador = new google.maps.Marker({
		position: punto,
		map: this.mapa
	});
	this.borde.extend(punto);
}

google_map.ajustar_mapa = function() {
	this.mapa.fitBounds(this.borde);
}

$('#gadget_colapsable').on('hidden', function () {
	$("#gadget").css({'height':'auto'});
	google.maps.event.trigger(google_map.mapa, 'resize');
})

$('#gadget_colapsable').on('show', function () {
	$("#gadget").css({'height':'40%'});
	$("#mapa").height($("#gadget").height() - $("#gadget_encabezado").height());
	google.maps.event.trigger(google_map.mapa, 'resize');
	
	if (google_map.borde != null) {
		google_map.ajustar_mapa();
	}
})