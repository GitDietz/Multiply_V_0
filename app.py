from flask import Flask,url_for, render_template, session, redirect, request, g, jsonify,flash
import logger as log, json
from game_control import Perf, Config
import utils, os

#Last edit 7:30

app = Flask(__name__)
mylog = log.logger('MLog.txt')
app.secret_key = 'aqd123'  #used before the  implementation of the config file
#app.config.from_object(Config)

C = Config()
#theQ = Q()
myPerform = Perf('set')
'''
@app.before_request
def confirm_origin():
    if C.last_page == '' and request.endpoint != 'homepage':
        mylog.add_log('before decorator triggered')
        #redirect to start/index
        return redirect(url_for('homepage'))
'''

@app.route('/')
def homepage():
    mylog.add_log('Home route entered')
    return render_template('index.html')

@app.route('/with_login')
def homepage_login():
    #activate this again when login operations are in plve
    if not session.get('logged_in'):
        mylog.add_log('not logged in, going to login')
        return render_template('login.html')
    else:
        mylog.add_log('Home route entered')
        return render_template('index.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
    #part of the login operation otherwise not required
    if request.form['password'] == 'password':
        session['logged_in'] = True
    else:
        flash('wrong password provided')
    return homepage()
#https://pythonspot.com/login-authentication-with-flask/

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return render_template('index.html')

@app.route('/start_game/<game_mode>')
def start_game(game_mode):
    global theQ
    #add validation to ensure only valid options are passed
    mylog.add_log('Route start_game entered with mode = ' + game_mode)
    C.set(game_mode)
    if C.gameset == True:
        C.last_page = 'Start game'
        myPerform.reset(C.curr_mode)
        theQ = C.set_question()
        return render_template('game.html', question = theQ.q)
    else:
        return render_template('invalid.html')

@app.route('/show_lb_direct/<game_mode>') #direct access to the leader board without plauying the game
def show_lb_direct(game_mode):
    mylog.add_log('direct leaderboard - route entered')
    C.set(game_mode)
    if C.gameset == True:
        C.last_page = 'Leader board direct'
        leaders = C.get_lead_list()
        board_name = C.curr_lb
        return render_template('leader_board.html', leaders = leaders,
                           board = board_name)
    else:
        return render_template('invalid.html')

@app.route('/submit_answer', methods = ['POST'])
def submit_answer():
    C.last_page = 'Answer submitted'
    global theQ
    HS = 'No'
    answer = request.form['answer'] #answer is the key in the json
    mylog.add_log('Answer route entered, Result received as ' + answer)
    last_result = theQ.result(answer)
    if theQ.invalid == False:
        mylog.add_log('valid format answer received')
        myPerform.updateScore(theQ.r)
        if myPerform.StopNow == 'yes':#lower case for javascript = yes
            HS = C.is_high_score(myPerform.CorrectRate) #is title case = Yes
            Q = 'No Question'
            mylog.add_log('Game will stop')
        else:
            theQ.reset()
            Q = theQ.q

    stats = str.replace(myPerform.stats, '\n', '<br>')
    return jsonify({'result': 'OK good', 'reaction': last_result,
                    'next_question': Q , 'stat' : stats , 'stop_game' : myPerform.StopNow,
                    'tstop':myPerform.TStop, 'hi_score' : HS, 'game_type': myPerform.Driver})


@app.route('/leader_board')
def show_leader_board():
    C.last_page = 'End Game leader board'
    mylog.add_log('show leaderboard - route entered')
    return render_template('leader_board.html', leaders = C.lead_list,
                           board=C.curr_lb)


@app.route('/get_new_high_score')#, methods = ['POST']
def get_new_high_score(): #No data needed since the score is available in the myPerform
    mylog.add_log('get_new_high_score - route entered')
    C.last_page = 'Get new high score'
    return render_template('add_leader.html',
                           score = myPerform.CorrectRate,
                           board = C.curr_lb )


@app.route('/add_to_leader_board', methods = ['POST'])
def add_to_leader_board():
    C.last_page = 'Add name to leader board'
    mylog.add_log('add_to_leader_board - route entered')
    user_name = request.form['user_name']
    C.lead_list = utils.add_high_score(C.curr_file,user_name,
                                               myPerform.CorrectRate,10)
    return jsonify({'result': 'Name added'})


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(port=4900, debug=True)