// Apply real time validations in add worker form
// Because that's a Django form, the id's of it's 
// fields are found using Ctrl+u after opening in 
// browser

function notification(){
    $(".notifications .messages .message").css("color","red");
    $(".notifications").children(".messages").fadeIn(300);
    setTimeout( function(){
        $(".notifications").children(".messages").fadeOut(400);   
    },2000);
}

$(document).ready(function(){

    $('.error > input').eq(0).focus();

    $('#id_first_name').on('input', function(){
        first_name = $("#id_first_name").val();      
        if (first_name == ""){
            $('#id_first_name').css("color","red");
            notification(); 
        }
        else if (first_name.match(/^[a-zA-Z ]*$/)){
            $('#id_first_name').css("color","#1abc9c");
        }          
        else{
            $('#id_first_name').css("color","red");
            notification();
        }
    });

    $('#id_middle_name').on('input', function(){
        first_name = $("#id_middle_name").val();      
        if (first_name == ""){
            $('#id_middle_name').css("color","red");
            notification(); 
        }
        else if (first_name.match(/^[a-zA-Z ]*$/)){
            $('#id_middle_name').css("color","#1abc9c");
        }          
        else{
            $('#id_middle_name').css("color","red");
            notification();
        }
    });


    $('#id_last_name').on('input', function(){
        last_name = $("#id_last_name").val();      
        if (last_name == ""){
            $('#id_last_name').css("color","red");
            notification(); 
        }
        else if (last_name.match(/^[a-zA-Z ]*$/)){
            $('#id_last_name').css("color","#1abc9c");
        }          
        else{
            $('#id_last_name').css("color","red");
            notification();
        }
    });

    $('#id_address').on('input', function(){
        address = $('#id_address').val();
        if (address == ""){
            $('#id_address').css("color","red");
            notification();
        }
        else{
            $('#id_address').css("color","#1abc9c");
        }
    });

    $('#id_basic_wage').on('input', function(){
        basic_wage = $("#id_basic_wage").val(); 

        if (basic_wage.match(/^[.]*$/)){
            $('#id_basic_wage').css("color","red");
            notification();
        }
        else{
            $('#id_basic_wage').css("color","#1abc9c");
        }
    })

    $('#id_provident_fund').on('input', function(){
        provident_fund = $("#id_provident_fund").val(); 

        if (provident_fund.match(/^[.]*$/)){
            $('#id_provident_fund').css("color","red");
            notification();
        }
        else{
            $('#id_provident_fund').css("color","#1abc9c");
        }
    })

})









