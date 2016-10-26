$(function() {
  var pgurl = window.location.pathname;
  $("#header  ul.nav.navbar-nav a").each(function(){
    if($(this).attr("href") == pgurl){
       $(this).parent('li').addClass("active").siblings().removeClass('active');
    }
  })
});


$(document).ajaxStart(function() { Pace.restart(); });



(function($){

	$(document).on('click', '.ajax-load', function(e){
		e.preventDefault();
		var id = $(this).attr("href");
		var url = $(this).attr("load-url");
		$(id).load(url, function (response, status, xhr) {
		});
		$(this).parent('li').addClass("active").siblings().removeClass('active');
	});

	$(document).on("click", "[data-toggle='ajax-modal']", function(e){
		e.preventDefault();
		url = $(this).attr("href");
		$("#ModalGeneral").load(url, function (response, status, xhr) {
			$("#ModalGeneral").modal('show');
			$('#ModalGeneral form').attr('action', url);
		});
	});
	
	$(document).on('submit', '#ModalGeneral form', function(e){
		e.preventDefault();
		var action = $(this).attr('action');
		$.ajax({
			type: $(this).attr('method'),
			url: action,
			data: $(this).serialize(),
			success: function (xhr, ajaxOptions, thrownError) {
				if ( $(xhr).find('.errorlist').length > 0 ) {
					
					$('#ModalGeneral').html(xhr);
					$('#ModalGeneral form').attr('action', action);
				}
				else {
					$('#ModalGeneral').modal('hide');
					
					if(xhr.alert_create == true){
						alert_create(xhr.id, xhr.price, xhr.isBuy, xhr.isHigherThan, xhr.created_at, xhr.competition_id);
					}

					if(xhr.alert_update == true){
						alert_update(xhr.id, xhr.price, xhr.isBuy, xhr.isHigherThan, xhr.created_at, xhr.competition_id);
					}

					if(xhr.alert_delete == true){
						alert_delete(xhr.id);
					}

					if(xhr.currency_buy == true){
						//alert_delete(xhr.id);
						alert('augasdgasdgagas');
					}

					$.notify(
					{
						icon: 'icon fa fa-check-circle',
						message: "Үйлдэл амжилттай хийгдлээ"
					},
					{
						type: 'success',
						placement: {
							from: "top",
							align: "right"
						},
					}
					);
				}
			},
			error: function (xhr, ajaxOptions, thrownError) {
			}
		});
	});


})(jQuery);

function alert_delete(id){
	$('#alert_'+id).remove();
};

function alert_create(id, price, isBuy, isHigherThan, created_at, competition_id){
	$('#alert_table').prepend('<tr id=alert_'+id+'><td>'+price+'</td><td class="text-center">'+isBuy+'</td>\
	<td class="text-center">'+isHigherThan+'</td><td class="text-center">'+created_at+'</td>\
	<td class="text-center"><button data-toggle="ajax-modal" href="/platform/alert/update/'+competition_id+'/'+id+'/" class="btn btn-plat btn-xs">Засах</button></td>\
	<td class="text-center"><button data-toggle="ajax-modal" href="/platform/alert/delete/'+competition_id+'/'+id+'/" class="btn btn-plat btn-xs">Устгах</button></td></tr>');
};

function alert_update(id, price, isBuy, isHigherThan, created_at, competition_id){
	$('#alert_'+id).replaceWith('<tr id=alert_'+id+'><td>'+price+'</td><td class="text-center">'+isBuy+'</td>\
	<td class="text-center">'+isHigherThan+'</td><td class="text-center">'+created_at+'</td>\
	<td class="text-center"><button data-toggle="ajax-modal" href="/platform/alert/update/'+competition_id+'/'+id+'/" class="btn btn-plat btn-xs">Засах</button></td>\
	<td class="text-center"><button data-toggle="ajax-modal" href="/platform/alert/delete/'+competition_id+'/'+id+'/" class="btn btn-plat btn-xs">Устгах</button></td></tr>');
};

$(document).ready(function(){
	$(".scrolling").slimScroll({
	    height: $(".scrolling").height(),
	    //size: '10px',
	    //position: 'left',
	    //color: '#ffcc00',
	    //alwaysVisible: true,
	    //distance: '20px',
	    //start: $('#child_image_element'),
	    //railVisible: true,
	    //railColor: '#222',
	    //railOpacity: 0.3,
	    //wheelStep: 10,
	    //allowPageScroll: false,
	    //disableFadeOut: false
	});
})

$(document).ready(function(){
	$("#value").slimScroll({
	    height: $("#value").height(),
	    //size: '10px',
	    //position: 'left',
	    //color: '#ffcc00',
	    //alwaysVisible: true,
	    //distance: '20px',
	    //start: $('#child_image_element'),
	    //railVisible: true,
	    //railColor: '#222',
	    //railOpacity: 0.3,
	    //wheelStep: 10,
	    //allowPageScroll: false,
	    //disableFadeOut: false
	});
})