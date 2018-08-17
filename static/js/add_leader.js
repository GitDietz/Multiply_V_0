
$(document).ready(function () {
console.log('Version 1.0 add_leader')

//name_given is the button name
$('#name_given').click(function(event){
    event.preventDefault();
    var new_name = $('#the_name').val();
    //$(window.location).attr('href', '/add_to_leader_board')

    $.ajax({
        url: '/add_to_leader_board',
        dataType : 'text',
        data: {user_name:new_name},      //$('form').serialize(),
        type: 'POST',
        success: function(response){
            console.log('returned from flask after name addition')
            console.log(response)
            var returned = JSON.parse(response)
            var result = returned['result']
            $(window.location).attr('href', '/leader_board')
            //console.log(returned['result']);
            //plan check response is indicating correct and then change elements else repeat
            /*$('#update_instruction').html('Welcome to the leaderboard!');
            $('.new_name').hide()
            $('.score_header').hide()*/
           // $('.leaderboard').hide()
            },
        error: function(error){
            console.log('ajax error returning from add high score')
            console.log(error)
        }
    });  //end of Ajax

});

$('#stop_game').click(function(event){
event.preventDefault()
console.log('Stop button clicked')
window.location = "/"
});

 });
    //console.log('the answer button press function entered');
    //alert(#answer);    //alert(new_name);
    //console.log('Answer given : ' + ans);
    //document.getElementById('answer').value = '';
    /* stuff from app
    add_heigh_score():
    #mylog.add_log('Answer route entered')
    user_name = request.form['user_name']
    */