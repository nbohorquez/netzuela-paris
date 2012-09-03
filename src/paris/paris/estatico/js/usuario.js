/**
 * @author Nestor Bohorquez
 */

$(document).ready(function () {
	$('#mapa').data('google_map').extender_borde("7.623887", "-68.730469");
    $('#mapa').data('google_map').extender_borde("11.22151", "-63.896484");
    var ubicacion = $('input[name=usuario_ubicacion]').val();
    if (ubicacion) {
    	$('#mapa').agregar_capa({
	    	territorio: ubicacion,
	        nivel: 0,
	        tipo: 'poligonos'
		});
    }
});