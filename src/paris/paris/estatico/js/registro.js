/**
 * @author Nestor Bohorquez
 */


function mostrar_posicion (posicion) {
	google_map.agregar_marcador(posicion.coords.latitude, posicion.coords.longitude);
}

function error_posicion () {
	alert('Error al obtener tu posicion');
}

$(document).ready(function () {
	/*
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(mostrar_posicion, error_posicion);
	} else {
		alert('Tu navegador no soporta Geolocation API');
	}
	*/
	$('#mapa').dibujar_municipios();
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
				equalTo: "Contraseñas no coinciden"
			},
			nombre: "Escriba su nombre",
			apellido: "Escriba su apellido",
			condiciones: "Acepte las condiciones del servicio"
	    },
	    highlight: function (label) {
	    	$(label).closest('.control-group').removeClass('error success').addClass('error');
	    },
	    success: function (label) {
	    	$(label).closest('.control-group').removeClass('error success').addClass('success');
	    }
	});
});