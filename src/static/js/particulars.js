    function notification(){
        $(".notifications .messages .message").css("color","green");
        $(".notifications").children(".messages").fadeIn(300);
        setTimeout( function(){
            $(".notifications").children(".messages").fadeOut(400);
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
  alert("not deleted");
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
         //   e.preventDefault();
            alert("oho");
            //$( this ).trigger( 'submit' );
        }
    });
})
