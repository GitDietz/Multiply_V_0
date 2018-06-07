from flask import Flask,url_for, render_template, session, redirect, request, g, jsonify
import logger as l, json
from multi import Q,Perf,write_results


app = Flask(__name__)
#mylog = l.logger('NinjaLog.txt')
app.secret_key = 'aqd123'

theQ = Q()
myPerform = Perf('time')
stats = ''
stop_or_not = 'no'


@app.route('/')
def homepage():
    #mylog.add_log('Home route entered')
    return render_template('index.html')

@app.route('/start_game/<game_mode>')
def start_game(game_mode):
    #mylog.add_log('Route start_game entered with mode = ' + game_mode)
    #game modes = Set time or anything else
    print('Were going for ' + game_mode)
    theQ.reset()
    myPerform.reset(game_mode)

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
        #should the game stop?
        if myPerform.StopNow:
            stop_or_not = 'yes'
        else:
            stop_or_not = 'no'
        print('To stop or not : ' + stop_or_not)
        Q = theQ.q
    else:
        Q = None
    return jsonify({'result': 'OK good', 'reaction': last_result, 'next_question': Q , 'stat' : stats , 'stop_game' : stop_or_not})

@app.route('/backimage')
def backimage():
    return render_template('other.html')



@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404



if __name__ == "__main__":
    app.run(port=4900, debug=True)
