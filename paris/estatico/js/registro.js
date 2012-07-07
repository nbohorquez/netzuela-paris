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

$(document).ready(function() {
	var venezuela = '0.02.00.00.00.00';
	// Colores provistos por http://colorbrewer2.org/index.php?type=diverging&scheme=RdBu&n=10
	var colores = ["#67001F", "#B2182B", "#D6604D", "#F4A582", "#FDDBC7", "#D1E5F0", "#92C5DE", "#4393C3", "#2166AC", "#053061"];
	$.getJSON('/territorio/terr' + venezuela + 'niv2/coordenadas.json', function(data) {
		//var terrs = new Array();
		
		// Este lazo recorre cada territorio
		for (var i = 0; i < data.territorios.length; i++) {
			var territorio = {
				contornos: new Array(),
				poligono: null
			};
			
			// Este lazo recorre cada poligono (contorno) de cada territorio
			for (var j = 0; j < data.territorios[i].length; j++) {			
				var contorno = new Array();
				var coordenadas = data.territorios[i][j].split(' ');
				// Este lazo recorre cada coordenada de cada poligono
				for (var k = 0; k < coordenadas.length; k++) {
					var pto = coordenadas[k].split(':');
					pto[0] = pto[0].replace(",", ".");
					pto[1] = pto[1].replace(",", ".");			
					google_map.extender_borde(pto[0], pto[1]);
					var punto_gmap = new google.maps.LatLng(pto[0], pto[1]);
					contorno.push(punto_gmap);
				}
				territorio.contornos.push(contorno);
			}
			
			var color = colores[Math.floor(Math.random()*5)];
			territorio.poligono = new google.maps.Polygon({
			    paths: territorio.contornos,
	    		strokeColor: "#000000",
	    		strokeOpacity: 0.8,
	    		strokeWeight: 0.5,
	    		fillColor: color,
	    		fillOpacity: 0.35
			});
			
			territorio.poligono.setMap(google_map.mapa);
			//terrs.push(territorio);
		}
	});	
			
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

function mostrar_posicion(posicion) {
	google_map.agregar_marcador(posicion.coords.latitude, posicion.coords.longitude);
}

function error_posicion() {
	alert('Error al obtener tu posicion');
}