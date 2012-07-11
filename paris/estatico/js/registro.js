/**
 * @author Nestor Bohorquez
 */

$(document).ready(function() {
	google_map.extender_borde("7.623887", "-68.730469");
	google_map.extender_borde("11.22151", "-63.896484");
	
	var Venezuela = '0.02.00.00.00.00';
	$.getJSON('/territorio/terr' + Venezuela + 'niv1/coordenadas.json', dibujar_limites);
	$.getJSON('/territorio/terr' + Venezuela + 'niv2/coordenadas.json', dibujar_regiones);
	
	/*
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(mostrar_posicion, error_posicion);
	} else {
		alert('Tu navegador no soporta Geolocation API');
	}
	*/
	
	$('#formulario_registro').validate({
		rules: {
			correo_electronico: {
	        	required: true,
	        	email: true
	      	},
	      	contrasena: {
		        required: true,
	        	minlength: 8
	      	},
	      	repetir_contrasena: {
		        required: true,
		        equalTo: "#contrasena"
	      	},
	      	nombre: {
	        	required: true
	      	},
	      	apellido: {
	        	required: true
	      	},
	      	grado_de_instruccion: {
	      		required: true
	      	},
	      	region: {
	      		required: false
	      	},
	      	fecha_de_nacimiento: {
	      		required: true
	      	},
	      	condiciones: {
	      		required: true
	      	}
	    },
	    messages: {
	    	correo_electronico: {
	    		required: "Se requiere una dirección de correo electrónico",
	    		email: "Correo electrónico inválido"
	    	},
			contrasena: {
				required: "Se requiere una contraseña",
				minlength: "Ingrese una contraseña de más de 8 dígitos"
			},
			repetir_contrasena: {
				required: "Repita la contraseña aquí",
				minlength: "Ingrese una contraseña de más de 8 dígitos",
				equalTo: "Contraseñas no concuerdan"
			},
			nombre: "Escriba su nombre",
			apellido: "Escriba su apellido",
			fecha_de_nacimiento: "Ingrese su fecha de nacimiento",
			condiciones: "Acepte las condiciones del servicio"
	    },
	    highlight: function(label) {
	    	$(label).closest('.control-group').removeClass('error success').addClass('error');
	    },
	    success: function(label) {
	    	$(label).closest('.control-group').removeClass('error success').addClass('success');
	    }
	});
});

function dibujar_limites(data) {
	// Este lazo recorre cada territorio
	for (var i = 0, len_i = data.territorios.length; i < len_i; i++) {
		var terr = new Territorio({
			id: data.territorios[i].id,
			nombre: data.territorios[i].nombre,
			mapa: google_map
		});
		
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
			
			terr.crear_polilinea(contorno);
		}
	}
}

function dibujar_regiones(data) {
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
	
	// Este lazo recorre cada territorio
	for (var i = 0, len_i = data.territorios.length; i < len_i; i++) {
		var terr = new Territorio({
			id: data.territorios[i].id,
			nombre: data.territorios[i].nombre,
			color: colores[Math.floor(Math.random()*5)],
			mapa: google_map
		});
		
		var contornos = new Array();
		
		// Este lazo recorre cada poligono (contorno) de cada territorio
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
			contornos.push(contorno);
		}
		
		terr.crear_poligono(contornos);
			
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
	}
}

/*
function mostrar_posicion(posicion) {
	google_map.agregar_marcador(posicion.coords.latitude, posicion.coords.longitude);
}

function error_posicion() {
	alert('Error al obtener tu posicion');
}
*/

/* Cambio el formato de la fecha a dd/mm/aaaa */
$.extend($.fn.datepicker.defaults, {
	parse: function(string) {
  		var matches;
  		if ((matches = string.match(/^(\d{2,2})\/(\d{2,2})\/(\d{4,4})$/))) {
        	return new Date(matches[3], matches[2] - 1, matches[1]);
  		} else {
            return null;
      	}
	},
	format: function(date) {
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