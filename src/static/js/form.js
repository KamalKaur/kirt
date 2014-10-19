    <script language="javascript" type="text/javascript">
//On clicking advance, for popup
//$(function(){
//$('.js-popup-link').click(function(e){
// e.preventDefault();
//  $("#popup").dialog({modal: true}).dialog('open').load(this.href);
// })
//})
var opt = {
resizable: false, 
autoOpen: false,
closeOnEscape: true,
width: 515, 
height: 245
}

function popitup(url) {
$.ajax({
  url: url,
  success: function(data) {
$("#dialog-form").dialog(opt).html(data).dialog('open');
    }
  });
$('#dialog-form').bind('dialogclose', function() {
    var split = url.split("="); //URL has a pattern, splitted it from =.
    //alert(url);
    var idyear = split[1]; //After splitting from =, there is a pattern which is splitted from &
    //alert(idyear);
    var yearmonth = split[2]; 
    //alert(yearmonth);
    var month = split[3];
    //alert(month);
    var worker_id = idyear.split("&")[0];
    //alert(worker_id);
    var year = yearmonth.split("&")[0];
    //alert(year);
    request_url = "/return_advance/?worker_id=" + worker_id + "&month=" + month + "&year=" + year;
    $.ajax({
      url: request_url,
      success: function(data) { 
      $('#advance_'+ worker_id).attr("value", data);   
      }
    });
  });
  return false;
}
//function popitup(url) {
//newwindow=window.open(url,'Add Advance','height=400, width=450');
// if (window.focus) {newwindow.focus()}
// return false;
// }
</script>
<script>
$(document).ready(function(){
if ({{editable}} == '0')
$(".details :input").attr('readonly', true);

else
$(".details :input").attr('readonly', false);
})
</script>
