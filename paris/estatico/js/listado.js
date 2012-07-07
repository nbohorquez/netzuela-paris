/**
 * @author Nestor Bohorquez
 */

$(document).ready(function() {
	territorio.id = $('input[name=territorio_id]').val();
	$.getJSON('/territorio/terr' + territorio.id + 'niv0/coordenadas.json', function(data) {
		for (var j = 0; j < data.territorios[0].length; j++) {			
			var contorno = new Array();
			var coordenadas = data.territorios[0][j].split(' ');
			for (var k = 0; k < coordenadas.length; k++) {
				var pto = coordenadas[k].split(':');
				pto[0] = pto[0].replace(",", ".");
				pto[1] = pto[1].replace(",", ".");
				google_map.extender_borde(pto[0], pto[1]);
				var punto_gmap = new google.maps.LatLng(pto[0], pto[1]);
				contorno.push(punto_gmap);
			}
			territorio.contornos.push(contorno);
		}
		
		territorio.poligono = new google.maps.Polygon({
		    paths: territorio.contornos,
    		strokeColor: "#FF0000",
    		strokeOpacity: 0.8,
    		strokeWeight: 2,
    		fillColor: "#FF0000",
    		fillOpacity: 0.35
		});
		
		territorio.poligono.setMap(google_map.mapa);
	});
});

var territorio = {
	id: null,
	contornos: new Array(),
	poligono: null
};