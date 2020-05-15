import random
import numpy as np
import time
import copy
from scipy.stats import t

from main import Node, Puzzle

start = []
goal = []

man_times = []
diff_times = []
man_steps = []
diff_steps = []

def makeRandomPuzzle(size):
    puzzle = np.full((size, size), '-', dtype=object)

    items = list(range(1, size**2 + 1))
    mixedItems = items[:]
    random.shuffle(mixedItems)

    for i in items[:-2]:
        val = i
        x = (mixedItems[i-1] -1)//size 
        y = mixedItems[i-1]-1-x*size
        # print(x,y)
    # for i in mixedItems[2:]:
    #     val = items[i-1]
    #     x = (i -1)//size
    #     y = i-1-x*size
        puzzle[x][y] = str(val)
    # print(puzzle)
    return puzzle.tolist()

def find(puz):
        for i in range(0,len(puz)):
            for j in range(0,len(puz)):
                if puz[i][j] == '-':
                    return (i,j)

def shufflePuzzle(puzzle,iterations):
    n = len(puzzle)
    tmp = copy.deepcopy(puzzle)
    for i in range(iterations):
        x,y = find(tmp)
        # print(x,y)
        possibeleMoves = [(x-1,y),(x,y-1),(x+1,y),(x,y+1)]
        while True:
            p,q = random.choice(possibeleMoves)
            if (0 <= p <n and 0 <= q < n):
                break
        tmp[p][q], tmp[x][y] = tmp[x][y], tmp[p][q]
    return tmp

def main():
    for i in range(100):
        size = random.randint(4,20)
        if size>15:
            shuff = random.randint(10,13)
        else:
            shuff = random.randint(12,15)
        start = makeRandomPuzzle(size)
        goal = shufflePuzzle(start, shuff)

        # print(start)
        # print(goal)
        t1 = time.time()
        puz = Puzzle('diff')
        puz.n = len(start)
        puz.travers(start,goal)
        puz.traceback(w=False)
        travers_steps = len(puz.moves)
        tot_steps = puz.tot_steps
        t2 = time.time()
        diff_times.append(t2 - t1)
        diff_steps.append(tot_steps)
        # print('Displacement steps {}'.format(tot_steps))
        # print('Time taken to solve using misplce heuristics: {} seconds'.format(t2 - t1))

        t1 = time.time()
        puz = Puzzle('man')
        puz.n = len(start)
        puz.travers(start,goal)
        puz.traceback(w=False)
        travers_steps = len(puz.moves)
        tot_steps = puz.tot_steps
        t2 = time.time()
        man_times.append(t2 - t1)
        man_steps.append(tot_steps)
        # print('Manhattan steps {}'.format(tot_steps))
        # print('Time taken to solve using manhattan distance heuristics: {} seconds'.format(t2 - t1))

        
    # print(man_times)
    # print(diff_times)

    mean_man_time = mean(man_times)
    mean_man_steps = mean(man_steps)
    mean_diff_time = mean(diff_times)
    mean_diff_steps = mean(diff_steps)
    std_man_time  = stddev(man_times)
    std_man_steps = stddev(man_steps)
    std_diff_time = stddev(diff_times)
    std_diff_steps = stddev(diff_steps)
    n = len(man_steps)
    alpha = 0.05
    t_stat, df, cv, p = pairedTTest(diff_steps, man_steps,alpha)
    
    print("Mean of manhatton Algorithm(Time) " , mean_man_time)
    print("S.D of manhatton Algorithm(Time) " , std_man_time)
    print("Mean of manhatton Algorithm(Steps) " , mean_man_steps)
    print("S.D of manhatton Algorithm(Steps) " , std_man_steps )
    
    print("---------------------------------------")
    print("Mean of misplaced Algorithm(Time) " , mean_diff_time)
    print("S.D of misplaced Algorithm(Time) " , std_diff_time)
    print("Mean of misplaced Algorithm(Steps) " , mean_diff_steps)
    print("S.D of misplaced Algorithm(Steps) " , std_diff_steps)

    print('P value: {}'.format(p))
    if p > alpha:
        print('Thre is no significant diffeerence between two algorithms')
    else:
        print('Thre is a significant diffeerence between two algorithms')

def mean(data):
    """Return the sample arithmetic mean of data."""
    n = len(data)
    if n < 1:
        raise ValueError('mean requires at least one data point')
    return sum(data)/n # in Python 2 use sum(data)/float(n)

def _ss(data):
    """Return sum of square deviations of sequence data."""
    c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss

def stddev(data, ddof=0):
    """Calculates the population standard deviation
    by default; specify ddof=1 to compute the sample
    standard deviation."""
    n = len(data)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    ss = _ss(data)
    pvar = ss/(n-ddof)
    return pvar**0.5

def sumSqrdDiff(data1, data2):
    n = len(data1)
    return sum([(data1[i] - data2[i])**2 for i in range(n)])


def sumDiff(data1, data2):
    n = len(data1)
    return sum([(data1[i] - data2[i]) for i in range(n)])

def stdDev(data1, data2):
    n = len(data1)
    d1 = sumSqrdDiff(data1, data2)
    d2 = sumDiff(data1, data2)
    return ((d1 - (d2**2 / n))/(n-1))**(0.5)

def stdError(data1, data2):
    n = len(data1)
    stddv = stdDev(data1, data2)
    return stddv/(n**0.5)


def pairedTTest(data1, data2, alpha=0.05):
    n = len(data1)
    mean1, mean2 = mean(data1), mean(data2)
    sed = stdError(data1, data2)
    t_stat = (mean1 - mean2) / sed
    df = n -1
    criticalVal = t.ppf(1.0 - alpha, df)
    p = (1.0 - t.cdf(abs(t_stat), df)) *2.0
    return t_stat, df, criticalVal, p

# a = makeRandomPuzzle(4)
# b = a[:]
# print(a)
# b = shufflePuzzle(a, 10)

# print(a)
# print(b)

main()

# print(len(start))
# print(len(goal))
# print(len(goal[4]))
# print(len(start[4]))
# print(makeRandomPuzzle(4))

