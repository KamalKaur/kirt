$(document).ready(function(){


  $('.promotion').on('input', function(){
    changed_id = this.id.split("_")[1]
    promotion = $('#promotion_' + changed_id).val();

    if (promotion < 0){
      $('#promotion_' + changed_id).css("color","red");
      //notification();
      }
    else {    
      reverse('src.views.ajaxpromotions', function(url) {
        var request_url = url + "?promotion=" + promotion + "&worker_id=" + changed_id;           
        $.ajax({
          url: request_url,
          success: function(data){
          if (data){ $('#promotion_' + changed_id).css("color","#1abc9c");}
          }
        });
      });
    }
  });
})
