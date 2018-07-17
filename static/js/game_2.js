
$(document).ready(function () {
console.log('Version 2.3 Deciding on destination at game end, fade test 30000')

function clear_redirect(){
alert('Finished waiting')
}


$('#answered').click(function(event){

    event.preventDefault();
    //console.log('the answer button press function entered');
    //alert(#answer);
    var ans = $('#answer').val();
    //alert(ans);
    //console.log('Answer given : ' + ans);
    document.getElementById('answer').value = '';

    $.ajax({
        url: '/submit_answer',
        dataType : 'text',
        data: {answer:ans},      //$('form').serialize(),
        type: 'POST',
        success: function(response){
            //console.log('returned from flask');
            console.log(response);
            var returned = JSON.parse(response);
            //console.log(returned['result']);
            $('#game_stat').html(returned['stat'])
            $('#feedback').html(returned['reaction'])
            if (returned['next_question']){ $('#question').html(returned['next_question']) }

            var stopper = returned['stop_game']
            console.log(stopper)
            //if (returned['stop_game']){console.log('value recognised')}
            if (stopper === "yes"){
                console.log('I have a yes to stop the game')
                $('#return_main').toggleClass('hidden')
                //setTimeout(clear_redirect,1500)

                $('.question').hide()
                $('#stop_game').hide()
                $('.jumbotron-heading').html('Moving to leaderboard')
                $('.jumbotron-heading').fadeOut(30000)


                if (returned['hi_score'] === "Yes"){
                    $(window.location).attr('href', '/add_high_score')
                }else{
                    $(window.location).attr('href', '/leader_board')
                }
            }
            //else {console.log('it is still no')}


        },
        error: function(error){
            console.log('error condition in ajax');
            console.log(error);
        }
    });
});

$('#stop_game').click(function(event){
event.preventDefault()
console.log('Stop button clicked')
window.location = "/"
});
});
