$(function(){
  $('a[data-modal="modalview"]').DjangoModalRunner({
    //alert($(this).attr('class'));
    on_show_modal: function(){
      $('#generic-modal .modal-dialog').addClass('modal-lg')
    },
    //on_hide_modal: function(){
    //  location.reload();
    //},
    //on_hide_modal_after_submit: function(){
    //  location.reload();
    //},
    on_submit: function(){
      alert("uuganaa");
    //  $('#modal-form').submit(function(event){
    //    event.preventDefault();
    //    $.ajax({
    //      url: $(this).attr('action'),
    //      method: 'post',
    //      data: $(this).serialize()
    //    }).done(function(response){
    //      $('#generic-modal').modal("hide");
    //    });
    //  });
      //location.reload();
    //}
    //on_done: function(){
    },
  });
});
//$(function() {
//  $.fn.modal.Constructor.DEFAULTS.backdrop = 'static';
//  $.fn.modal.Constructor.DEFAULTS.class = 'modal-lg';
//});


$(function() {
  var pgurl = window.location.pathname;
  $("ul.sidebar-menu a").each(function(){
    if($(this).attr("href") == pgurl){
      if($(this).parent().parent('ul').hasClass('treeview-menu')){
        $(this).parent().parent().parent('li').addClass("active").siblings().removeClass('active');
        $(this).parent('li').addClass("active").siblings().removeClass('active');
      }
      else{
        $(this).parent('li').addClass("active").siblings().removeClass('active');
      }
    }
  })
});


$('a[data-toggle="tab"]').click(function (e) {
  e.preventDefault();
  $(this).tab('show');
});

$('a[data-toggle="tab"]').on("shown.bs.tab", function (e) {
    var id = $(e.target).attr("href");
    localStorage.setItem('selectedTab', id)
});

var selectedTab = localStorage.getItem('selectedTab');
if (selectedTab != null) {
  $('a[data-toggle="tab"][href="' + selectedTab + '"]').tab('show');
};

/* DateTimeRangePicker */
function managerDaterange(button_id){
  $(function () {
    $(button_id).daterangepicker({
      "buttonClasses": "btn btn-sm btn-flat",
      "applyClass": "btn-success",
      "cancelClass": "btn-default",
      locale: {
        applyLabel: 'Шүүх',
        cancelLabel: 'Цуцлах',
        customRangeLabel : 'Гараар сонгох',
        "daysOfWeek": [
          "Бү","Да","Мя","Лх","Пү","Ба","Бя",
        ],
        "monthNames": [
          '1 сар','2 сар','3 сар','4 сар','5 сар','6 сар','7 сар','8 сар','9 сар','10 сар','11 сар','12 сар',
        ],
      },
      //opens : 'left',
      ranges: {
        'Өнөөдөр': [moment(), moment()],
        'Өчигдөр': [moment().subtract('days', 1), moment().subtract('days', 1)],
        'Сүүлийн 7 хоног': [moment().subtract('days', 6), moment()],
        'Сүүлийн 30 хоног': [moment().subtract('days', 29), moment()],
        'Энэ сар': [moment().startOf('month'), moment().endOf('month')],
        'Өнгөрсөн сар': [moment().subtract('month', 1).startOf('month'), moment().subtract('month', 1).endOf('month')]
      },
    });

    $('#filter5').on('apply.daterangepicker', function (ev, picker) {
      $('#id_filter_type').val(5);
      $('#id_start').val(picker.startDate.format('YYYY-MM-DD'));
      $('#id_end').val(picker.endDate.format('YYYY-MM-DD'));
      $("#competition_form").submit();
    });
  });
};

function managerDatatable(table_id){
  $(table_id).DataTable({
    "oLanguage" : {
      "sInfo" : "Нийт _TOTAL_ бичлэгнээс _START_-с _END_ хүртэл харуулав.",
      "sEmptyTable": "Бичлэг олдсонгүй",
      "sInfoEmpty": "Нийт 0 бичлэгнээс 0-с 0 хүртэл харуулав.",
      "oPaginate" : {
        "sFirst" : "эхлэл",
        "sLast" : "төгсгөл",
        "sNext" : "дараах",
        "sPrevious" : "өмнөх",
      }
    },
    "paging": true,
    "lengthChange": false,
    "searching": false,
    "ordering": false,
    "info": true,
    "autoWidth": false,
  });
}


$(document).ajaxStart(function() { Pace.restart(); });