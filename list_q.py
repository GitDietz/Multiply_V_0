import csv

def get_q_from_file():
    #change this to used path setting as per multiply
    with open('questions.csv') as csvfile:
        readQs = csv.reader(csvfile,delimiter=',')
        for Q in readQs:
            Q_and_A.append({'Q':Q[0][1:-1],'c1':Q[1][1:-1],'c2':Q[2][1:-1],'c3':Q[3][1:-1],'c4':Q[4][1:-1],'r':Q[5]})
        print(Q_and_A)
        print('boo')

def present_q():
    for q in Q_and_A:
        print('Question: ',format(q['Q']))
        print('Option 1 :', format(q['c1']))
        print('Option 2 :', format(q['c2']))
        print('Option 3 :', format(q['c3']))
        print('Option 4 :', format(q['c4']))
        proper_response = False
        while not proper_response:
            response = input('Which one is correct? Enter 1,2,3 or 4')
            if response.isnumeric():
                proper_response = True
                if int(response) == int(q['r']):
                    print('Well done!')
                else:
                    print('Oops, not that one')
            else:
                print('Only input 1,2,3,4')


if __name__ == '__main__':
    Q_and_A = []
    get_q_from_file()
    present_q()


