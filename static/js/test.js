$(document).ready(function(){
	$('.toggle').toggle(function(){
		$(this).parent().next().slideUp('fast');
		$(this).children('img:first').attr("src", "/images/interface/rightarrow.png");
		$(this).children('img:last').attr("src", "/images/interface/leftarrow.png");
	},function(){
		$(this).parent().next().slideDown('fast');
		$(this).children('img:first,img:last').attr("src", "/images/interface/downarrow.png");
	});
	$('#heropane').sortable({
		axis: 'y',
		cancel: ":input, \
		         button, \
		         span, \
		         img[src='/images/interface/downarrow.png'], \
		         img[src='/images/interface/leftarrow.png'], \
		         img[src='/images/interface/rightarrow.png'], \
		         a, \
		         .cancel",
		cursor: 'move',
		handle: $('#heropane>div'),
		items:  '> div',
		update: function(e,ui){
			var helper = ui.helper.get(0);
			var list_order = [];
			$(this).children().each(function() {
				if (this !== helper && this.id !== '')
					list_order.push(this.id);
			});
			//alert(list_order);
		},
		scroll: true,
		scrollSensitivity: 50
	});
	$('#inventorymenu').accordion({
		autoHeight: false,
		header: '.head'
	});
	$('textarea').one("focus", function(){
		$(this).attr("value","");
	});
	$('.slot>.item,#inventoryitems .item').draggable({
		helper: 'clone'
	});
	dropfunc=function(ev,ui) {
		$(this).children(".item:first").appendTo("#inventoryitems");
		$(this).append($(ui.draggable));
	};
	$('.headslot').droppable({
		accept: ".item",
		drop: dropfunc
	});
	$('.slot').droppable({
		accept: ".item",
		drop: dropfunc
	});
	$('#unequip').droppable({
		accept: ".equipped",
		drop: function(ev,ui){$(ui.draggable).appendTo($('#inventoryitems'));}
	});
});
