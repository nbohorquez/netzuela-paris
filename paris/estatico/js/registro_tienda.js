/**
 * @author Nestor Bohorquez
 */

$(document).ready(function () {
	dibujar_venezuela_municipios();

	$.validator.addMethod(
        "regex",
        function (value, element, param) {
            var re = new RegExp(param);
            return this.optional(element) || re.test(value);
        },
        "Formato inválido"
	);

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
	    highlight: function (label) {
	    	$(label).closest('.control-group').removeClass('error success').addClass('error');
	    },
	    success: function (label) {
	    	$(label).closest('.control-group').removeClass('error success').addClass('success');
	    }
	});
});