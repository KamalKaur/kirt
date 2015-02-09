// Take data from the fields of daily_attendance form to views, when they are changed,
// Changed_id is introduced for separating the ids for different rows.

$(document).ready(function(){
  $('.attendance').on('click', function(){    
  changed_id = this.id.split("_")[1]
  if($(this).prop("checked") == true){
     //alert(changed_id);
    //alert("Checkbox is checked.");
    attendance = $('#attendance_' + changed_id).val();
    attendance="1";
    //alert(attendance);
    reverse('src.views.ajax_daily_attendance', function(url) {
      var request_url = url + "?attendance=" + attendance + "&worker_id=" + changed_id;
      $.ajax({
        url: request_url,
        success: function(data){
        if (data){ 
          $('#attendance_' + changed_id).css("color","#1abc9c");
        } 
        }
      });
    });
  }
  else if($(this).prop("checked") == false){
    
attendance = $('#attendance_' + changed_id).val();
    attendance="-1";
    //alert(attendance);
    reverse('src.views.ajax_daily_attendance', function(url) {
      var request_url = url + "?attendance=" + attendance + "&worker_id=" + changed_id;
      $.ajax({
        url: request_url,
        success: function(data){
        if (data){ 
          alert("Attendance unmarked");
        } 
        }
      });
    });
}
  });


  $('.overtime').on('input', function(){
  changed_id = this.id.split("_")[1]
  overtime = $('#overtime_' + changed_id).val();
  //alert(overtime);  
 if ( overtime < 0 ){
    $('#overtime_' + changed_id).css("color","red");
    //notification();
    } 
  else if ( overtime > 10 ){ 
    $('#overtime_' + changed_id).css("color","red");
    //notification();
    }
  else if  (overtime > 0 && overtime < 11){ 
    reverse('src.views.ajax_daily_attendance', function(url) {
      var request_url = url + "?overtime=" + overtime + "&worker_id=" + changed_id;
      $.ajax({
        url: request_url,
        success: function(data){
        if (data){ 
          $('#overtime_' + changed_id).css("color","#1abc9c");
        } 
        }
      });
    });
    }
  });

})

  //
  //alert(attendance);
  

