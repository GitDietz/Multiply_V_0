import random as Rd


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


