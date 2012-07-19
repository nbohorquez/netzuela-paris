/**
 * @author Nestor Bohorquez
 */

function Mapa(opciones) {
	var territorios_crudos = this.parsear_json(opciones.json);
	switch(opciones.tipo) {
		case 'poligonos':
			this.territorios = this.dibujar_poligonos(territorios_crudos, opciones.proveedor);
			break;
		case 'polilineas':
			this.territorios = this.dibujar_limites(territorios_crudos, opciones.proveedor);
			break;
		default:
			break;
	}
}

Mapa.prototype.parsear_json = function(data) {
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

Mapa.prototype.dibujar_limites = function(territorios, proveedor) {
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

Mapa.prototype.dibujar_poligonos = function(territorios, proveedor) {
	// Colores provistos por http://colorbrewer2.org/index.php?type=diverging&scheme=RdBu&n=10
	var colores = ["#67001F", "#B2182B", "#D6604D", "#F4A582", "#FDDBC7", "#D1E5F0", "#92C5DE", "#4393C3", "#2166AC", "#053061"];
	var infobox_posicion = new google.maps.Point(80, 230);
	var infobox = $(document.createElement('div'))
		.attr({'id': 'infobox'})
		.css({
			'border': '1px solid black',
			'margin-top': '8px',
			'background': '#FFFFFF',
			'padding': '5px' 
		});
	var resultado = [];
		
	for (var i = 0, len_i = territorios.length; i < len_i; i++) {
		var terr = new Territorio({
			id: territorios[i].id,
			nombre: territorios[i].nombre,
			color: colores[Math.floor(Math.random()*5)],
			mapa: proveedor
		});
		
		terr.crear_poligono(territorios[i].contornos);
			
		terr.attachEvent('mouseover', function(remitente, args) {
			remitente.poligono.setOptions({fillColor: "#FF0000"});
			//infobox.html('<span>' + remitente.nombre + '</span>');
			//remitente.mapa.infobox.setContent(infobox.outerHtml());
			remitente.mapa.infobox.setContent(remitente.nombre);
			if (!remitente.mapa.infobox_abierto) {
				remitente.mapa.infobox_abierto = true;
				remitente.mapa.infobox.setPosition(remitente.mapa.malla.getProjection().fromContainerPixelToLatLng(infobox_posicion));
				remitente.mapa.infobox.open(remitente.mapa.mapa);
			}
		});
		
		terr.attachEvent('mouseout', function(remitente, args) {
			remitente.poligono.setOptions({fillColor: remitente.color});
			remitente.mapa.infobox.setContent('');				
		});		
		
		terr.attachEvent('click', function(remitente, args) {
			$("#ubicacion_visible").text(remitente.nombre);
			$("#ubicacion").val(remitente.id);
		});
		
		resultado.push(terr);
	}
	
	return resultado;
}