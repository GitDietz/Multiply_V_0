import random as Rd, json

class QFrac(object):
    '''
    Fraction question object
    '''
    def __init__(self,no_of,same_denom):
        self.reset(no_of,same_denom)

    def reset(self,no_of,same_denom):
        top = 12
        self.tolerance = 0.000000001
        self.components = []
        self.q = 'What is '
        numer = Rd.randint(2, top)
        self.components.append(numer)
        denominator = Rd.randint(2, top)
        self.components.append(denominator)

        self.q += str(numer) + '/' + str(denominator) + ' '
        self.correct_result = numer/denominator
        for i in range(1,no_of):
            numer = Rd.randint(1, top)
            self.components.append(numer)
            if not same_denom:
                denominator = Rd.randint(2, top)
            self.components.append(denominator)
            self.q += ' + ' + str(numer) + '/' + str(denominator) +' '
            self.correct_result += numer/denominator
        self.invalid = True  # this means a non number value was given
        self.r = False  # use to store the result

        #print(self.components)
        #jval = json.dumps(self.components)
        #print(jval)

    def result(self, myval):
        #return Correct or not
        #no / contained not all values
        self.r = False
        if myval.isnumeric():
            if abs(float(myval) - self.correct_result) <= self.tolerance:
                return 'Well Done!'

        if myval.find('/')==-1:
            comment = 'Format needs to be 2 numbers separated with the / e.g. 3 / 4'
        else:
            parts = myval.split('/')
            #print(parts)
            if parts[0].isnumeric() and parts[1].isnumeric():
                if abs((int(parts[0]) / int(parts[1])) - self.correct_result) <= self.tolerance:
                    #print('Resulting in {}'.format(str(int(parts[0]) / int(parts[1]))))
                    comment = 'Well Done!'
                    self.r = True
                else:
                    comment = 'Not quite'
            else:
                comment = 'Both parts must be numbers'
        return comment

def __main__():
    question = QFrac(4,True)
    print(question.q)

    while question.r == False:
        response = input('What is your answer?')
        print(question.result(response))




if __name__ == '__main__':
    __main__()

