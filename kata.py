def solve_mine(map, n):
    # coding and coding...
    mine = [i.split(' ') for i in map.split('\n')]
    field = MineSweeper(mine, n)
    #compare last map with new map
    flag = 0
    for i in range(10):
        print("Iteration: ", i)
        st1 = field.get_map()
        field.maybe_solve(flag)
        st2 = field.get_map()
        if st1 == st2:
            print('we stuck')
            flag = 1
        else:
            flag = 0
        print(field)
    return 0

class MineSweeper():
    def __init__(self, map, n):
        self.map = map
        self.n = n
        self.rows = len(map)
        self.columns = len(map[0])
        self.status_dict = {'b': [], 'n': [], 'x': [], 'u': []}
        for i in range(self.rows):
            for j in range(self.columns):
                status = self.check_neighbors(self.map, i, j)
                self.status_dict[status].append((i,j))
    def __str__(self):
        map_str = '\n'.join([ (' '.join([str(elem) for elem in row])) for row in self.map])
        return 'Map:\n' + map_str + '\n'

    def get_map(self):
        map_str = '\n'.join([ (' '.join([str(elem) for elem in row])) for row in self.map])
        return map_str

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
    def x(map, n, m):
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
                        if map[i][j] == '?':
                            count_h += 1
                            near_h.append((i,j))
                        elif map[i][j] == 'x':
                            count_x +=1
                    except IndexError:
                        continue
        return count_x, count_h, near_h
                    
    def maybe_solve(self, flag):
        for row, column in self.status_dict['n']:
            #check neighb
            c_x, c_h, near = self.x(self.map, row, column)
            if c_x + c_h == int(self.map[row][column]):
                for r, c in near:
                    self.map[r][c] = 'x'
                    self.status_dict['b'].remove((r,c))
                    self.status_dict['x'].append((r,c))
                self.status_dict['n'].remove((row,column))
                self.status_dict['u'].append((row,column))
            elif c_x == int(self.map[row][column]):
                for r, c in near:
                    self.map[r][c] = open(r,c)
                    self.status_dict['b'].remove((r,c))
                    self.status_dict['n'].append((r,c))
                self.status_dict['n'].remove((row,column))
                self.status_dict['u'].append((row,column))
            elif c_x + c_h > int(self.map[row][column]) and flag:
                print("Im in ", row, column)
                print(int(self.map[row][column]) - c_x, 'bombs near')
                print(near)
        return 0

gamemap = """
? ? ? ? ? ?
? ? ? ? ? ?
? ? ? 0 ? ?
? ? ? ? ? ?
? ? ? ? ? ?
0 0 0 ? ? ?
""".strip()
result = """
1 x 1 1 x 1
2 2 2 1 2 2
2 x 2 0 1 x
2 x 2 1 2 2
1 1 1 1 x 1
0 0 0 1 1 1
""".strip()

def open(n,m):
    res = [i.split(' ') for i in result.split('\n')]
    if res[n][m] == 'x':
        print('Mine blowed(((')
    return res[n][m]
    
print(solve_mine(gamemap, 2))