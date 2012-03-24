$(document).ready(function() {
	var latLng = new google.maps.LatLng(10.40, -71.44);
  	google_map.inicializar('#mapa', latLng, 11);
});

var google_map = {
  	mapa: null
}

google_map.inicializar = function(ubicacion, latLng, zoom) {
	var opciones = {
	    zoom:zoom,
	    center: latLng,
	    mapTypeId: google.maps.MapTypeId.ROADMAP
  	}
  	this.mapa = new google.maps.Map($(ubicacion)[0], opciones);
	//this.bounds = new google.maps.LatLngBounds();
}

google_map.marcador = function(latitud, longitud) {
	var punto = new google.maps.LatLng(parseFloat(latitud),parseFloat(longitud));
	var marcador = new google.maps.Marker({
		position: punto,
		map: google_map.mapa
	});
	/*
	var infoWindow = new google.maps.InfoWindow();
	var html='<strong>'+name+'</strong.><br />'+address;
	google.maps.event.addListener(marker, 'click', function() {
		infoWindow.setContent(html);
		infoWindow.open(MYMAP.map, marker);
	});
	MYMAP.map.fitBounds(MYMAP.bounds);
	*/
}

$('#gadget_colapsable').on('hidden', function () {
	$("#gadget").css({'height':'auto'});
	google.maps.event.trigger(google_map.mapa, 'resize');
})

$('#gadget_colapsable').on('show', function () {
	$("#gadget").css({'height':'40%'});
	$("#mapa").height($("#gadget").height() - $("#gadget_encabezado").height());
	google.maps.event.trigger(google_map.mapa, 'resize');
})