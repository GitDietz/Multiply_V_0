import random as Rd
import time as t
from datetime import datetime as d
import csv, os.path

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
        self.QLimit = 5
        self.Start = t.time() #this is in sec
        self.Correct = 0
        self.TStop = t.time() + 60
        self.Driver = mode #time=run against set time
        self.StopNow = False
        self.AnswerRate = 0.0 # Q/sec
        self.CorrectRate = 0.0
        self.running = True
        self.stats = ''
        self.hi_score = 'No'


    def start_stop(self,toggle, mode = None):# toggle on/off, mode='Set questions, Set time'
        if mode:#change to only set mode nothing else
            return True
        else:
            return False

    def runCheck(self):
        if self.Driver == 'Set time':
            if t.time()>=self.TStop:
                self.StopNow = True
        else:
            if self.Asked >= self.QLimit:
                self.StopNow = True

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




# Game1: 20 questions, timed performance