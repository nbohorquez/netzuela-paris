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
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(mostrar_posicion, error_posicion);
	} else {
		alert('Tu navegador no soporta Geolocation API, ¡usa vergas buenas!');
	}
	
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
