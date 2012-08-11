/**
 * @author Nestor Bohorquez
 */

$(document).ready(function () {
	$('#mapa').dibujar_municipios();
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
	    highlight: function (label) {
	    	$(label).closest('.control-group').removeClass('error success').addClass('error');
	    },
	    success: function (label) {
	    	$(label).closest('.control-group').removeClass('error success').addClass('success');
	    }
	});
});