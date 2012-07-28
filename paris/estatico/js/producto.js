/**
 * @author Nestor Bohorquez
 */

$(document).ready(function () {
	$('input[name=tienda_id]').each(function () {
		$.getJSON('/tienda/' + $(this).val() + '/coordenadas.json', function (data) {
			var latitud = data.puntos[0].latitud.replace(",", ".");
			var longitud = data.puntos[0].longitud.replace(",", ".");
			google_map.agregar_marcador(latitud, longitud);
		});
    });
});