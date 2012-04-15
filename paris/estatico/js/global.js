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

	var tab;	
	$("ul.treeview").each(function() {
		tab = 0;
		$(this).children("li").each(function() {
			if ($(this).hasClass("nodo_padre")){
				$(this).css({'margin-left': tab.toString() + 'em'});
				tab += 1.5;
			}
			else if ($(this).hasClass("nodo_hijo")) {
				$(this).css({'margin-left': tab.toString() + 'em'});
			}
		});
	});

	$(".collapse").collapse();
	$('.carousel').carousel()
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
		google_map.ajustar_borde();
	}
});