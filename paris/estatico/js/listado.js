/**
 * @author Nestor Bohorquez
 */

$(document).ready(function() {
	var terr = new Territorio({
		id: $('input[name=territorio_id]').val(),
		mapa: google_map,
		color: "#FF0000"
	});

	$.getJSON('/territorio/terr' + terr.id + 'niv0/coordenadas.json', function(data) {
		terr.nombre = data.territorios[0].nombre;
		var contornos = new Array();
		for (var j = 0, len_j = data.territorios[0].poligonos.length; j < len_j; j++) {			
			var contorno = new Array();
			var coordenadas = data.territorios[0].poligonos[j].split(' ');
			for (var k = 0, len_k = coordenadas.length; k < len_k; k++) {
				var pto = coordenadas[k].split(':');
				pto[0] = pto[0].replace(",", ".");
				pto[1] = pto[1].replace(",", ".");
				terr.mapa.extender_borde(pto[0], pto[1]);
				contorno.push(new google.maps.LatLng(pto[0], pto[1]));
			}
			contornos.push(contorno);
		}
		
		terr.crear_poligono(contornos);
	});
});