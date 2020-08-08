def solve_mine(map, n):
    # coding and coding...
    mine = [i.split(' ') for i in map.split('\n')]
    field = MineSweeper (mine)
    print(field)
    #compare last stat_map with new stat_map
    for i in range(7):
        print("Iteration: ", i)
        st1 = field.ret_stat_map()
        field.maybe_solve()
        st2 = field.ret_stat_map()
        if st1 == st2:
            print('we stuck')
        print(field)
    return 0

class MineSweeper():
    def __init__(self, map):
        self.map = map
        self.rows = len(map)
        self.columns = len(map[0])
        self.stat_map = [[ self.check_neighbors(self.map, i, j) for j in range(self.columns)]for i in range(self.rows)]
    
    def __str__(self):
        map_str = '\n'.join([ (' '.join([str(elem) for elem in row])) for row in self.map])
        stat_map_str = '\n'.join([ (' '.join([str(elem) for elem in row])) for row in self.stat_map])
        return 'Map:\n' + map_str + '\n\nStat map:\n'+ stat_map_str + '\n'

    def ret_stat_map(self):
        stat_map_str = '\n'.join([ (' '.join([str(elem) for elem in row])) for row in self.stat_map])
        return stat_map_str


    @staticmethod
    def check_neighbors(map, n, m):
        flag = -1
        blocks = 0
        blocked = 0
        numbers = 0
        bombs = 0
        for i in range(n-1, n+2):
            for j in range(m-1, m+2):
                if i == n and j == m:
                    if map[i][j] == '?':
                        flag = 1
                    elif map[i][j] == 'x':
                        flag = 2
                    else:
                        flag = 3
                elif i < 0 or j < 0:
                    continue
                else:
                    try:
                        blocks += 1
                        if map[i][j] == '?':
                            blocked += 1
                        elif map[i][j] == 'x':
                            bombs += 1
                        else:
                            numbers += 1
                    except IndexError:
                        continue
        # b - blocked
        # h - have neighbours
        # n - number
        # u - used
        # x - bomb
        if flag == 1:
            if numbers > 0:
                return 'h'
            else:
                return 'b'
        elif flag == 2:
            return 'x'
        else:
            if numbers == blocks:
                return 'u'
            elif blocked == 0:
                return 'u'
            else:
                return 'n'
    @staticmethod
    def h(stat_map, n, m):
        near_h = []
        for i in range(n-1, n+2):
            for j in range(m-1, m+2):
                if i == n and j == m:
                    continue
                elif i < 0 or j < 0:
                    continue
                else:
                    try:
                        if stat_map[i][j] == 'h':
                            near_h.append((i,j))
                    except IndexError:
                        continue
        return near_h
    
    @staticmethod
    def x(stat_map, n, m):
        near_h = []
        count_x = 0
        count_h = 0
        for i in range(n-1, n+2):
            for j in range(m-1, m+2):
                if i == n and j == m:
                    continue
                elif i < 0 or j < 0:
                    continue
                else:
                    try:
                        if stat_map[i][j] == 'h':
                            count_h += 1
                            near_h.append((i,j))
                        elif stat_map[i][j] == 'x':
                            count_x +=1
                    except IndexError:
                        continue
        return count_x, count_h, near_h
                    
    def maybe_solve(self):
        #find n
        for i in range(self.rows):
            for j in range(self.columns):
                #biiiiiiig check
                if self.stat_map[i][j] == 'n':
                    if self.map[i][j] == '0':
                        near = self.h(self.stat_map, i, j)
                        for row, column in near:
                            self.map[row][column] = open(row,column)
                            #self.stat_map[row][column] = 'n'
                        #self.stat_map[i][j] == 'u'
                    else:
                        c_x, c_h, near = self.x(self.stat_map, i, j)
                        if c_x + c_h == int(self.map[i][j]):
                            for row, column in near:
                                self.map[row][column] = 'x'
                        elif c_x == int(self.map[i][j]):
                            for row, column in near:
                                self.map[row][column] = open(row,column)
                self.stat_map = [[ self.check_neighbors(self.map, i, j) for j in range(self.columns)]for i in range(self.rows)]
        return 0


