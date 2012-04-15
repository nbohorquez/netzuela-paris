/**
 * @author Nestor Bohorquez
 */

$(document).ready(function() {
	territorio.id = $('input[name=territorio_id]').val();
	$.getJSON('/territorio_coordenadas.json', { territorio_id: territorio.id }, function(data) {
		for (var i = 0; i < data.puntos.length; i++) {
			var punto = new Array();
			punto['latitud'] = data.puntos[i].latitud.replace(",", ".");
			punto['longitud'] = data.puntos[i].longitud.replace(",", ".");
			google_map.extender_borde(punto['latitud'], punto['longitud']);
			territorio.puntos.push(punto);
		}
	});
});

var territorio = {
	id: null,
	puntos: new Array()
}