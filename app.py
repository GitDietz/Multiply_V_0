from flask import Flask,url_for, render_template, session, redirect, request, g, jsonify
import logger as log, json
from multi import Q
from game_control import Perf
from operator import itemgetter
import utils, os

app = Flask(__name__)
mylog = log.logger('MLog.txt')
app.secret_key = 'aqd123'

theQ = Q()
myPerform = Perf('multi_set')


@app.route('/')
def homepage():
    mylog.add_log('Home route entered')
    return render_template('index.html')

@app.route('/start_game/<game_mode>')
def start_game(game_mode):
    #add validation to ensure only valid options are passed
    mylog.add_log('Route start_game entered with mode = ' + game_mode)
    #print('We\'re going for ' + game_mode)
    theQ.reset()
    myPerform.reset(game_mode)
    return render_template('game.html', question = theQ.q)


@app.route('/show_lb_direct/<game_mode>') #direct access to the leader board without plauying the game
def show_lb_direct(game_mode):
    mylog.add_log('direct leaderboard - route entered')
    myPerform.reset(game_mode)
    #mylog.add_log(myPerform.board_name + ' is the board name')
    myPerform.get_lead_list()
    leaders = myPerform.lead_list
    return render_template('leader_board.html', leaders = leaders,
                           board = myPerform.board_name)

@app.route('/submit_answer', methods = ['POST'])
def submit_answer():
    answer = request.form['answer'] #answer is the key in the json
    mylog.add_log('Answer route entered, Result received as ' + answer)
    last_result = theQ.result(answer)
    if theQ.invalid == False:
        myPerform.updateScore(theQ.r)
        theQ.reset()
        stats = str.replace(myPerform.stats,'\n','<br>')
        Q = theQ.q
    else:
        Q = None
    return jsonify({'result': 'OK good', 'reaction': last_result,
                    'next_question': Q , 'stat' : stats , 'stop_game' : myPerform.StopNow,
                    'tstop':myPerform.TStop, 'hi_score' : myPerform.hi_score, 'game_type': myPerform.Driver})


@app.route('/leader_board')
def show_leader_board():
    mylog.add_log('show leaderboard - route entered')
    #print(myPerform.CorrectRate)
    #print(myPerform.file)
    #print(myPerform.lead_list)
    #mylog.add_log(myPerform.board_name + ' is the board name')
    return render_template('leader_board.html', leaders = myPerform.lead_list,
                           board=myPerform.board_name)




@app.route('/get_new_high_score')#, methods = ['POST']
def get_new_high_score(): #No data needed since the score is available in the myPerform
    mylog.add_log('get_new_high_score - route entered')
    #print('score is '+str(myPerform.CorrectRate))
    #print('Board is = {}'.format(myPerform.board_name))
    #print(myPerform.lead_list)
    return render_template('add_leader.html',
                           score = myPerform.CorrectRate,
                           board = myPerform.board_name )


@app.route('/add_to_leader_board', methods = ['POST'])
def add_to_leader_board():
    # this will only update the scoreboard and then route to leaderboard
    mylog.add_log('add_to_leader_board - route entered')
    user_name = request.form['user_name']
    myPerform.lead_list = utils.add_high_score(myPerform.file,user_name,
                                               myPerform.CorrectRate,10)
    print(myPerform.lead_list)
    return jsonify({'result': 'Name added'})

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(port=4900, debug=True)