/**
 * @author Nestor Bohorquez
 */

/* Cambio el formato de la fecha a dd/mm/aaaa */
$.extend($.fn.datepicker.defaults, {
	parse: function (string) {
  		var matches;
  		if ((matches = string.match(/^(\d{2,2})\/(\d{2,2})\/(\d{4,4})$/))) {
        	return new Date(matches[3], matches[2] - 1, matches[1]);
  		} else {
            return null;
      	}
	},
	format: function (date) {
    	var month = (date.getMonth() + 1).toString(), dom = date.getDate().toString();
  		if (month.length === 1) {
          	month = "0" + month;
    	}
  		if (dom.length === 1) {
          	dom = "0" + dom;
  		}
  		return dom + "/" + month + "/" + date.getFullYear();
	}
});

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