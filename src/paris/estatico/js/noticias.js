/**
 * @author Nestor Bohorquez
 */

$(document).ready(function() {
    $('.popover-aqui').bind('hover', function () {
        var este = $(this);
        $.getJSON('/objeto/tipo' + $(this).attr("tipo") + 'id' + $(this).attr("id") + '/teaser.json', function (data) {
            html = "<div class='media' style='width: auto'><div class='pull-left'>";
            
            if (data.foto != null) {
                html += "<img src='/img/" + data.foto + "' alt='foto actor' />";
            }
            
            html += "</div><div class='media-body'><table class='table'><tbody><tr><td><p>";
            for (var key in data.diccionario) {
                html += "<span>" + key + "</span><br />";
            }
            
            html += "</p></td><td><p>";
            for (var key in data.diccionario) {
                html += "<span>" + data.diccionario[key] + "</span><br />";
            }
            
            html += "</p></td></tr></tbody></table></div></div>";

            este.unbind('hover').popover({
                title: data.titulo,
                html: true,
                content: html,
                template: '<div class="popover"><div class="arrow"></div><div class="popover-inner" style="width: auto"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>',
                trigger: 'hover'
            }).popover('show').css('width', 'auto');
        });
    });
});