gamemap = """
? ? 0 ? ? ? 0 0 ? ? ? 0 0 0 0 ? ? ? 0
? ? 0 ? ? ? 0 0 ? ? ? 0 0 0 0 ? ? ? ?
? ? 0 ? ? ? ? ? ? ? ? 0 0 0 0 ? ? ? ?
0 ? ? ? ? ? ? ? ? ? ? 0 0 0 0 0 ? ? ?
0 ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 0 0
0 ? ? ? 0 0 0 ? ? ? 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 ? ? ? ? ? ? ? 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 ? ? ? ? 0 0 0 0 0
0 0 ? ? ? 0 ? ? ? 0 ? ? ? ? 0 0 0 0 0
0 0 ? ? ? ? ? ? ? 0 0 0 0 0 0 ? ? ? 0
0 0 ? ? ? ? ? ? ? ? ? 0 0 0 0 ? ? ? 0
0 0 0 0 ? ? ? ? ? ? ? 0 0 0 0 ? ? ? 0
0 0 0 0 0 ? ? ? ? ? ? 0 0 0 0 0 ? ? ?
0 0 ? ? ? ? ? ? 0 0 0 0 0 0 0 0 ? ? ?
0 0 ? ? ? ? ? ? ? 0 0 0 0 0 0 0 ? ? ?
0 0 ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 ? ?
0 0 0 0 0 0 ? ? ? ? 0 0 0 ? ? ? 0 ? ?
0 0 0 ? ? ? ? ? ? ? 0 0 0 ? ? ? ? ? ?
0 0 0 ? ? ? ? ? 0 0 0 ? ? ? ? ? ? ? ?
0 0 0 ? ? ? ? ? 0 0 0 ? ? ? 0 ? ? ? ?
0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
""".strip()
result = """
1 1 0 1 1 1 0 0 1 1 1 0 0 0 0 1 1 1 0
x 1 0 1 x 1 0 0 2 x 2 0 0 0 0 1 x 2 1
1 1 0 2 3 3 1 1 3 x 2 0 0 0 0 1 2 x 1
0 1 1 2 x x 1 2 x 3 1 0 0 0 0 0 1 1 1
0 1 x 2 2 2 1 3 x 3 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 2 x 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 1 1 2 2 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 x x 1 0 0 0 0 0
0 0 1 1 1 0 1 1 1 0 1 2 2 1 0 0 0 0 0
0 0 1 x 2 1 3 x 2 0 0 0 0 0 0 1 1 1 0
0 0 1 1 2 x 3 x 3 1 1 0 0 0 0 1 x 1 0
0 0 0 0 1 2 3 2 2 x 1 0 0 0 0 1 1 1 0
0 0 0 0 0 1 x 1 1 1 1 0 0 0 0 0 1 1 1
0 0 1 1 2 2 2 1 0 0 0 0 0 0 0 0 1 x 1
0 0 1 x 2 x 2 1 1 0 0 0 0 0 0 0 1 1 1
0 0 1 1 2 1 3 x 3 1 0 0 0 0 0 0 0 1 1
0 0 0 0 0 0 2 x x 1 0 0 0 1 1 1 0 1 x
0 0 0 1 1 1 1 2 2 1 0 0 0 1 x 1 1 2 2
0 0 0 1 x 3 2 1 0 0 0 1 1 2 1 1 1 x 2
0 0 0 1 2 x x 1 0 0 0 1 x 1 0 1 2 3 x
0 0 0 0 1 2 2 1 1 1 1 1 1 1 0 1 x 3 2
0 0 0 0 1 1 1 1 2 x 1 1 1 1 0 2 3 x 2
0 0 0 0 1 x 1 1 x 2 1 1 x 1 0 1 x 3 x
""".strip()

def open(n,m):
    res = [i.split(' ') for i in result.split('\n')]
    if res[n][m] == 'x':
        print('Mine blowed(((')
    return res[n][m]
    
print(solve_mine(gamemap, 2))