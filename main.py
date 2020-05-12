import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# start_config = []
# with open(os.path.join(ROOT_DIR, 'Start_Configuration.txt')) as file:
#     for line in file:
#         start_config.append(line.strip().split('\t'))
# goal_config = []
# with open(os.path.join(ROOT_DIR, 'Goal_Configuration.txt')) as file:
#     for line in file:
#         goal_config.appned(line.strip().split('\t'))

class Node:
    def __init__(self,state,level,fval):
        """ Initialize the node with the data, level of the node and the calculated fvalue """
        self.data = state
        self.level = level
        self.fval = fval
    
    def generate_child(self):
        """ Generate child nodes from the given node by moving the blank space
        either in the four directions {up,down,left,right} """
        x1,y1,x2,y2 = self.find(self.data,'-',2)
        """ val_list contains position values for moving the blank space in either of
        the 4 directions [up,down,left,right] respectively. """
        val_list1 = [[x1,y1-1],[x1,y1+1],[x1-1,y1],[x1+1,y1]]
        val_list2 = [[x2,y2-1],[x2,y2+1],[x2-1,y2],[x2+1,y2]]
        children = []
        for i in val_list1:
            child = self.swap(self.data,x1,y1,i[0],i[1])
            if child is not None:
                child_node = Node(child,self.level+1,0)
                children.append(child_node)
        for i in val_list2:
            child = self.swap(self.data,x2,y2,i[0],i[1])
            if child is not None:
                child_node = Node(child,self.level+1,0)
                children.append(child_node)
        return children

    def swap(self,puz,x1,y1,x2,y2):
        """ Move the blank space in the given direction and if the position value are out
        of limits the return None """
        if x2 >= 0 and x2 < len(self.data) and y2 >= 0 and y2 < len(self.data):
            temp_puz = []
            temp_puz = self.copy(puz)
            # temp = temp_puz[x2][y2]
            temp_puz[x2][y2],temp_puz[x1][y1] = temp_puz[x1][y1],temp_puz[x2][y2]
            # temp_puz[x1][y1] = temp
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
        
    def accept(self):
        """ Accepts the puzzle from the user """
        puz = []
        for i in range(0,self.n):
            temp = input().split(" ")
            puz.append(temp)
        return puz

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
        val = []
        for i in range(0,len(puz)):
            for j in range(0,len(puz)):
                if puz[i][j] == x:
                    return i,j

    def f(self,start,goal,h):
        """ Heuristic Function to calculate hueristic value f(x) = h(x) + g(x) """
        if h == 'diff':
            return self.h_diff(start.data,goal)+start.level
        elif h == 'man':
            return self.h_man(start.data,goal)+start.level

    def h_diff(self,start,goal):
        """ Calculates the different between the given puzzles """
        temp = 0
        for i in range(0,self.n):
            for j in range(0,self.n):
                if start[i][j] != '-':
                    x,y = self.find(goal, start[i][j])
                    temp += abs(x-i) + abs(y - j)
        return temp
    
    def h_man(self,start,goal):
        """ Calculates the different between the given puzzles """
        temp = 0
        for i in range(0,self.n):
            for j in range(0,self.n):
                if start[i][j] != goal[i][j] and start[i][j] != '-':
                    temp += 1
        return temp
        

    def process(self):
        """ Accept Start and Goal Puzzle state"""
        # print("Enter the start state matrix \n")
        # start = self.accept()
        # print("Enter the goal state matrix \n")        
        # goal = self.accept()
        start, goal = self.readInputs()

        start = Node(start,0,0)
        start.fval = self.f(start,goal, self.heu)
        """ Put the start node in the open list"""
        self.open.append(start)
        # print("\n\n")
        while True:
            cur = self.open[0]
            # print("")
            print("  | ")
            print("  | ")
            print(" \\\'/ \n")
            for i in cur.data:
                for j in i:
                    print(j,end=" ")
                print("")
            """ If the difference between current and goal node is 0 we have reached the goal node"""
            heu = self.h_diff(cur.data,goal) if self.heu == 'diff' else self.h_man(cur.data,goal)
            # print(heu)
            if(heu == 0):
                break
            for i in cur.generate_child():
                i.fval = self.f(i,goal, self.heu)
                self.open.append(i)
            self.closed.append(cur)
            del self.open[0]
            """ sort the opne list based on f value """
            self.open.sort(key = lambda x:x.fval,reverse=False)
        print('Finished')

puz = Puzzle('man')
puz.process()