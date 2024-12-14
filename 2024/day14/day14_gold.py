# Gold
# Based on visual analysis pattern repeats every 101 iterations after 28
from RobotGrid import RobotGrid
import os
import time

with open('input.txt') as file:
    data = file.read()

data = data.split('\n')


grid = RobotGrid(101,103)
for row in data:
    pos = tuple([int(num) for num in row.split(' ')[0].split('=')[1].split(',')])
    vel = tuple([int(num) for num in row.split(' ')[1].split('=')[1].split(',')])
    grid.add_robot(pos,vel)

n = 0
max_iter = 10000
grid.iterate_over_time(28)
while n < max_iter:
    
    print(grid.get_grid())
    print(f'Iteration {n}')
    input()
    # time.sleep(0.1)
    grid.iterate_over_time(101)
    n += 101

    os.system('cls')
    


