import json,datetime as d
from operator import itemgetter

now = d.datetime.now()

def load_list_json(file_name):
    with open(file_name) as json_data:
        return json.load(json_data)


def write_json_file(file_name,package):
    with open(file_name, 'w') as fp:
        json.dump(package, fp)
    return

def add_high_score(file_name,name,score,no_scores):
    #already established the score is higher than the lowest in the table
    l = load_list_json(file_name)
    if len(l) >= no_scores:
        l.sort(key=itemgetter('CPM'))
        lowest = l[0]
        low_val = l[0]['CPM']
        #print('direct lowest {}'.format(low_val))
        #print('first item is ' + str(lowest['CPM']))
        l.pop(0)
        #print(l)
    l.append({'name': name, 'date': str(now), 'CPM': score})
    #print(l)
    write_json_file(file_name,l)
    return l