
$(document).ready(function () {
console.log('Version 2.1')

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
            //console.log(response);
            var returned = JSON.parse(response);
            //console.log(returned['result']);
            $('#game_stat').html(returned['stat']);

            $('#feedback').html(returned['reaction']);

            if (returned['next_question']){ $('#question').html(returned['next_question']) }


            var stopper = returned['stop_game']
            //console.log(stopper)
            //if (returned['stop_game']){console.log('value recognised')}

            if (stopper === "yes"){
                //console.log('I have a yes to stop the game')
                $('.question').hide()
                $('#stop_game').hide()
                $('.jumbotron-heading').html('Your game is finished, Click the <strong>Return to Main</strong> button to start again')
                $('#return_main').toggleClass('hidden')
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
