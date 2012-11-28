/**
 * @author Nestor Bohorquez
 */

(function ($) {
    $.google_map = function (elemento, opciones) {
        this.opciones = {};
        this.infobox_abierto = false;
        this.mapa = this.cursor = this.borde = this.malla = this.infobox = null;
        elemento.data('google_map', this);

        // Contructor publico
        this.inicializar = function (elemento, opciones) {
            this.opciones = $.extend({}, $.google_map.defaults, opciones);
            
            var infobox_posicion = new google.maps.Point(80, 230);
            var contexto = this;
            var opciones2 = {
                zoom: this.opciones.zoom,
                center: this.opciones.centro,
                mapTypeId: this.opciones.tipo,
                styles: this.opciones.estilos
            };
            
            this.mapa = new google.maps.Map(elemento[0], opciones2);
            this.borde = new google.maps.LatLngBounds();
            
            this.malla = new google.maps.OverlayView();
            this.malla.draw = function () {};
            this.malla.setMap(this.mapa);
            
            this.infobox = new InfoBox({
                content: '',
                disableAutoPan: false,
                zIndex: null,
                closeBoxURL: "",
                boxStyle: { width: "280px" },
                closeBoxMargin: "10px 2px 2px 2px",
                infoBoxClearance: new google.maps.Size(1, 1),
                isHidden: false,
                pane: "floatPane",
                enableEventPropagation: false,
            });
            
            google.maps.event.addListener(this.mapa, 'bounds_changed', function (event) {
                contexto.infobox.setPosition(contexto.malla.getProjection().fromContainerPixelToLatLng(infobox_posicion));
            });
            
            google.maps.event.addListener(this.mapa, 'mousemove', function (event) {
                contexto.cursor = event.latLng;
            });
        };
        
        // Metodo publico
        this.agregar_marcador = function (latitud, longitud) {
            var punto = new google.maps.LatLng(latitud, longitud);
            var marcador = new google.maps.Marker({
                position: punto,
                map: this.mapa
            });
            this.extender_borde(latitud, longitud);
        }
        
        // Metodo publico
        this.extender_borde = function (latitud, longitud) {
            var punto = new google.maps.LatLng(latitud, longitud);
            this.borde.extend(punto);
        }
        
        // Metodo publico
        this.ajustar_a_borde = function () {
            if (this.borde != null) {
                this.mapa.fitBounds(this.borde);
            }
        }
        
        // Metodo publico
        this.redibujar = function (ajustar) {
            google.maps.event.trigger(this.mapa, 'resize');
            if (ajustar) {
                this.ajustar_a_borde();
                // Un zoom mayor a 16 es demasiado
                if (this.mapa.getZoom() > 16) {
                    this.mapa.setZoom(16);
                }
            }
        }
        
        this.inicializar(elemento, opciones);
    };
    
    // Punto de entrada del plugin
    $.fn.google_map = function (opciones) {
        return this.each(function () {
            (new $.google_map($(this), opciones));
        });
    };
    
    $.google_map.defaults = {
        tipo: google.maps.MapTypeId.ROADMAP,
        centro: new google.maps.LatLng(10.40, -71.44),
        zoom: 11,
        estilos: [{
            featureType: "road",
            stylers: [
                { visibility: "off" }
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
    }
})(jQuery);