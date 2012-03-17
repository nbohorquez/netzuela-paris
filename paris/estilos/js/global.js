function inicializar() {
    var latlng = new google.maps.LatLng(10.40, -71.44);
    var opciones = {
      zoom: 8,
      center: latlng,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var mapa = new google.maps.Map(document.getElementById("mapa"), opciones);
}

$('#gadget_colapsable').on('hidden', function () {
	$("#gadget").css({'height':'auto'});
})

$('#gadget_colapsable').on('show', function () {
	$("#gadget").css({'height':'40%'});
	$("#mapa").height($("#gadget").height() - $("#gadget_encabezado").height());
})