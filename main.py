import os
import time
from queue import PriorityQueue

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class Node:
    def __init__(self,state,level,fval,prev, move):
        """ Initialize the node with the data, level of the node and the calculated fvalue """
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
        
        x1,y1,x2,y2 = self.find(self.data,'-',2)
        val_list1 = [[x1,y1-1],[x1,y1+1],[x1-1,y1],[x1+1,y1]]
        val_list2 = [[x2,y2-1],[x2,y2+1],[x2-1,y2],[x2+1,y2]]
        move = ['right', 'left', 'down', 'up']
        children = []
        for i in range(4):
            p, q = val_list1[i]
            child = self.swap(self.data,x1,y1,p,q)
            if child is not None:
                child_node = Node(child,self.level+1,0,self,(self.data[p][q],move[i]))
                children.append(child_node)
            p, q = val_list2[i]
            child = self.swap(self.data,x2,y2,p,q)
            if child is not None:
                child_node = Node(child,self.level+1,0,self,(self.data[p][q],move[i]))
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
                    val += [i,j]
                    remain -= 1
                    if not remain:
                        break
        return val

class Puzzle:
    def __init__(self,h):
        """ Initialize the puzzle size by the specified size,open and closed lists to empty """
        # self.n = size
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

        start = Node(start,0,0,None,())
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
            print(formatted_row)
        print()

    def traceback(self,w=True):
        state = self.final_state
        # prev_state = state.prev
        state_list = [state]
        while True:
            prev_state = state.prev
            # prev_state = prev_state.prev
            if prev_state == None:
                break
            state_list.append(prev_state)
            state = prev_state
        
        state_list = state_list[::-1]
        moves = []
        for state in state_list:
            moves.append(state.move)
        self.moves = moves
            # self.printPuzzle(state.data)
        # self.printPuzzle(state.data)
        # print(','.join(map(str, moves[1:])))
        if w:
            self.writeLog(','.join(map(str, moves[1:])))

if __name__  == '__main__':

#     puz = Puzzle('man')
#     puz.travers()
#     puz.traceback()

    strat = input('Manhattan distance or tile difference?(man or diff): ')
    t1 = time.time()
    puz = Puzzle(strat)
    puz.travers()
    puz.traceback()
    t2 = time.time()
    print('Time taken is {} seconds'.format(t2-t1))
# input('Press any key to exit')