/**
 * @author Nestor Bohorquez
 */

$(document).ready(function() {
	var latLng = new google.maps.LatLng(10.40, -71.44);
  	google_map.inicializar('#mapa', latLng, 11);
});

var google_map = {
	infobox: null,
	infobox_abierto: false,
	malla: null,
	cursor: null,
  	mapa: null,
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
	},{
		featureType: "administrative.province",
	    stylers: [
	    	{ visibility: "off" }
	    ]
	}]
};

google_map.inicializar = function(ubicacion, latLng, zoom) {
	var infobox_posicion = new google.maps.Point(80, 230);
	var contexto = this;
	var opciones = {
	    zoom: zoom,
	    center: latLng,
	    mapTypeId: google.maps.MapTypeId.ROADMAP,
	    styles: google_map.estilos
  	};
  	
  	this.mapa = new google.maps.Map($(ubicacion)[0], opciones);
	this.borde = new google.maps.LatLngBounds();

    this.malla = new google.maps.OverlayView();
	this.malla.draw = function() {};
	this.malla.setMap(this.mapa);
	
	this.infobox = new InfoBox({
		content: '',
		disableAutoPan: false,
		zIndex: null,
		closeBoxURL: "",
		boxStyle: { width: "280px" },
		closeBoxMargin: "10px 2px 2px 2px",
		infoBoxClearance: new google.maps.Size(1, 1),
		isHidden: false,
		pane: "floatPane",
		enableEventPropagation: false,
	});
	
	google.maps.event.addListener(this.mapa, 'bounds_changed', function(event) {
		contexto.infobox.setPosition(contexto.malla.getProjection().fromContainerPixelToLatLng(infobox_posicion));
	});
		
	google.maps.event.addListener(this.mapa, 'mousemove', function(event) {
		contexto.cursor = event.latLng;
	});
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