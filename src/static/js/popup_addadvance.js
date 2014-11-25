// Take data from the popup for adding more advance to view given in request-url, 
// when they are changed and the view saves it in database.
// Changed_id is introduced for separating the ids for different rows.

$(document).ready(function(){  

//  On changing Paid Salary column    
    $('.popupadvance').on('change', function(){
        changed_id = this.id.split("_")[1]
        popupadvance = $('#popupadvance_' + changed_id).val();
        
        request_url = "ajaxpopupadvance/?popupadvance=" + popupadvance + "&worker_id=" + changed_id; 
        if (popupadvance == ""){
            $('#popupadvance_' + changed_id).css("color","red");
        }
        else if (popupadvance.match(/^[0-9]+$/)){
            $.ajax({
                url: request_url,
                success: function(data){
                    if (data) {
                        $('#popupadvance_' + changed_id).css("color","#2ecc71");
                    }
                }
            });
        }
        else {
            $('#popupadvance_' + changed_id).css("color","red");
        }
    });
 
    $('.popupadvance').on('input', function(){
        changed_id = this.id.split("_")[1]
        popupadvance = $('#popupadvance_' + changed_id).val();
        if (popupadvance.match(/^[0-9]+$/)){
            $('#popupadvance_' + changed_id).css("color","#2ecc71");
        }
        else {
            $('#popupadvance_' + changed_id).css("color","red");
        }
    })
        
    
})



 

