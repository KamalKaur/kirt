
// The function that shows the success notification 
// and then hides after 2 seconds and redirects the 
// user to main page

// + 

// Do a most important thing: Submit the amount paid and save balance +
// all particulars for making the user capable of searching in future. 
// Here the history is made! (y)




function notification(){
    $(".notifications .messages .message").css("color","green");
    $(".notifications").children(".messages").fadeIn(300);

    setTimeout( function(){
        $(".notifications").children(".messages").fadeOut(500);
        
    },2000);
    
    setTimeout( function(){
        document.location.href = '/';
    },2000);
    
}

function deleteworker(url){
$.ajax({
  url: url,
  success: function(data) {
if(data){
  notification();
  }
  else{
  alert("Not deleted");
  }
  }
})
}



function paysalary(url){
  paid = $('.paid').val()
  alert(paid);
  var request_url = url + "&paid=" + paid;
  alert(request_url);
$.ajax({
  url: request_url,
  success: function(data) {
if(data){
  $('#paid').prop('disabled', true);
  $('#balance').html('Balance');
  $('#balance_value').html(data);
  $('#pay_salary').hide();
  }
  else{
  alert("Not paid");
  }
  }
})
}


$(document).ready(function(){
  $(function() {
    $(".notifications .messages").hide();
  })

  $(document).keyup(function(e) {
    if( e.keyCode === 13 ) {
    //e.preventDefault();
      alert("What?");
    //$( this ).trigger( 'submit' );
    }
  });



})
