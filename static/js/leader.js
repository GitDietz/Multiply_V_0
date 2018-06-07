
$(document).ready(function () {
console.log('Version 1.2')


//name_given is the button name
$('#name_given').click(function(event){

    event.preventDefault();
    //console.log('the answer button press function entered');
    //alert(#answer);
    var new_name = $('#the_name').val();
    //alert(new_name);
    //console.log('Answer given : ' + ans);
    //document.getElementById('answer').value = '';
    /* stuff from app
    add_heigh_score():
    #mylog.add_log('Answer route entered')
    user_name = request.form['user_name']
    */



    $.ajax({
        url: '/add_high_score',
        dataType : 'text',
        data: {user_name:new_name},      //$('form').serialize(),
        type: 'POST',
        success: function(response){
            console.log('returned from flask after name addition');
            console.log(response);
            var returned = JSON.parse(response);

            //console.log(returned['result']);
            //plan check response is indicating correct and then change elements else repeat
            $('#update_instruction').html('Welcome to the leaderboard!');
            $('.new_name').hide()
            $('.leaderboard').hide()
            $('#return_main').toggleClass('hidden')
        },
        error: function(error){
            console.log('error condition in ajax');
            console.log(error);
        }
    });  //end of Ajax

});

$('#stop_game').click(function(event){
event.preventDefault()
console.log('Stop button clicked')
window.location = "/"
});

 });
