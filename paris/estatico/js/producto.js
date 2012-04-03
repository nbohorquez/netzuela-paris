/**
 * @author Nestor Bohorquez
 */

$(document).ready(function() {
	$('input[name=tienda_id]').each(function() {
		$.getJSON('/tienda_coordenadas.json', { tienda_id: $(this).val() }, function(data) {
			var latitud = parseFloat(data.latitud.replace(",", "."));
			var longitud = parseFloat(data.longitud.replace(",", "."));
			google_map.agregar_marcador(latitud, longitud);
		});
    });    
});