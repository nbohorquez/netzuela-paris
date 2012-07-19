/**
 * @author Nestor Bohorquez
 */

$(document).ready(function() {
	var terr_padre = $('input[name=territorio_padre]').val();
	var terr_yo = $('input[name=territorio_id]').val();

	google_map.extender_borde("7.623887", "-68.730469");
	google_map.extender_borde("11.22151", "-63.896484");
	
	$.getJSON('/territorio/terr' + terr_padre + 'niv1/coordenadas.json', function (data) {
		var lineas = new Mapa({
			json: data,
			tipo: 'polilineas',
			proveedor: google_map
		});
	});
	$.getJSON('/territorio/terr' + terr_yo + 'niv1/coordenadas.json', function (data) {
		var poligonos = new Mapa({
			json: data,
			tipo: 'poligonos',
			proveedor: google_map
		});
	});
});