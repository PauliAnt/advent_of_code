from colorama import Fore # For rendering the image
class Intersect():
    def __init__(self, pos, prev, score):
        self.pos = pos
        self.score = score
        self.prev = [prev]
    
    def update_score(self,score, prev):
        self.score = score
        self.prev = [prev]

    def add_prev(self,prev):
        self.prev.append(prev)

    
class Maze():
    def __init__(self,grid, start_pos, target):
        self.directions = ((0,1), (-1,0), (0,-1), (1,0))

        start_node = Intersect(start_pos, None, -1)
        self.queue = [start_node]
        self.running_id = 1
        self.visited = {start_pos:start_node}
        self.grid = grid
        self.grid_shape = len(grid),len(grid[0])
        self.target = target
        self.target_score = 100000
        self.target_node = None


    def is_intersection(self,pos,direction_ind):
        direction_inds = ((direction_ind + 1) % 4, (direction_ind + 3) % 4)
        for direction_ind in direction_inds:
            new_pos = (pos[0] + self.directions[direction_ind][0], pos[1] + self.directions[direction_ind][1])
            if self.grid[new_pos[0]][new_pos[1]] == 0:
                return True
        return False
    
    def add_to_que(self, pos, prev_pos, s):
        if pos not in self.visited:
            intersect = Intersect(pos,prev_pos,s + 1000)
            self.queue.append(intersect)
            self.visited[pos] = intersect

        else:
            if s+1000 < self.visited[pos].score:
                self.visited[pos].update_score(s + 1000, prev_pos)
            elif s+1000 == self.visited[pos].score and prev_pos not in self.visited[pos].prev:
                self.visited[pos].add_prev(prev_pos)


    def print_paths(self):
        print(f'Paths in que {len(self.queue)}:')
        for path in self.queue:
            print(path.pos, path.score)
        print('-'*10)


    def render_grid(self, filename = None):
        print('Currently explored:')
        s = ''
        for ii in range(self.grid_shape[0]):
            for jj in range(self.grid_shape[1]):
                if self.grid[ii][jj] == 1:
                    s += Fore.WHITE + '▓▓'
                elif self.on_path[ii][jj] == 1:
                    s += Fore.GREEN + '▓▓'
                elif (ii,jj) in self.visited:
                    s += Fore.RED + '▓▓'
                else:
                    s += '  '
            s += '\n'
        print(s)
        if filename:
            with open(filename,'w') as file:
                file.write(s)

    
    def find_shortest_path(self):
        while len(self.queue) > 0:
            self.queue = sorted(self.queue, key=lambda intersect: intersect.score)
            intersect = self.queue.pop(0)
            pos = intersect.pos
            if intersect.score > self.target_score + 1000:
                break

            for ii in range(4):
                
                direction = self.directions[ii]
                next_pos = (pos[0] + direction[0], pos[1] + direction[1])
                s = intersect.score
                
                while self.grid[next_pos[0]][next_pos[1]] == 0:
                    s += 1
                    if next_pos == self.target:
                        if self.target_node == None:
                            self.add_to_que(next_pos, pos, s)
                            self.target_node = self.visited[next_pos]
                            self.target_score = s
                        

                    # Check intersections
                    if self.is_intersection(next_pos,ii):
                        self.add_to_que(next_pos, pos, s)
                    next_pos = (next_pos[0] + direction[0], next_pos[1] + direction[1])
        return s

    def backtrack(self):
        self.queue = [self.target_node]
        self.backtracked = set()
        self.on_path = [[0 for ii in range(self.grid_shape[1])] for jj in range(self.grid_shape[0])] 
        while len(self.queue):
            intersect = self.queue.pop(0)
            if intersect.pos in self.backtracked:
                continue
            elif intersect.prev == [None]:
                break

            
            self.backtracked.add(intersect.pos)
            for prev_pos in intersect.prev:
                if prev_pos[0] == intersect.pos[0]:
                    x_pos = sorted([prev_pos[1],intersect.pos[1]])
                    for jj in range(x_pos[0],x_pos[1]+1):
                        self.on_path[intersect.pos[0]][jj] = 1
                if prev_pos[1] == intersect.pos[1]:
                    y_pos = sorted([prev_pos[0],intersect.pos[0]])
                    for ii in range(y_pos[0],y_pos[1]+1):
                        self.on_path[ii][intersect.pos[1]] = 1
                self.queue.append(self.visited[prev_pos])
        
        return sum([sum(row) for row in self.on_path])-1

