
class Robot():
    def __init__(self, pos, vel, N, M):
        self.x = pos[0]
        self.y = pos[1]
        self.vel_x = vel[0]
        self.vel_y = vel[1]
        self.N = N
        self.M = M

    def move(self, t):
        self.x = (self.x + self.vel_x * t) % self.N
        self.y = (self.y + self.vel_y * t) % self.M

    def get_pos(self):
        return self.x, self.y

class RobotGrid():
    def __init__(self, N, M):
        self.robots = []
        self.N = N
        self.M = M
    def add_robot(self,pos,vel):
        self.robots.append(Robot(pos,vel,self.N,self.M))
    
    def iterate_over_time(self,t):
        for robot in self.robots:
            robot.move(t)

    def safety_score(self):
        scores = [[0,0],[0,0]]
        N_mid = self.N//2 
        M_mid = self.M//2 
        for robot in self.robots:
            x,y = robot.get_pos()
            if x != N_mid and y != M_mid:
                scores[(x > N_mid) * 1][(y > M_mid) * 1] += 1
        return scores
    
    def get_grid(self):
        grid = [[0 for ii in range(self.N)] for jj in range(self.M)]
        for robot in self.robots:
            x,y = robot.get_pos()
            grid[y][x] += 1

        output_str = ''
        for ii in range(self.N):
            for jj in range(self.M):
                if grid[jj][ii] > 0:
                    output_str += 'O'
                else:
                    output_str += '.'
            output_str += '\n'
        return output_str
