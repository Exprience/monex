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
				}
			},
			error: function (xhr, ajaxOptions, thrownError) {
			}
		});
	});


})(jQuery);