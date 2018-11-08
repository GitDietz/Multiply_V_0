import time as t
from datetime import datetime as d
import csv, os.path, utils
from operator import itemgetter
from multi import Q
from fractor import QFrac
import logger as log

class Config(object):
    #this stores the config data from the json until the app closes
    def __init__(self):
        self.mylog = log.logger('MLog.txt')
        self.config = utils.get_config()
        self.curr_game = ''
        self.curr_mode = ''
        self.curr_lb = ''
        self.curr_file = ''
        self.curr_var1 = 1
        self.curr_var2 = True
        self.lead_list = []
        self.last_page = ''
        self.mylog.add_log('Config initialised')
        self.gameset = False

    def set(self,game_mode):
        self.mylog.add_log('Config, set method start')
        found = False
        for f in self.config:
            print(f['game'] + ' file of ' + f['file'])
            if f['game'] == game_mode:
                self.curr_file = f['file']
                self.curr_lb = f['boardname']
                qset = game_mode.split("_")
                self.curr_game = qset[0]
                self.curr_mode = qset[1]
                if qset[0] == 'frac':
                    self.curr_var1 = int(qset[2])
                    if qset[3] == 'True':
                        self.curr_var2 = True
                    else:
                        self.curr_var2 = False
                found = True
                self.gameset = True
                break
        #if not found:
            #raise ValueError('No game of type ''{}'' found in config file'.format(game_mode))
         #   return False

    def get_lead_list(self):
        self.mylog.add_log('Config, get_lead_list method start')
        leadlist = utils.load_list_json(self.curr_file)
        leadlist.sort(key=itemgetter('CPM'), reverse=True)
        self.lead_list = leadlist
        return self.lead_list

    def set_question(self):
        self.mylog.add_log('Config, set question method start')
        if self.curr_game == 'multi':
            return Q()
        elif self.curr_game == 'frac':
            return QFrac(self.curr_var1, self.curr_var2)
        else:
            return None

    def is_high_score(self,CorrectRate):
        self.mylog.add_log('Config, is HScore method start')
        if self.curr_file == '':
            pass
        lead_list = utils.load_list_json(self.curr_file)
        lead_list.sort(key=itemgetter('CPM'))
        low_val = lead_list[0]['CPM']
        lead_list.sort(key=itemgetter('CPM'), reverse=True)
        self.lead_list = lead_list
        if CorrectRate > low_val:
            return 'Yes'
        else:
            return 'No'


class Perf(object):  #is reset when new game is started
    def __init__(self,mode):
        self.reset(mode)

    def reset(self,mode):
        self.mylog = log.logger('MLog.txt')
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
        self.mylog.add_log('Perform initialised')
    '''
    def start_stop(self,toggle, mode = None):
        if mode:#change to only set mode nothing else
            return True
        else:
            return False
    '''

    def get_lead_list(self):
        self.mylog.add_log('Perform get lead list starts')
        leadlist = utils.load_list_json(self.file)
        leadlist.sort(key=itemgetter('CPM'), reverse=True)
        self.lead_list = leadlist
        return self.lead_list

    def CheckForStop(self):
        self.mylog.add_log('Check for stop')
        if self.Driver == 'time':
            if t.time()>=self.TStop:
                self.StopNow = 'yes'
        else:
            if self.Asked >= self.QLimit:
                self.StopNow = 'yes'

    def RecalcRates(self):
        self.AnswerRate = round(self.Asked * 60 / (t.time() - self.Start),2)
        self.CorrectRate = round(self.Correct * 60 / (t.time() - self.Start),2)
        self.stats = "Answer rate Q/min = " + str(self.AnswerRate) +'\n'\
                    +"Correctly answered Q/min = {}".format(self.CorrectRate) +'\n'\
                    + "Scored {} out of {}".format(self.Correct,self.Asked)

    def updateScore(self,result):
        self.mylog.add_log('Update score')
        self.Asked += 1
        self.CheckForStop()
        if result == True:
            self.Correct +=1
        self.RecalcRates()

    def set_leader_board(self):
        self.mylog.add_log('set leader board')
        l = utils.get_score_file(self.Driver)
        self.file = l[0]
        #print('file is {}'.format(self.file))
        self.board_name = l[1]

    def is_high_score(self):
        self.mylog.add_log('Check for new high score')
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
