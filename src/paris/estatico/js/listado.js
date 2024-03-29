/**
 * @author Nestor Bohorquez
 */

$(document).ready(function () {
    var terr_padre = $('input[name=territorio_padre]').val();
    var terr_yo = $('input[name=territorio_id]').val();
    $('#mapa').dibujar_niveles([
        {territorio: terr_yo, nivel: 0, tipo: 'polilineas', centrar: true},
        {territorio: terr_yo, nivel: 1, tipo: 'poligonos', centrar: false}
    ]);
    $('#mapa').bind('poligono_click', function (e, data) {
        var remitente = data.remitente;
        var listado = $('input[name=listado]').val().toLowerCase();
        var categoria = $('input[name=categoria_id]').val();
        window.location.href = '/' + listado + '/cat' + categoria 
                               + 'geo' + remitente.id;
    });
});