/**
 * @author Nestor Bohorquez
 */

(function ($) {
	$.fn.dibujar_marcador_tienda = function (tienda) {
		return this.each(function () {
			var contexto = $(this);
        	$.getJSON('/tienda/' + tienda + '/coordenadas.json', function (data) {
				var latitud = data.puntos[0].latitud.replace(",", ".");
				var longitud = data.puntos[0].longitud.replace(",", ".");
				contexto.data('google_map').agregar_marcador(latitud, longitud);
			});
      	});
   	}
   	
   	$.fn.dibujar_poligono_tienda = function (tienda) {
		return this.each(function () {
			var contexto = $(this);
        	$.getJSON('/tienda/' + tienda + '/coordenadas.json', function (data) {
				for (var i = 0; i < data.puntos.length; i++) {
					var punto = new Array();
					punto['latitud'] = data.puntos[i].latitud.replace(",", ".");
					punto['longitud'] = data.puntos[i].longitud.replace(",", ".");
					contexto.data('google_map').extender_borde(punto['latitud'], punto['longitud']);
					tienda.puntos.push(punto);
				}
				// Sin embargo colocamos el marcador en el primer punto solamente. Se podria emplear
				// alguna funcion matematica para calcular el centro del poligono tambien.
				$(this).data('google_map').agregar_marcador(tienda.puntos[0]['latitud'], tienda.puntos[0]['longitud']);
			});
   		});
   	}
		
	$.fn.dibujar_niveles = function (padre, yo) {
		return this.each(function () {
        	$(this).data('google_map').extender_borde("7.623887", "-68.730469");
			$(this).data('google_map').extender_borde("11.22151", "-63.896484");
			$(this).agregar_capa({
				territorio: padre,
				nivel: 1,
				tipo: 'polilineas'
			});
			$(this).agregar_capa({
				territorio: yo,
				nivel: 1,
				tipo: 'poligonos'
			});
      	});
   	}
   	
   	$.fn.dibujar_municipios = function () {
		return this.each(function () {
        	var Venezuela = '0.02.00.00.00.00';
			$(this).data('google_map').extender_borde("7.623887", "-68.730469");
			$(this).data('google_map').extender_borde("11.22151", "-63.896484");
			$(this).agregar_capa({
				territorio: Venezuela,
				nivel: 1,
				tipo: 'polilineas'
			});
			$(this).agregar_capa({
				territorio: Venezuela,
				nivel: 2,
				tipo: 'poligonos'
			});
      	});
   	}
   	
   	$.fn.dibujar_parroquias = function () {
		return this.each(function () {
        	var Venezuela = '0.02.00.00.00.00';
			$(this).data('google_map').extender_borde("7.623887", "-68.730469");
			$(this).data('google_map').extender_borde("11.22151", "-63.896484");
			$(this).agregar_capa({
				territorio: Venezuela,
				nivel: 1,
				tipo: 'polilineas'
			});
			$(this).agregar_capa({
				territorio: Venezuela,
				nivel: 3,
				tipo: 'poligonos'
			});
      	});
   	}
   	
   	$.fn.agregar_capa = function (opciones) {
   		return this.each(function () {
   			var contexto = $(this);
			$.getJSON('/territorio/terr' + opciones.territorio + 'niv' + opciones.nivel + '/coordenadas.json', function (data) {
				var trazos = new Mapa({
					json: data,
					tipo: opciones.tipo,
					proveedor: contexto.data('google_map')
				});
			});
		});
	}
})(jQuery);

function Mapa (opciones) {
	var territorios_crudos = this.parsear_json(opciones.json);
	switch(opciones.tipo) {
		case 'poligonos':
			this.territorios = this.dibujar_poligonos(territorios_crudos, opciones.proveedor);
			break;
		case 'polilineas':
			this.territorios = this.dibujar_polilineas(territorios_crudos, opciones.proveedor);
			break;
		default:
			break;
	}
}

