/**
 * @author Nestor Bohorquez
 */

$(document).ready(function () {
    var terr_padre = $('input[name=territorio_padre]').val();
    var terr_yo = $('input[name=territorio_id]').val();
    $('#mapa').dibujar_niveles(terr_padre, terr_yo);
});