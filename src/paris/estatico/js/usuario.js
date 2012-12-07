/**
 * @author Nestor Bohorquez
 */

$(document).ready(function () {
    var ubicacion = $('input[name=usuario_ubicacion]').val();
    if (ubicacion) {
        $('#mapa').agregar_capa({
            territorio: ubicacion,
            nivel: 0,
            tipo: 'polilineas'
        });
    }
});