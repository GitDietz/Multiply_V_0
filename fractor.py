import random as Rd, json

class QFrac(object):
    '''
    Fraction question object
    '''
    def __init__(self,no_of,same_denom):
        self.reset(no_of,same_denom)

    def reset(self,no_of,same_denom):
        top = 12
        self.components = []
        self.q = 'What is '
        numer = Rd.randint(2, top)
        self.components.append(numer)
        denominator = Rd.randint(2, top)
        self.components.append(denominator)

        self.q += str(numer) + '/' + str(denominator) + ' '
        self.result = numer/denominator
        for i in range(1,no_of):
            numer = Rd.randint(1, top)
            self.components.append(numer)
            if not same_denom:
                denominator = Rd.randint(2, top)
            self.components.append(denominator)
            self.q += ' + ' + str(numer) + '/' + str(denominator) +' '
            self.result += numer/denominator
        self.invalid = True  # this means a non number value was given
        self.answer = False  # use to store the result
        print(self.components)
        jval = json.dumps(self.components)
        print(jval)

def prep_answer():
    #return Correct or not
    myval = input('What is your answer?')
    #no / contained not all values
    if myval.find('/')==-1:
        return 'Format needs to be 2 numbers separated with the / e.g. 3 / 4'
    else:
        parts = myval.split('/')
        print(parts)
        if parts[0].isnumeric() and parts[1].isnumeric():
            result = True
            return ('Resulting in {}'.format(str(int(parts[0]) / int(parts[1]))))
        else:
            return 'Both parts must be numbers'

def __main__():
    question = QFrac(4,True)
    result = False
    print(question.q)
    while result == False:
        print('The result will be {}'.format(question.result))
        print(prep_answer())



if __name__ == '__main__':
    __main__()

