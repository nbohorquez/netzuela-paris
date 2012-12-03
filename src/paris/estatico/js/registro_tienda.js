/**
 * @author Nestor Bohorquez
 */

$(document).ready(function () {
    $('#mapa').dibujar_municipios();
    $('#mapa').bind('poligono_click', function (e, data) {
        var remitente = data.remitente;
        $("#ubicacion_visible").text(remitente.nombre);
        $("#ubicacion").val(remitente.id);
    });
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