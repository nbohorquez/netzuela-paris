/**
 * @author Nestor Bohorquez
 */

$(document).ready(function() {
	var pagina = $("input[name=pagina]").val();
	
	$("#navegacion li").each(function() {
		// Chequeo si this.text() contiene la cadena de caracteres objeto.val()
		if (~$(this).text().indexOf(pagina)) {
			$(this).addClass("active");
		}
	});
	
	$(".collapse").collapse();
	$('.carousel').carousel()
	
	//$.getJSON('/categorias.json', { categoria_id: 1 }, escribir_categorias);
});

$('#categorias li a').live('click', function() {
	//$.getJSON('/categorias.json', { categoria_id: $(this).siblings('input[name=categoria_id]').val() }, escribir_categorias);
});

$('#gadget_colapsable').on('hidden', function () {
	$("#gadget").css({'height':'auto'});
	google.maps.event.trigger(google_map.mapa, 'resize');
	$("#gadget_encabezado a i").removeClass("icon-chevron-up").addClass("icon-chevron-down");
});

$('#gadget_colapsable').on('show', function () {
	$("#gadget").css({'height':'40%'});
	$("#mapa").height($("#gadget").height() - $("#gadget_encabezado").height());
	google.maps.event.trigger(google_map.mapa, 'resize');
	
	$("#gadget_encabezado a i").removeClass("icon-chevron-down").addClass("icon-chevron-up");
	
	if (google_map.borde != null) {
		google_map.ajustar_mapa();
	}
});

function escribir_categorias(data) {
	var html = '<li class="nav-header">Categorias</li>';
	$.each(data.categorias, function(indice, valor) {
		html += (indice == 0) ? '<li class="active">' : '<li>';
		html += '<a href="#">' + valor['nombre'] + '</a><input type="hidden" name="categoria_id" value="' + valor['categoria_id'] + '" /></li>';			
	});
	$('#categorias').html(html);
}