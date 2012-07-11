/**
 * @author Nestor Bohorquez
 */

function Territorio(opciones) {
	this.id = ('id' in opciones) ? opciones.id : null;
	this.nombre = ('nombre' in opciones) ? opciones.nombre : null;
	this.color = ('color' in opciones) ? opciones.color : null;
	this.mapa = ('mapa' in opciones) ? opciones.mapa : null;
	this.polilineas = new Array();	
	this.poligono = null;
}

Territorio.prototype = new EventObject();

Territorio.prototype.crear_polilinea = function(contorno) {
	var polilinea = new google.maps.Polyline({
		path: contorno,
		strokeColor: "#000000",
		strokeOpacity: 1.5,
		strokeWeight: 2
	});
	
	polilinea.setMap(this.mapa.mapa);
	this.polilineas.push(polilinea);
}

Territorio.prototype.crear_poligono = function (contornos) {
	this.poligono = new google.maps.Polygon({
	    paths: contornos,
		strokeColor: "#FFFFFF",
		strokeOpacity: 0.8,
		strokeWeight: 0.5,
		fillColor: this.color,
		fillOpacity: 0.35
	});
	
	var contexto = this;
	this.poligono.setMap(this.mapa.mapa);
	
	google.maps.event.addListener(this.poligono, 'mouseover', function(args) {
		//var start = new Date().getTime();
		contexto.raiseEvent('mouseover', args);
		/*var end = new Date().getTime();
		var time = end - start;
		alert('Execution time: ' + time);*/
	});
	
	google.maps.event.addListener(this.poligono, 'mouseout', function(args) {
		contexto.raiseEvent('mouseout', args);
	});
	
	google.maps.event.addListener(this.poligono, 'click', function(args) {
		contexto.raiseEvent('click', args);
	});
}