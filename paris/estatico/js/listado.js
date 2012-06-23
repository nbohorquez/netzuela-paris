/**
 * @author Nestor Bohorquez
 */

$(document).ready(function() {
	territorio.id = $('input[name=territorio_id]').val();
	$.getJSON('/territorio/' + territorio.id + '/coordenadas.json', function(data) {
		for (var i = 0; i < data.poligonos.length; i++) {
			var poligono = new Array();
			for (var j = 0; j < data.poligonos[i].length; j++) {
				var punto = new Array();
				punto['latitud'] = data.poligonos[i][j].latitud.replace(",", ".");
				punto['longitud'] = data.poligonos[i][j].longitud.replace(",", ".");
				google_map.extender_borde(punto['latitud'], punto['longitud']);
				var punto_gmap = new google.maps.LatLng(punto['latitud'], punto['longitud']);
				poligono.push(punto_gmap);
			}
			
			var contorno = territorio.contorno = new google.maps.Polyline({
			    path: poligono,
			    strokeColor: "#FF0000",
			    strokeOpacity: 1.0,
			    strokeWeight: 2
			});
			contorno.setMap(google_map.mapa);
			
			territorio.poligonos.push(poligono);
			territorio.contornos.push(contorno);
		}
	});
});

var territorio = {
	id: null,
	poligonos: new Array(),
	contornos: new Array()
};