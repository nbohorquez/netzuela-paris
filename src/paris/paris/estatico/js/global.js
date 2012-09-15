/**
 * @author Nestor Bohorquez
 */

$(document).ready(function () {
    var pagina = $("input[name=pagina]").val();
    var pantalla = {
        alto: screen.height,
        ancho: screen.width
    };
    
    $("#navegacion li").each(function () {
        // Chequeo si this.text() contiene la cadena de caracteres objeto.val()
        if (~$(this).text().indexOf(pagina)) {
            $(this).addClass("active");
        }
    });

    var tab;    
    $("ul.treeview").each(function () {
        tab = 0;
        $(this).children("li").each(function () {
            if ($(this).hasClass("nodo_padre")){
                $(this).css({'margin-left': tab.toString() + 'em'});
                tab += 1.5;
            }
            else if ($(this).hasClass("nodo_hijo")) {
                $(this).css({'margin-left': tab.toString() + 'em'});
            }
        });
    });
    
    // Este codigo evita que se cierre el dropdown al hacer clic sobre el formulario de ingreso
    $('.dropdown-menu').find('form').click(function (e) {
        e.stopPropagation();
    });
    
    $("#mapa").google_map();
    
    $('#gadget1_colapsable').on('hidden', function () {
        $("#gadget1").height('auto');
        $("#gadget1_encabezado a i").removeClass("icon-chevron-up").addClass("icon-chevron-down");
        $("#mapa").data('google_map').redibujar(false);
    });
    
    $('#gadget1_colapsable').on('show', function () {
        // Debido a que la pagina tiene el encabezado "DOCTYPE html", es necesario especificar
        // el tamaño del lienzo del mapa en pixeles y no en porcentajes. Mas informacion aqui:
        // http://stackoverflow.com/questions/3217928/google-map-not-working-with-xhtml-doctype-document-type
        $("#gadget1").height((pantalla.alto * 0.4).toString() + 'px');
        $("#mapa").height($("#gadget1").height() - $("#gadget1_encabezado").height());
        $("#gadget1_encabezado a i").removeClass("icon-chevron-down").addClass("icon-chevron-up");
        $("#mapa").data('google_map').redibujar(true);
    });
    
    $('#gadget2_colapsable').on('hidden', function () {
        $("#gadget2").height('auto');
        $("#gadget2_encabezado a i").removeClass("icon-chevron-up").addClass("icon-chevron-down");
    });
    
    $('#gadget2_colapsable').on('show', function () {
        $("#gadget2").height($("#gadget2").width());
        $("#historial").height($("#gadget2").height() - $("#gadget2_encabezado").height());
        $("#gadget2_encabezado a i").removeClass("icon-chevron-down").addClass("icon-chevron-up");
        $('#historial').mostrar_historial();
    });
    
    $('.editable').hover(function () {
        //$(this).css('background-color', '#f5f5f5');
        $(this).find('.boton-editar-contenido').show();
        $(this).find('.boton-editar-breadcum').show();
    }, function () {
        //$(this).css('background-color', 'transparent');
        $(this).find('.boton-editar-contenido').hide();
        $(this).find('.boton-editar-breadcum').hide();
    });
});