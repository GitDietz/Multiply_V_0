from operator import itemgetter
import json,datetime as d

now = d.datetime.now()



def __main__():
    '''

    l= [{'key':'R', 'item1':'Zoo', 'item2':2},
                {'key':'Z', 'item1':'Donk', 'item2':7.2},
                {'key':'A', 'item1':'Swea', 'item2':5.0},
                {'key':'B', 'item1':'Kiml', 'item2':6.4}]
    :return:
    Now - when there are less than 10 in list - must add and not remove

    '''

    with open('leaders.json') as json_data:
        l = json.load(json_data)
    print(l)
    print('time now ' + str(now))
    l.sort(key=itemgetter('CPM'))
    print(l)
    lowest = l[0]
    low_val = l[0]['CPM']
    print('direct lowedt {}'.format(low_val))
    print('first item is ' + str(lowest['CPM']))
    l.pop(0)
    print(l)
    l.append({'name':'P', 'date':str(now), 'CPM':7.4})
    print(l)
    print('the list is now containing {}'.format(len(l)))

    with open('leaders.json', 'w') as fp:
        json.dump(l, fp)


if __name__== '__main__':
    __main__()
