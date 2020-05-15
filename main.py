import os
import time
from queue import PriorityQueue

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class Node:
    def __init__(self,state,level,fval,prev, move, blanks):
        """ Initialize the node with the data, level of the node and the calculated fvalue """
        self.blanks = blanks
        self.prev = prev
        self.move = move
        self.data = state
        self.level = level
        self.fval = fval
    
    def __gt__(self, other): 
        if(self.fval>other.fval): 
            return True
        else: 
            return False
    
    def generate_child(self):
        """ Generate child nodes from the given node by moving the blank space
        either in the four directions {up,down,left,right} """
        

        possibleMovesCordinates = self.find(self.data,'-',self.blanks)
        move = ['right', 'left', 'down', 'up']
        children = []
        
        for i in range(4):
            for j in range(self.blanks):
                # print(possibleMovesCordinates[j:4*j+3])
                x,y = possibleMovesCordinates[j*4:j*4+4][0]
                x +=1 
                p, q = possibleMovesCordinates[j*4:j*4+4][i]
                child = self.swap(self.data,x,y,p,q)
                if child is not None:
                    child_node = Node(child,self.level+1,0,self,(self.data[p][q],move[i]),self.blanks)
                    children.append(child_node)
        return children

    def swap(self,puz,x1,y1,x2,y2):
        """ Move the blank space in the given direction and if the position value are out
        of limits the return None """
        if x2 >= 0 and x2 < len(self.data) and y2 >= 0 and y2 < len(self.data) and puz[x2][y2] != '-':
            temp_puz = []
            temp_puz = self.copy(puz)
            temp_puz[x2][y2],temp_puz[x1][y1] = temp_puz[x1][y1],temp_puz[x2][y2]
            return temp_puz
        else:
            return None

    def copy(self,root):
        """ Copy function to create a similar matrix of the given node"""
        temp = []
        for i in root:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp
        # return root[:]

    def find(self,puz,x,repeat):
        """ Specifically used to find the position of the blank space """
        val = []
        remain = repeat
        for i in range(0,len(self.data)):
            for j in range(0,len(self.data)):
                if puz[i][j] == x:
                    val += [(i-1,j),(i+1,j),(i,j-1),(i,j+1) ]
                    remain -= 1
                    if not remain:
                        break
        return val

class Puzzle:
    def __init__(self,h,blanks):
        """ Initialize the puzzle size by the specified size,open and closed lists to empty """
        # self.n = size
        self.nblanks = blanks
        self.heu = h
        self.open = []
        self.closed = []
        self.queue = PriorityQueue()
        self.tot_steps = 0

    def readInputs(self):
        start_config = []
        with open(os.path.join(ROOT_DIR, 'Start_Configuration.txt')) as file:
            for line in file:
                start_config.append(line.strip().split('\t'))
        self.n = len(start_config)
        goal_config = []
        with open(os.path.join(ROOT_DIR, 'Goal_Configuration.txt')) as file:
            for line in file:
                goal_config.append(line.strip().split('\t'))
        return start_config, goal_config

    def find(self,puz,x):
        """ Specifically used to find the position of the blank space """
        for i in range(0,len(puz)):
            for j in range(0,len(puz)):
                if puz[i][j] == x:
                    return (i,j)

    def f(self,start,goal,h):
        """ Heuristic Function to calculate hueristic value f(x) = h(x) + g(x) """
        if h == 'diff':
            return self.h_diff(start.data,goal)+start.level
        elif h == 'man':
            return self.h_man(start.data,goal)+start.level

    def h_man(self,start,goal):
        """ Calculates the manhattan distance between the given puzzle tiles  """
        temp = 0
        for i in range(0,self.n):
            for j in range(0,self.n):
                if start[i][j] != '-':
                    x,y = self.find(goal, start[i][j])
                    temp += abs(x-i) + abs(y - j)
        return temp
    
    def h_diff(self,start,goal):
        """ Calculates the different between the given puzzles """
        temp = 0
        for i in range(0,self.n):
            for j in range(0,self.n):
                if start[i][j] != goal[i][j] and start[i][j] != '-':
                    temp += 1
        return temp
    
    def writeLog(self,move):
        with open(os.path.join(ROOT_DIR, 'Output.txt'),'w+') as file:
            file.write('{}\n'.format(move))

    def to_pq_entry(self, data):
        """
            returns the tuple (priority, count, board)
        """
        val = int(data.fval)
        return (val, data)

    def travers(self,start=None, goal=None):
        if start == None or goal == None:
            start, goal = self.readInputs()

        start = Node(start,0,0,None,(),self.nblanks)
        start.fval = self.f(start,goal, self.heu)
        self.open.append(start)
        self.queue.put(self.to_pq_entry(start))
        while not self.queue.empty():
            cur = self.queue.get()[1]
            heu = self.h_diff(cur.data,goal) if self.heu == 'diff' else self.h_man(cur.data,goal)
            self.tot_steps += 1
            if(heu == 0):
                self.final_state = cur
                break
            children = cur.generate_child()
            for i in children:
                i.fval = self.f(i,goal, self.heu)
                self.open.append(i)
                self.queue.put(self.to_pq_entry(i))
            self.closed.append(cur)
            
        # print('Finished')
    def printPuzzle(self,data):
        l = len(data)
        for row in data:
            formatted_row = ('%s\t'*l)%tuple(row)
            # print('-'*25)
            print(formatted_row)
        print('-'*7*self.n)
        # print()

    def traceback(self,w=True,p=True):
        state = self.final_state
        state_list = [state]
        while True:
            prev_state = state.prev
            if prev_state == None:
                break
            state_list.append(prev_state)
            state = prev_state
        
        state_list = state_list[::-1]
        moves = []
        for state in state_list:
            moves.append(state.move)
            if p:
                self.printPuzzle(state.data)
        self.moves = moves
        print(','.join(map(str, moves[1:])))
        if w:
            self.writeLog(','.join(map(str, moves[1:])))

if __name__  == '__main__':

    strat = "man" #input('Manhattan distance or tile difference?(man or diff): ')
    blanks = 4
    t1 = time.time()
    puz = Puzzle(strat,blanks)
    puz.travers()
    puz.traceback()
    t2 = time.time()
    print('Time taken is {} seconds'.format(t2-t1))
# input('Press any key to exit')