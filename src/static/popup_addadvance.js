// Take data from the popup for adding more advance to view given in request-url, 
// when they are changed and the view saves it in database.
// Changed_id is introduced for separating the ids for different rows.

$(document).ready(function(){  

// On changing Paid Salary column    
  $('.popupadvance').change(function(){
    changed_id = this.id.split("_")[1]
    popupadvance = $('#popupadvance_' + changed_id).val();
    request_url = "/ajaxpopupadvance/?popupadvance=" + popupadvance + "&worker_id=" + changed_id;
    $.ajax({
      url: request_url,
      success: function(data){
      alert(data);
      }
    })
  })
})


