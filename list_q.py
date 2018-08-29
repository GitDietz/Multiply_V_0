import csv

def get_q_from_file():
    #change this to used path setting as per multiply
    with open('questions.csv') as csvfile:
        readQs = csv.reader(csvfile,delimiter=',')
        Q_and_A = []
        for Q in readQs:
            Q_and_A.append({'Q':Q[0],'A':Q[1]})
            print(Q[0])
            print('boo')


if __name__ == '__main__':
    get_q_from_file()


