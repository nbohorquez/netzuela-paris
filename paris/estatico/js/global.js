/**
 * @author Nestor Bohorquez
 */

$(document).ready(function() {
	var pagina = $("input[name=pagina]").val();
	pantalla.alto = screen.height;
	pantalla.ancho = screen.width;
	
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

	// Este codigo evita que se cierre el dropdown al hacer clic sobre el formulario de ingreso
	$('.dropdown-menu').find('form').click(function(e) {
		e.stopPropagation();
	});
	
	// No escribais nada despues de estas lineas porque el javascript no lo va a ejecutar
	// No se por que...
	$(".collapse").collapse();
	$('.carousel').carousel();
});

var pantalla = {
	alto: null,
	ancho: null
};

$('#gadget_colapsable').on('hidden', function () {
	$("#gadget").css({'height':'auto'});
	google.maps.event.trigger(google_map.mapa, 'resize');
	$("#gadget_encabezado a i").removeClass("icon-chevron-up").addClass("icon-chevron-down");
});

$('#gadget_colapsable').on('show', function () {
	// Debido a que la pagina tiene el encabezado "DOCTYPE html", es necesario especificar
	// el tamaño del lienzo del mapa en pixeles y no en porcentajes. Mas informacion aqui:
	// http://stackoverflow.com/questions/3217928/google-map-not-working-with-xhtml-doctype-document-type
	$("#gadget").css({'height': (pantalla.alto * 0.4).toString() + 'px'});
	$("#mapa").height($("#gadget").height() - $("#gadget_encabezado").height());
	google.maps.event.trigger(google_map.mapa, 'resize');
	
	$("#gadget_encabezado a i").removeClass("icon-chevron-down").addClass("icon-chevron-up");
	
	if (google_map.borde != null) {
		google_map.ajustar_borde();
	}
});

function dibujar_venezuela_municipios() {
	google_map.extender_borde("7.623887", "-68.730469");
	google_map.extender_borde("11.22151", "-63.896484");
	
	var Venezuela = '0.02.00.00.00.00';
	$.getJSON('/territorio/terr' + Venezuela + 'niv1/coordenadas.json', function (data) {
		var lineas = new Mapa({
			json: data,
			tipo: 'polilineas',
			proveedor: google_map
		});
	});
	$.getJSON('/territorio/terr' + Venezuela + 'niv2/coordenadas.json', function (data) {
		var poligonos = new Mapa({
			json: data,
			tipo: 'poligonos',
			proveedor: google_map
		});
	});
}