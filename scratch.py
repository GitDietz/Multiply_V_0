def set_q(game_mode):
    print('game is '+game_mode)
    #the format is frac_set, frac_time
    qset = game_mode.split("_")
    if qset[0] == 'frac':
        q=QFrac()
    elif qset[0] == 'multi':
        q=Q()


#set_q('fraction_mat')

def isFloat(str):
    try:
        result = float(str)
        return True
    except:
        return False

print('the value 2.33 is a float ? {}',format(isFloat('2.555')))
