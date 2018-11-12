import json,datetime as d,os
import logger as log
from operator import itemgetter

now = d.datetime.now()

def full_name(fname):
    the_folder = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(the_folder, 'static/files/',fname)

def load_list_json(file_name):
    with open(full_name(file_name)) as json_data:
        return json.load(json_data)


def write_json_file(file_name,package):
    with open(full_name(file_name), 'w') as fp:
        json.dump(package, fp)
    return

def add_high_score(file_name,name,score,no_scores):
    l = load_list_json(full_name(file_name))
    if len(l) >= no_scores:
        l.sort(key=itemgetter('CPM'))
        l.pop(0)
    l.append({'name': name, 'date': str(now), 'CPM': score})
    l.sort(key=itemgetter('CPM'), reverse=True)
    write_json_file(file_name,l)
    return l

def get_score_file(game_name):
    file_list = load_list_json(full_name('config.json'))
    name_l = []
    for f in file_list:
        print(f['game'] + ' file of ' +f['file'])
        if f['game']==game_name:
            name_l.append(f['file'])
            name_l.append(f['boardname'])
            return name_l
    raise LookupError('No game with the name {} found in file',format(game_name))

def get_config():
    return load_list_json(full_name('config.json'))

def get_low_score(file_name):
    lead_list = load_list_json(file_name)
    lead_list.sort(key=itemgetter('CPM'))
    low_val = lead_list[0]['CPM']
    lead_list = lead_list.sort(key=itemgetter('CPM'), reverse=True)
    if self.CorrectRate > low_val:
        self.hi_score = 'Yes'
    return self.hi_score

def isFloat(str):
    try:
        result = float(str)
        return True
    except:
        return False