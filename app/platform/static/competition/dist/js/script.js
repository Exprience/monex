
/*----Switch Tabs ----*/
$(document).ready(function(){
	$(".nav-tabs a").click(function(){
		$(this).tab('show');
	});
$('#rootwizard').bootstrapWizard({'tabClass': 'nav nav-tabs'});
 
});
$(document).ready(function(){
    $("td").click(function(){
        $("#myModal2").modal();
    });
});
/*----------------------------Model PopUp----------------------*/
/*
<script>



$("alert").click(function(){
 form_submit('alert', '{% url "pop" %}')
});

<script>
$(document).ready(function(){
    $("#myBtn").click(function(){
        $("#myModal").modal();
    });
});
</script>



            var acc = document.getElementsByClassName("accordion");
            var i;

            for (i = 0; i < acc.length; i++) {
              acc[i].onclick = function(){
                this.classList.toggle("active");
                this.nextElementSibling.classList.toggle("show");
              }
            }
          </script>




function myFunction() {
  var input, filter, table, tr, td, i;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("table1");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

*/