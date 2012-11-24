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

    switch (pagina)
        {
            case 'Tienda':
            case 'Producto':
            case 'Patrocinante':
            case 'Usuario':
                $("#mapa").google_map({
                    estilos: [{
                        featureType: "road",
                        stylers: [
                            { visibility: "on" }
                        ]
                    },{
                        featureType: "poi",
                        stylers: [
                            { visibility: "off" }
                        ]
                    },{
                        featureType: "transit",
                        stylers: [
                            { visibility: "off" }
                        ]
                    },{
                        featureType: "administrative.province",
                        stylers: [
                            { visibility: "off" }
                        ]
                    }] 
                });
                break;
            case 'Tiendas':
            case 'Productos':
            case 'Registro':
            case 'Registro de tienda':
                $("#mapa").google_map();
                break;
            default:
                $("#mapa").google_map();
        }
    
    $('.accordion-body').on('hidden', function () {
        $(this).siblings('.accordion-heading').find('a i').removeClass("icon-chevron-up").addClass("icon-chevron-down");
    });
    
    $('.accordion-body').on('show', function () {
        $(this).siblings('.accordion-heading').find('a i').removeClass("icon-chevron-down").addClass("icon-chevron-up");
    });

    $('#gadget_colapsable').on('hidden', function () {
        $("#gadget").height('auto');
        $("#mapa").data('google_map').redibujar(false);
    });
    
    $('#gadget_colapsable').on('show', function () {
        // Debido a que la pagina tiene el encabezado "DOCTYPE html", es necesario especificar
        // el tamaño del lienzo del mapa en pixeles y no en porcentajes. Mas informacion aqui:
        // http://stackoverflow.com/questions/3217928/google-map-not-working-with-xhtml-doctype-document-type
        //$("#gadget1").height((pantalla.alto * 0.4).toString() + 'px');
        switch (pagina)
        {
            case 'Tienda':
            case 'Producto':
            case 'Patrocinante':
            case 'Usuario':
                $("#gadget").height($("#pitch_well").height() + $("#gadget_encabezado").height()/2);
                break;
            case 'Tiendas':
            case 'Productos':
            case 'Registro':
            case 'Registro de tienda':
                $("#gadget").height('350px');
                break;
            default:
                $("#gadget").height('350px');
        }
        
        $("#mapa").height($("#gadget").height() - $("#gadget_encabezado").height());
        $("#mapa").data('google_map').redibujar(true);
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