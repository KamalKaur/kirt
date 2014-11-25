// Take data from the form fields to views, when they are changed
// Changed_id is introduced for separating the ids for different rows.

$(document).ready(function(){

    $(function() {
        $(".notifications .messages").hide();
//      $(".notifications").click(function() {
//          if ($(this).children(".messages").children().length > 0) {
//              $(this).children(".messages").fadeToggle(300);
//          }
//      });
    });

    function notification(){
        $(".notifications .messages .message").css("color","red");
        $(".notifications").children(".messages").fadeIn(300);
        setTimeout( function(){
            $(".notifications").children(".messages").fadeOut(400);
        },2000);
    }

//  On changing the Days column:   
    $('.days').on('input', function(){     
        changed_id = this.id.split("_")[1]
        days = $('#days_' + changed_id).val();
        request_url = "ajaxrequest/?days=" + days + "&worker_id=" + changed_id;

        if ( days < 1 ){
            $('#days_' + changed_id).css("color","red");
            notification();
        } 
        else if ( days > 31 ){  // Days in month? :D
            $('#days_' + changed_id).css("color","red");
            notification();
        }
        else {
            $.ajax({
                url: request_url,
                success: function(data){
//                  $('#days_' + changed_id).css("border","1px solid green");
//                  Change text color green:
                    if (data){
                        $('#days_' + changed_id).css("color","#1abc9c");
                    }
//                  Undo CSS but basically apply yet another CSS after some 1000 mili seconds :p
//                  setTimeout( function(){
//                      $('#days_' + changed_id).css("color","black");
//                  },1000);
                }
            });
        }
    });

//  On changing overtime column:
    $('.overtime').on('input', function(){
        changed_id = this.id.split("_")[1]
        overtime = $('#overtime_' + changed_id).val();
        request_url = "ajaxrequest/?overtime=" + overtime + "&worker_id=" + changed_id;

        if ( overtime < 1 ){
            $('#overtime_' + changed_id).css("color","red");
            notification();
        } 
        else if ( overtime > 50 ){  
            $('#overtime_' + changed_id).css("color","red");
            notification();
        }
        else {
            $.ajax({
                url: request_url,
                success: function(data){
                    if (data) $('#overtime_' + changed_id).css("color","#1abc9c");
//                  For writing data on next page..
//                  document.write(data); 
                }
            });
        }
    });

//  On changing Paid Salary column:   
    $('.paid').on('input', function(){
        changed_id = this.id.split("_")[1]
        paid = $('#paid_' + changed_id).val();
        request_url = "ajaxrequestpaid/?paid=" + paid + "&worker_id=" + changed_id;

        if (paid == ""){
            $('#paid_' + changed_id).css("color","red");
            notification();
        }
        else if (paid < 1){
            $('#paid_' + changed_id).css("color","red");
            notification();
        }
        else {               
            $.ajax({
                url: request_url,
                success: function(data){
                    if (data){ $('#paid_' + changed_id).css("color","#1abc9c");}
                }
            });
        }
    });
  
    // Popup for adding advance 
    // Is it used anymore? 
    $('.addadvance').click(function() {
        changed_id = this.id.split("_")[1]
        request_url = "ajaxrequestadvance/?worker_id=" + changed_id;
        alert(request_url);
        $.ajax({
            url: request_url,
            success: function(data){
            alert(data);
            }
        })
    })  
       
    // Click on add advance button and it greet you with a dialog box to add more values
    $('.dialog').click(function () {
        changed_id = this.id.split("_")[1]
        request_url = "popupadvance/?worker_id=" + changed_id;
        alert(request_url);
        $.ajax({
            url: request_url,
            success: function(data) {
            $(".dialog").load(request_url).dialog('open');
            }
        });
    })

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
