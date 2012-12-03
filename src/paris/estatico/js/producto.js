/**
 * @author Nestor Bohorquez
 */

$(document).ready(function () {
    $('input[name=tienda_id]').each(function () {
        $('#mapa').dibujar_marcador_tienda($(this).val());
    });
});