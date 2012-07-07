/**
 * @author Nestor Bohorquez
 */

$(document).ready(function() {
	var latLng = new google.maps.LatLng(10.40, -71.44);
  	google_map.inicializar('#mapa', latLng, 11);
});

var google_map = {
  	mapa: null,
  	geocodificador: null,
  	borde: null,
  	estilos : [{
	    featureType: "road",
	    stylers: [
	    	{ visibility: "off" }
	    ]
	},{
		featureType: "poi",
	    stylers: [
	    	{ visibility: "off" }
	    ]
	},{
		featureType: "transit",
	    stylers: [
	    	{ visibility: "off" }
	    ]
	}]
};

google_map.inicializar = function(ubicacion, latLng, zoom) {
	var opciones = {
	    zoom: zoom,
	    center: latLng,
	    mapTypeId: google.maps.MapTypeId.ROADMAP,
	    styles: google_map.estilos
  	};
  	this.mapa = new google.maps.Map($(ubicacion)[0], opciones);
  	this.geocodificador = new google.maps.Geocoder();
	this.borde = new google.maps.LatLngBounds();
}

google_map.agregar_marcador = function(latitud, longitud) {
	var punto = new google.maps.LatLng(latitud,longitud);
	var marcador = new google.maps.Marker({
		position: punto,
		map: this.mapa
	});
	this.extender_borde(latitud, longitud);
}

google_map.extender_borde = function(latitud, longitud) {
	var punto = new google.maps.LatLng(latitud,longitud);
	this.borde.extend(punto);
}

google_map.ajustar_borde = function() {
	this.mapa.fitBounds(this.borde);
}