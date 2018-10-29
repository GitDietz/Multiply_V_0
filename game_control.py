import time as t
from datetime import datetime as d
import csv, os.path, utils
from operator import itemgetter
from multi import Q
from fractor import QFrac

class Config(object):
    #this stores the config data from the json until the app closes
    def __init__(self):
        self.reset()

    def reset(self):
        #what do we need for the leader boards only? game_mode
        self.config = utils.get_config()
        self.curr_game = ''
        self.curr_mode = ''
        self.curr_lb = ''
        self.curr_file = ''
        self.curr_var1 = 1
        self.curr_var2 = True
        self.lead_list = []
        print('Config set')

    def set(self,game_mode):
        found = False
        for f in self.config:
            print(f['game'] + ' file of ' + f['file'])
            if f['game'] == game_mode:
                self.curr_file = f['file']
                self.curr_lb = f['boardname']
                found = True
                break
        if found:
            # the format is frac_set, frac_time
            qset = game_mode.split("_")
            self.curr_game = qset[0]
            self.curr_mode = qset[1]
            if qset[0] == 'frac':
                self.curr_var1 = int(qset[2])
                if qset[3] == 'True':
                    self.curr_var2 = True
                else:
                    self.curr_var2 = False
        else:
            raise ValueError('No game of type ''{}'' found in config file'.format(game_mode))

    def get_lead_list(self):
        leadlist = utils.load_list_json(self.curr_file)
        leadlist.sort(key=itemgetter('CPM'), reverse=True)
        self.lead_list = leadlist
        return self.lead_list

    def set_question(self):
        if self.curr_game == 'multi':
            return Q()
        elif self.curr_game == 'frac':
            return QFrac(self.curr_var1, self.curr_var2)
        else:
            return None

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
        self.lead_list = []
        self.low_score = 0.0


    def start_stop(self,toggle, mode = None):
        if mode:#change to only set mode nothing else
            return True
        else:
            return False

    def get_lead_list(self):
        leadlist = utils.load_list_json(self.file)
        leadlist.sort(key=itemgetter('CPM'), reverse=True)
        self.lead_list = leadlist
        return self.lead_list

    def CheckForStop(self):
        if self.Driver == 'time':
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
        self.CheckForStop()
        if result == True:
            self.Correct +=1
        self.RecalcRates()

    def set_leader_board(self):
        l = utils.get_score_file(self.Driver)
        self.file = l[0]
        #print('file is {}'.format(self.file))
        self.board_name = l[1]

    def is_high_score(self):
        #print('func is_high_score starts')
        #now add the other content from ishighscore in app here toset high or not
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
