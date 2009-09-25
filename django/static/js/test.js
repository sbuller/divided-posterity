$(document).ready(function(){

/*
 * Collapse/Expand widgets
 */
	$('.toggle').toggle(function(){
		$(this).parent().next().slideUp('fast');
		$(this).children('img:first').attr("src", "/images/interface/rightarrow.png");
		$(this).children('img:last').attr("src", "/images/interface/leftarrow.png");
	},function(){
		$(this).parent().next().slideDown('fast');
		$(this).children('img:first,img:last').attr("src", "/images/interface/downarrow.png");
	});

/*
 * Allow reordering of heropane widgets
 */
	$('#heropane').sortable({
		axis: 'y',
		cancel: ":input, \
		         button, \
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
	
/*
 * Inventory accordion menu
 */
	$('#inventorymenu').accordion({
		autoHeight: false,
		header: '.head1'
	});
	
/*
 * Textarea clearing
 */
	$('textarea').one("focus", function(){
		$(this).attr("value","");
	});
	
/*
 * Drag 'n' Drop for the inventory
 */
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