Mapa.prototype.parsear_json = function (data) {
	var resultado = [];
	
	// Este lazo recorre cada territorio
	for (var i = 0, len_i = data.territorios.length; i < len_i; i++) {
		var terr = {
			id: data.territorios[i].id,
			nombre: data.territorios[i].nombre,
			contornos: new Array()
		};
		
		// Este lazo recorre cada contorno de cada territorio
		for (var j = 0, len_j = data.territorios[i].poligonos.length; j < len_j; j++) {
			var contorno = new Array();
			var coordenadas = data.territorios[i].poligonos[j].split(' ');
			// Este lazo recorre cada coordenada de cada poligono
			for (var k = 0, len_k = coordenadas.length; k < len_k; k++) {
				var pto = coordenadas[k].split(':');
				pto[0] = pto[0].replace(",", ".");
				pto[1] = pto[1].replace(",", ".");
				contorno.push(new google.maps.LatLng(pto[0], pto[1]));
			}
			
			terr.contornos.push(contorno);
		}
		
		resultado.push(terr);
	}
	
	return resultado;
}

Mapa.prototype.dibujar_polilineas = function (territorios, proveedor) {
	var resultado = [];
	
	// Este lazo recorre cada territorio
	for (var i = 0, len_i = territorios.length; i < len_i; i++) {
		var terr = new Territorio({
			id: territorios[i].id,
			nombre: territorios[i].nombre,
			mapa: proveedor
		});
		
		// Este lazo recorre cada contorno de cada territorio
		for (var j = 0, len_j = territorios[i].contornos.length; j < len_j; j++) {
			terr.crear_polilinea(territorios[i].contornos[j]);
		}
		
		resultado.push(terr);
	}
	
	return resultado;
}

Mapa.prototype.dibujar_poligonos = function (territorios, proveedor) {
	// Colores provistos por http://colorbrewer2.org/index.php?type=diverging&scheme=RdBu&n=10
	var colores = ["#67001F", "#B2182B", "#D6604D", "#F4A582", "#FDDBC7", "#D1E5F0", "#92C5DE", "#4393C3", "#2166AC", "#053061"];
	var infobox_posicion = new google.maps.Point(80, 230);
	/*var infobox = $(document.createElement('div'))
		.attr({'id': 'infobox'})
		.css({
			'border': '1px solid black',
			'margin-top': '8px',
			'background': '#FFFFFF',
			'padding': '5px' 
		});*/
	var resultado = [];
		
	for (var i = 0, len_i = territorios.length; i < len_i; i++) {
		var terr = new Territorio({
			id: territorios[i].id,
			nombre: territorios[i].nombre,
			color: colores[Math.floor(Math.random()*5)],
			mapa: proveedor
		});
		
		terr.crear_poligono(territorios[i].contornos);
			
		terr.attachEvent('mouseover', function (remitente, args) {
			remitente.poligono.setOptions({fillColor: "#FF0000"});
			//infobox.html('<span>' + remitente.nombre + '</span>');
			//remitente.mapa.infobox.setContent(infobox.outerHtml());
			remitente.mapa.infobox.setContent('<p style="font-weight: bold;">' + remitente.nombre + '</p>');
			if (!remitente.mapa.infobox_abierto) {
				remitente.mapa.infobox_abierto = true;
				remitente.mapa.infobox.setPosition(remitente.mapa.malla.getProjection().fromContainerPixelToLatLng(infobox_posicion));
				remitente.mapa.infobox.open(remitente.mapa.mapa);
			}
		});
		
		terr.attachEvent('mouseout', function (remitente, args) {
			remitente.poligono.setOptions({fillColor: remitente.color});
			remitente.mapa.infobox.setContent('');				
		});		
		
		terr.attachEvent('click', function (remitente, args) {
			$("#ubicacion_visible").text(remitente.nombre);
			$("#ubicacion").val(remitente.id);
		});
		
		resultado.push(terr);
	}
	
	return resultado;
}