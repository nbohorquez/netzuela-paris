/**
 * @author Nestor Bohorquez
 */

$(document).ready(function() {
	territorio.id = $('input[name=territorio_id]').val();
	$.getJSON('/territorio/' + territorio.id + '/coordenadas.json', function(data) {
		for (var i = 0; i < data.poligonos.length; i++) {			
			var poligono = new Array();
			for (var j = 0; j < data.poligonos[i].length; j++) {
				var punto = new Array();
				punto['latitud'] = data.poligonos[i][j].latitud.replace(",", ".");
				punto['longitud'] = data.poligonos[i][j].longitud.replace(",", ".");
				google_map.extender_borde(punto['latitud'], punto['longitud']);
				var punto_gmap = new google.maps.LatLng(punto['latitud'], punto['longitud']);
				poligono.push(punto_gmap);
			}
			territorio.poligonos.push(poligono);
		}
		
		var poligono_visible = new google.maps.Polygon({
		    paths: territorio.poligonos,
    		strokeColor: "#FF0000",
    		strokeOpacity: 0.8,
    		strokeWeight: 2,
    		fillColor: "#FF0000",
    		fillOpacity: 0.35
		});
		
		poligono_visible.setMap(google_map.mapa);
		/*
		var valores = "";
		paths = poligono_visible.getPaths();
		for (var i = 0; i < paths.getLength(); i++)
		{
			valores += 'Poligono[' + i.toString() + ']:';
			for(var j = 0; j < paths.getAt(i).getLength(); j++)
			{
				valores += paths.getAt(i).getAt(j).lat() + ',' + paths.getAt(i).getAt(j).lng() + ' ';
			}
			valores += "\n";
		}
		alert(valores);
		*/
	});
});

var territorio = {
	id: null,
	poligonos: new Array(),
	contornos: new Array()
};