/**
 * @author Nestor Bohorquez
 */

$(document).ready(function() {
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
	
	/*
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(mostrar_posicion, error_posicion);
	} else {
		alert('Tu navegador no soporta Geolocation API');
	}
	*/
	
	$.validator.addMethod(
        "regex",
        function(value, element, param) {
            var re = new RegExp(param);
            return this.optional(element) || re.test(value);
        },
        "Formato inválido"
	);
	
	$('#formulario_registro_consumidor').validate({
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
	      	ubicacion: {
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
	
	$('#formulario_registro_tienda').validate({
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
	      	rif: {
	      		required: true,
	      		regex: "^[JVG]-[0-9]{8}-[0-9]$"
	      	},
	      	nombre_legal: {
	      		required: true
	      	},
	      	nombre_comun: {
	      		required: true
	      	},
	      	categoria: {
	      		required: true
	      	},
	      	telefono: {
	      		required: true,
	      		regex: "^[1-9][0-9]{2}-[1-9][0-9]{6}$"
	      	},
	      	calle: {
	      		required: true
	      	},
	      	urbanizacion: {
	      		required: true
	      	},
	      	ubicacion: {
	      		required: false
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
			rif: {
				required: "Ingrese el RIF de su tienda",
				regex: "Formato de RIF inválido"
			},
	      	nombre_legal: "Escriba el nombre legal de su tienda",
	      	nombre_comun: "Escriba el nombre común de su tienda",
	      	categoria: "Seleccione la categoría o rubro en el cual se desempeña su tienda",
	      	telefono: {
	      		required: "Ingrese su número de teléfono",
	      		regex: "Formato de teléfono inválido"
	      	},
	      	calle: "Ingrese el nombre de la calle/avenida donde se ubica la tienda",
	      	urbanizacion: "Ingrese el nombre de la urbanización donde se ubica la tienda",
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