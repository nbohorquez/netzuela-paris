/**
 * @author Nestor Bohorquez
 */

/*
 * Estos plugins-clases en jQuery las tome de estas fuentes:
 * http://www.virgentech.com/blog/2009/10/building-object-oriented-jquery-plugin.html
 * http://stefangabos.ro/jquery/jquery-plugin-boilerplate-oop/
 */

(function ($) {
    $.mapa = function (elemento, opciones) {
        elemento.data('mapa', this);
        this.opciones = {};
        this.marcadores = this.poligonos = this.polilineas = [];
        this.gmap = elemento.data('google_map');
        
        // Constructor publico
        this.inicializar = function (elemento, opciones) {
            this.opciones = $.extend({}, $.mapa.defaults, opciones);
            
            switch(this.opciones.tipo) {
                case 'poligonos':
                    var territorios_crudos = parsear_json(this, this.opciones.json, this.opciones.centrar);
                    dibujar_poligonos(this, territorios_crudos, this.opciones.centrar);
                    break;
                case 'polilineas':
                    var territorios_crudos = parsear_json(this, this.opciones.json, this.opciones.centrar);
                    dibujar_polilineas(this, territorios_crudos, this.opciones.centrar);
                    break;
                case 'marcador':
                    dibujar_marcador(this, this.opciones);
                    break;
                default:
                    break;
            }
        };
        
        /*
         * Metodo privado. Fijate que 'objeto' es 'esta' instancia de esta
         * clase. Dentro de parsear_json, 'this' pierde el significado usual
         */
        var parsear_json = function (objeto, data, centrar) {
            var resultado = [];
            
            // Este lazo recorre cada territorio
            for (var i = 0, len_i = data.territorios.length; i < len_i; i++) {
                var terr = {
                    id: data.territorios[i].id,
                    nombre: data.territorios[i].nombre,
                    contornos: new Array()
                };
                
                // Este lazo recorre cada contorno de cada territorio
                for (var j = 0, len_j = data.territorios[i].poligonos.length; j < len_j; j++) {
                    var contorno = new Array();
                    var coordenadas = data.territorios[i].poligonos[j].split(' ');
                    // Este lazo recorre cada coordenada de cada poligono
                    for (var k = 0, len_k = coordenadas.length; k < len_k; k++) {
                        var pto = coordenadas[k].split(':');
                        pto[0] = pto[0].replace(",", ".");
                        pto[1] = pto[1].replace(",", ".");

                        if (centrar) {
                            objeto.gmap.extender_borde(pto[0], pto[1]);
                        }
                        
                        contorno.push(new google.maps.LatLng(pto[0], pto[1]));
                    }
                    
                    terr.contornos.push(contorno);
                }
                
                resultado.push(terr);
            }
            
            return resultado;
        }
        
        // Metodo privado
        var dibujar_polilineas = function (objeto, territorios) {
            // Este lazo recorre cada territorio
            for (var i = 0, len_i = territorios.length; i < len_i; i++) {
                var terr = new Territorio({
                    id: territorios[i].id,
                    nombre: territorios[i].nombre,
                    mapa: objeto.gmap
                });
                
                // Este lazo recorre cada contorno de cada territorio
                for (var j = 0, len_j = territorios[i].contornos.length; j < len_j; j++) {
                    terr.crear_polilinea(territorios[i].contornos[j]);
                }
                
                objeto.polilineas.push(terr);
            }
        }

        // Metodo privado
        var dibujar_poligonos = function (objeto, territorios) {
            // Colores provistos por http://colorbrewer2.org/index.php?type=diverging&scheme=RdBu&n=10
            var colores = ["#67001F", "#B2182B", "#D6604D", "#F4A582", "#FDDBC7", "#D1E5F0", "#92C5DE", "#4393C3", "#2166AC", "#053061"];
            var infobox_posicion = new google.maps.Point(80, 230);
            /*var infobox = $(document.createElement('div'))
                .attr({'id': 'infobox'})
                .css({
                    'border': '1px solid black',
                    'margin-top': '8px',
                    'background': '#FFFFFF',
                    'padding': '5px' 
                });*/

            for (var i = 0, len_i = territorios.length; i < len_i; i++) {
                var terr = new Territorio({
                    id: territorios[i].id,
                    nombre: territorios[i].nombre,
                    color: colores[Math.floor(Math.random()*5)],
                    mapa: objeto.gmap
                });

                terr.crear_poligono(territorios[i].contornos);

                terr.attachEvent('mouseover', function (remitente, args) {
                    remitente.poligono.setOptions({fillColor: "#FF0000"});
                    //infobox.html('<span>' + remitente.nombre + '</span>');
                    //remitente.mapa.infobox.setContent(infobox.outerHtml());
                    remitente.mapa.infobox.setContent('<p style="font-weight: bold;">' + remitente.nombre + '</p>');
                    if (!remitente.mapa.infobox_abierto) {
                        remitente.mapa.infobox_abierto = true;
                        remitente.mapa.infobox.setPosition(remitente.mapa.malla.getProjection().fromContainerPixelToLatLng(infobox_posicion));
                        remitente.mapa.infobox.open(remitente.mapa.mapa);
                    }
                    // Eventos en jQuery:
                    // http://fuelyourcoding.com/jquery-custom-events-they-will-rock-your-world/
                    elemento.trigger('poligono_mouseover', {
                        remitente: remitente,
                        args: args
                    });
                });
                
                terr.attachEvent('mouseout', function (remitente, args) {
                    remitente.poligono.setOptions({fillColor: remitente.color});
                    remitente.mapa.infobox.setContent('');
                    
                    elemento.trigger('poligono_mouseout', {
                        remitente: remitente,
                        args: args
                    });
                });
                
                terr.attachEvent('click', function (remitente, args) {
                    elemento.trigger('poligono_click', {
                        remitente: remitente,
                        args: args
                    });
                });
                
                objeto.poligonos.push(terr);
            }
        }
        
        // Metodo privado
        var dibujar_marcador = function (objeto, opciones) {
            var marcador = objeto.gmap.agregar_marcador(opciones.latitud, opciones.longitud, opciones.opciones);
            opciones.propietario.marcador = marcador;
            objeto.marcadores.push(marcador);
        }
        
        this.inicializar(elemento, opciones);
    };
    
    $.fn.dibujar_marcador = function (opciones) {
        return this.each(function () {
            $(this).mapa({
                tipo: 'marcador',
                latitud: opciones.latitud,
                longitud: opciones.longitud,
                propietario: opciones.propietario,
                opciones: opciones.opciones
             });
        });
    }
    
    $.fn.centrar_en_venezuela = function () {
        $(this).data('google_map').extender_borde("7.623887", "-68.730469");
        $(this).data('google_map').extender_borde("11.22151", "-63.896484");
    }
    
    $.fn.dibujar_estados = function () {
        return this.each(function () {
            var Venezuela = '0.02.00.00.00.00';
            $(this).centrar_en_venezuela();
            $(this).dibujar_niveles([
                {territorio: Venezuela, nivel: 0, tipo: 'polilineas', centrar: false},
                {territorio: Venezuela, nivel: 1, tipo: 'poligonos', centrar: false}
            ])
        });
    }
    
    $.fn.dibujar_municipios = function () {
        return this.each(function () {
            var Venezuela = '0.02.00.00.00.00';
            $(this).centrar_en_venezuela();
            $(this).dibujar_niveles([
                {territorio: Venezuela, nivel: 1, tipo: 'polilineas', centrar: false},
                {territorio: Venezuela, nivel: 2, tipo: 'poligonos', centrar: false}
            ])
        });
    }
    
    $.fn.dibujar_parroquias = function () {
        return this.each(function () {
            var Venezuela = '0.02.00.00.00.00';
            $(this).centrar_en_venezuela();
            $(this).dibujar_niveles([
                {territorio: Venezuela, nivel: 1, tipo: 'polilineas', centrar: false},
                {territorio: Venezuela, nivel: 3, tipo: 'poligonos', centrar: false}
            ])
        });
    }
    
    $.fn.dibujar_niveles = function (niveles) {
        return this.each(function () {
            for (var i = 0, len_i = niveles.length; i < len_i; i++) {
                $(this).agregar_capa({
                    territorio: niveles[i].territorio,
                    nivel: niveles[i].nivel,
                    tipo: niveles[i].tipo,
                    centrar: niveles[i].centrar
                });
            }
        });
    }
    
    $.fn.agregar_capa = function (opciones) {
        return this.each(function () {
            var contexto = $(this);
            $.getJSON('/territorio/terr' + opciones.territorio + 'niv' + opciones.nivel + '/coordenadas.json', function (data) {
                contexto.mapa({
                    json: data,
                    tipo: opciones.tipo,
                    centrar: opciones.centrar
                });
            });
        });
    }
    
    $.fn.mapa = function (opciones) {
        return this.each(function () {
            // Este plugin funciona solamente si el elemento en cuestion ya 
            // tiene un $.google_map y no tiene un $.mapa
            if (!($(this).data('google_map'))) {
                return;
            }
            
            if ($(this).data('mapa')) {
                   $(this).data('mapa').inicializar($(this), opciones);
            } else {
                (new $.mapa($(this), opciones));
               }
        });
    };
    
    $.mapa.defaults = {
        json: null,
        tipo: 'poligonos',
        centrar: true
    }
})(jQuery);