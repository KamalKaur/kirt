// Take data from the form fields to views, when they are changed
// Changed_id is introduced for separating the ids for different rows.

$(document).ready(function(){
  
  //On changing the Days column
  $('.days').change(function(){
  changed_id = this.id.split("_")[1]
  days = $('#days_' + changed_id).val();
  request_url = "/ajaxrequest/?days=" + days + "&worker_id=" + changed_id;
  $.ajax({
    url: request_url,
    success: function(data){
    alert(data);
    }
    });
  });

  // On changing overtime column
  $('overtime').change(function(){
    changed_id = this.id.split("_")[1]
    alert(changed_id);
    overtime = $('#overtime_' + changed_id).val();
    request_url = "/ajaxrequest/?overtime=" + overtime + "&worker_id=" + changed_id;
    alert(request_url);
    $.ajax({
      url: request_url,
      success: function(data){
      alert(data);
      }
    })
  })

  // On changing Paid Salary column    
  $('.paid').change(function(){
    changed_id = this.id.split("_")[1]
    alert(changed_id);
    paid = $('#paid_' + changed_id).val();
    request_url = "/ajaxrequestpaid/?paid=" + paid + "&worker_id=" + changed_id;
    $.ajax({
      url: request_url,
      success: function(data){
      alert(data);
      }
    })
  })

  // On changing Advance column
  $('.advance').change(function(){
    changed_id = this.id.split("_")[1]
    advance = $('#advance_' + changed_id).val();
    request_url = "/ajaxrequestadvance/?advance=" + advance + "&worker_id=" + changed_id;
    $.ajax({
      url: request_url,
      success: function(data){
      alert(data);
      }
    })
  })
  
  // Popup for adding advance
  
})
	
