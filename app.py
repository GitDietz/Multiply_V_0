from flask import Flask,url_for, render_template, session, redirect, request, g, jsonify
import logger as l, json
from multi import Q,Perf,write_results
from operator import itemgetter
import utils, os
#from flask_table import Table, Col

app = Flask(__name__)
#mylog = l.logger('NinjaLog.txt')
app.secret_key = 'aqd123'

theQ = Q()
myPerform = Perf('time')
stats = ''
stop_or_not = 'no'
hi_score = 'No'
the_folder = os.path.dirname(os.path.abspath(__file__))
l_file = os.path.join(the_folder,'static/files/leaders.json')
l_file_20 = os.path.join(the_folder,'static/files/leaders20.json')
use_file = l_file

def is_high_score():
    score = myPerform.CorrectRate
    l = utils.load_list_json(use_file)
    l.sort(key=itemgetter('CPM'))
    low_val = l[0]['CPM']
    l.sort(key=itemgetter('CPM'), reverse=True)
    if score > low_val:
        return 'Yes'
    else:
        return 'No'

@app.route('/')
def homepage():
    #mylog.add_log('Home route entered')
    return render_template('index.html')

@app.route('/start_game/<game_mode>')
def start_game(game_mode):
    global use_file
    #mylog.add_log('Route start_game entered with mode = ' + game_mode)
    #game modes = Set time or anything else
    print('We\'re going for ' + game_mode)
    theQ.reset()
    myPerform.reset(game_mode)
    if myPerform.Driver == 'Set time':
        use_file = l_file
    else:
        use_file = l_file_20
    return render_template('game.html', question = theQ.q, answer = theQ.p)


@app.route('/submit_answer', methods = ['POST'])
def submit_answer():
        #mylog.add_log('Answer route entered')
    answer = request.form['answer'] #snwer is the key in the json
        #mylog.add_log('Result received as ' + answer)
    last_result = theQ.result(answer)

    if theQ.invalid == False:
        myPerform.updateScore(theQ.r)
        theQ.reset()
        stats = str.replace(myPerform.stats,'\n','<br>')
        if myPerform.StopNow:
            stop_or_not = 'yes'
            hi_score = is_high_score()
        else:
            stop_or_not = 'no'
        Q = theQ.q
    else:
        Q = None
    return jsonify({'result': 'OK good', 'reaction': last_result,
                    'next_question': Q , 'stat' : stats , 'stop_game' : stop_or_not,
                    'tstop':myPerform.TStop, 'hi_score' : hi_score, 'game_type': myPerform.Driver})


@app.route('/leader_board')
def show_leader_board():
    #print(myPerform.CorrectRate)
    print(use_file)
    score = myPerform.CorrectRate
    l = utils.load_list_json(use_file)
    #print(l)
    l.sort(key=itemgetter('CPM'))
        #for leader in l:
        #    print(leader)

    low_val = l[0]['CPM']
    add_to_list = False
    l.sort(key=itemgetter('CPM'),reverse = True)
    if score>low_val:
        add_to_list = True
    return render_template('leader_board.html', leaders = l, score = score, add_to_list = add_to_list)


@app.route('/add_high_score', methods = ['POST'])
def add_heigh_score():
    #mylog.add_log('Answer route entered')
    user_name = request.form['user_name']
    print('score is '+str(myPerform.CorrectRate))
    print('The new top score is going to be added : {}'.format(user_name))
    l = utils.add_high_score(use_file,user_name,myPerform.CorrectRate,10)
    print(l)
    return jsonify({'result': 'Updated','leaders':l})


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(port=4900, debug=True)
#https://codereview.stackexchange.com/questions/69570/insert-json-data-into-rendered-template-after-ajax-call
