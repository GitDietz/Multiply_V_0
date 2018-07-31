import random as Rd
import time as t
from datetime import datetime as d
import csv, os.path, utils
from operator import itemgetter

class Q(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.top = 13
        self.x = Rd.randint(1,self.top)
        self.y = Rd.randint(2,self.top)
        self.p = self.x*self.y
        self.q ='What is ' + str(self.x) + ' times ' + str(self.y) +'?'
        self.invalid = True #this means a non number value was given
        self.r = False #use to store the result

    def result(self,Resp):
        if Resp.isnumeric():
            self.invalid = False #numeric value given = no longer invalid and will be evaluated
            Answer = int(Resp)
            if Answer == self.p:
                self.r = True
                comment = 'Well done!'
            else:
                self.r = False
                comment = 'Oops!'
            return comment
        else:
            return 'Only whole numbers'


class Perf(object):  #is reset when new game is started
    def __init__(self,mode):
        self.reset(mode)

    def reset(self,mode):
        self.Asked = 0
        self.QLimit = 20
        self.Start = t.time() #this is in sec
        self.Correct = 0
        self.TStop = t.time() + 60
        self.Driver = mode
        self.StopNow = 'no'
        self.AnswerRate = 0.0 # Q/sec
        self.CorrectRate = 0.0
        self.running = True
        self.stats = ''
        self.hi_score = 'No'
        self.file = ''
        self.board_name = ''
        self.lead_list = []
        self.set_leader_board()

    def start_stop(self,toggle, mode = None):
        if mode:#change to only set mode nothing else
            return True
        else:
            return False

    def runCheck(self):
        if self.Driver == 'multi_time':
            if t.time()>=self.TStop:
                self.StopNow = 'yes'
        else:
            if self.Asked >= self.QLimit:
                self.StopNow = 'yes'
        if self.StopNow == 'yes':
            self.is_high_score()

    def RecalcRates(self):
        self.AnswerRate = round(self.Asked * 60 / (t.time() - self.Start),2)
        self.CorrectRate = round(self.Correct * 60 / (t.time() - self.Start),2)
        self.stats = "Answer rate Q/min = " + str(self.AnswerRate) +'\n'\
                    +"Correctly answered Q/min = {}".format(self.CorrectRate) +'\n'\
                    + "Scored {} out of {}".format(self.Correct,self.Asked)

    def updateScore(self,result):
        self.Asked += 1
        self.runCheck()
        if result == True:
            self.Correct +=1
        self.RecalcRates()

    def set_leader_board(self):
        l = utils.get_score_file(self.Driver)
        self.file = l[0]
        #print('file is {}'.format(self.file))
        self.board_name = l[1]

    def is_high_score(self):
        #print('func is_high_scrore starts')
        #now add the other content fomr ishighscore in app here toset high or not
        lead_list = utils.load_list_json(self.file)
        lead_list.sort(key=itemgetter('CPM'))
        low_val = lead_list[0]['CPM']
        #lead_list.sort(key=itemgetter('CPM'), reverse=True)
        #print(lead_list)
        self.lead_list = lead_list.sort(key=itemgetter('CPM'), reverse=True)
        if self.CorrectRate > low_val:
            self.hi_score = 'Yes'
        return self.hi_score

def write_results(StatSent,player):
    fname='GameStats.csv'
    now = d.now()
    if not os.path.exists(fname):
        with open(fname, 'w') as f:
            stat = "Game Stats for various players:"
            f.write(stat +'\n')
    if os.path.exists(fname):
        with open(fname, 'a') as f:
            stat = now.strftime('%Y/%m/%d %H:%M') + \
                   " Here are the stats for " + player + '\n' + StatSent
            f.write(stat +'\n')
