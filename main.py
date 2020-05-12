import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

start_config = []
with open(os.path.join(ROOT_DIR, 'Start_Configuration.txt')) as file:
    for line in file:
        start_config.append(line.strip().split('\t'))
goal_config = []
with open(os.path.join(ROOT_DIR, 'Goal_Configuration.txt')) as file:
    for line in file:
        goal_config.appned(line.strip().split('\t'))

