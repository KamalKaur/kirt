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
        success: function(){
            // Highlight input box border:
            //$('#days_' + changed_id).css("border","1px solid green");

            // Change text color green:
            $('#days_' + changed_id).css("color","#2ecc71");

            // Undo CSS but basically apply yet another CSS after some 1000 mili seconds :p
            // setTimeout( function(){
            // $('#days_' + changed_id).css("color","black");
            // },1000);
        }
      });
  });

  // On changing overtime column
  $('.overtime').change(function(){
    changed_id = this.id.split("_")[1]
    overtime = $('#overtime_' + changed_id).val();
    request_url = "/ajaxrequest/?overtime=" + overtime + "&worker_id=" + changed_id;
    $.ajax({
      url: request_url,
      success: function(data){
      // For writing on next page..
      //document.write(data); 

      }
    })
  })

  // On changing Paid Salary column    
  $('.paid').change(function(){
    changed_id = this.id.split("_")[1]
    paid = $('#paid_' + changed_id).val();
    request_url = "/ajaxrequestpaid/?paid=" + paid + "&worker_id=" + changed_id;
    $.ajax({
      url: request_url,
      success: function(data){
      alert(data);
      }
    })
  })
  
  // Popup for adding advance 
  // Is it used anymore? 
  $('.addadvance').click(function() {
    changed_id = this.id.split("_")[1]
    request_url = "/ajaxrequestadvance/?worker_id=" + changed_id;
    alert(request_url);
    $.ajax({
      url: request_url,
      success: function(data){
      alert(data);
      }
    })
  })  
       
  // Click on add advance button
  $('.dialog').click(function () {
    changed_id = this.id.split("_")[1]
    request_url = "/popupadvance/?worker_id=" + changed_id;
    alert(request_url);
     $.ajax({
    url: request_url,
    success: function(data) {
    $(".dialog").load(request_url).dialog('open');
    }
  });
})

//$("#dialog-form").hide();
//$("#click").click(function(){
//$("#dialog-form").slideToggle();
//  });

  $(".contact").click(function(ev) { // for each edit contact url
        ev.preventDefault(); // prevent navigation
        var url = $(this).data("form"); // get the contact form url
        alert(url);
        $("#contactModal").load(url, function() { // load the url into the modal
            $(this).modal('show'); // display the modal on url load
        });
        return false; // prevent the click propagation
    })
})	
