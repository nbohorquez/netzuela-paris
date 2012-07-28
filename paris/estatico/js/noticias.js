/**
 * @author Nestor Bohorquez
 */

$(document).ready(function() {
	$('.popover-actor-activo').popover({ 
	    html: true,
	    content: function() {
	    	return $(this).parents('.titular-noticia').siblings('.popover-inner-actor-activo').html();
	    },
	    // Aqui agrego 'width: auto' a la clase .popover-inner
	    template: '<div class="popover"><div class="arrow"></div><div class="popover-inner" style="width: auto"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'
	});
	
	$('.popover-actor-pasivo').popover({ 
	    html: true,
	    content: function() {
	    	return $(this).parents('.titular-noticia').siblings('.popover-inner-actor-pasivo').html();
	    },
	    // Aqui agrego 'width: auto' a la clase .popover-inner
	    template: '<div class="popover"><div class="arrow"></div><div class="popover-inner" style="width: auto"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'
	});
});