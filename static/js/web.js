function initMap() {
  var mapDiv = document.getElementById('map');
  var location = {lat: 47.9150500, lng: 106.9261500};
  var map = new google.maps.Map(mapDiv, {
    center: location,
    zoom: 18
  });
  var marker = new google.maps.Marker({
    position: location,
    map: map,
    title: 'Innosol'
  });
}


$(function () {
  $(".youtube").YouTubeModal({autoplay:0, width:640, height:480});
});

$(function(){
  $('button[date="daterange"]').daterangepicker();
});

var formAjaxSubmit = function(form, body) {
  $(form).submit(function (e) {
    e.preventDefault();
    $.ajax({
      type: $(this).attr('method'),
      url: $(this).attr('action'),
      data: $(this).serialize(),
      success: function (xhr, ajaxOptions, thrownError) {
        $(body).append('<p style="font-weight:bold;">'+ xhr.user+ ' : ' + xhr.msg +'</p><br/>');
      },
      error: function (xhr, ajaxOptions, thrownError) {
      }
    });
  });
};

formAjaxSubmit('#message-form', '#message-body');

//$('#bagts-button').click(function(){
//  if($('#bagts-button').hasClass('marginer')){
//    $('#bagts-button').removeClass('marginer');
//    $('#bagts-button').css({"margin-right": "0px"}, 10);
//    $('#bagts-body').hide();
//  }
//  else{
//    $('#bagts-button').addClass('marginer');
//    $('#bagts-button').css({"margin-right": "225px"}, 10);
//    $('#bagts-body').show(); 
//  }
//});

$(function(){
  $('[data-modal="modalview"]').DjangoModalRunner({
    //on_show_modal: function(){
    //},
    //on_hide_modal: function(){
    //},
    //on_hide_modal_after_submit: function(){
    //},
    on_submit: function(){
      //location.reload();
    }
    //on_done: function(){
    //}
  });
});
$(function() {
  $.fn.modal.Constructor.DEFAULTS.backdrop = 'static';
});