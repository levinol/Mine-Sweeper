import sys
import json
def solve_mine(map, n):
    # coding and coding...
    mine = [i.split(' ') for i in map.split('\n')]
    field = MineSweeper(mine, n)
    #compare last map with new map
    if len(field.status_dict['n']) == 0:
        print('No bomb scenario')
        if n == 0:
            for r, c in field.status_dict['b']:
                field.map[r][c] = map_open(r,c)
            return field.get_map()
        elif n == len(field.status_dict['b']):
            for r, c in field.status_dict['b']:
                field.map[r][c] = 'x'
            return field.get_map()
        else:
            return '?'
    i = 0
    counter = 0
    while (field.status_dict['n'] and counter <2):
    #for j in range(10):
        print("Iteration: ", i)
        st1 = field.get_map()
        field.maybe_solve()
        st2 = field.get_map()
        if st1 == st2:
            print('we stuck')
            counter += 1
            a = field.modulate_solve()
            if a:
                counter = 0
        else:
            counter = 0
        print(field)
        i +=1
    
    if counter ==2:
        return '?'
    else:
        if len(field.status_dict['b']) > 0:
            if n - len(field.status_dict['x']) == 0:
                for r, c in field.status_dict['b']:
                        field.map[r][c] = map_open(r,c)
                return field.get_map()
            elif n - len(field.status_dict['x']) == len(field.status_dict['b']):
                for r, c in field.status_dict['b']:
                    field.map[r][c] = 'x'
                return field.get_map()
            else:
                print('How?')
                return '?'
        else:
            return st2

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
    
                    
    def maybe_solve(self):
        numbers = self.status_dict['n'].copy()
        for row, column in numbers:
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
                    self.map[r][c] = map_open(r,c)
                    self.status_dict['b'].remove((r,c))
                    self.status_dict['n'].append((r,c))
                self.status_dict['n'].remove((row,column))
                self.status_dict['u'].append((row,column))
        return 0
  
    def modulate_solve(self):
        changes_flag = 0
        #Сортирую от наименьшего кол-ва соседей & мин к наибольшему  
        numbers = self.status_dict['n'].copy()
        temp_dict ={}
        for row, column in numbers:
            c_x, c_h, near = self.x(self.map, row, column)
            temp_dict[(row,column)] = (int(self.map[row][column]) - c_x, len(near), near)
        temp_order_arr = sorted(temp_dict, key=lambda k: (temp_dict[k][1], temp_dict[k][0]))
        left_bombs = self.n - len(self.status_dict['x'])
        intersec_set = set()
        print('Осталось ', left_bombs, ' бомб')
        # - это че
        if left_bombs == 0:
            if len(temp_dict) == 1 and temp_dict[temp_order_arr[0]][2] == []:
                self.status_dict['n'].remove(temp_order_arr[0])
                return 0

        #Проход по словарю 
        for i in temp_order_arr:
            temp_bomb_dict = {}
            temp_fo_dict = {}
            for j in temp_dict[i][2]:
                #near maybe bombs
                print(i, '->', j)
                maybe_x, fo_arr, flag = modulate_x(self.map, self.status_dict, i, j,left_bombs)
                if flag == 1:
                    self.map[j[0]][j[1]] = map_open(j[0],j[1])
                    changes_flag = 1
                    print('I map_opened')
                    self.status_dict['b'].remove(j)
                    self.status_dict['n'].append(j)
                    break
                elif flag == 2:
                    print('Развилка получаеца')
                    continue
                else:
                    #суммировать maybe_x и fo_arr в словарь
                    for xs in maybe_x:
                        temp_bomb_dict[xs] = temp_bomb_dict.get(xs, 0) + 1
                    for fo in fo_arr:
                        temp_fo_dict[fo] = temp_fo_dict.get(fo, 0) + 1
                
            if flag == 1:
                break
            iter_count = len(temp_dict[i][2])
            print("Count iter: ", iter_count)
            if iter_count > left_bombs:
                print('Надо разобраться')
            print('Bombs:', temp_bomb_dict, len(temp_bomb_dict))
            for cell, count in temp_bomb_dict.items():
                if count == iter_count:
                    print('Modulation found bomb', cell, count)
                    self.map[cell[0]][cell[1]] = 'x'
                    changes_flag = 1
                    self.status_dict['b'].remove(cell)
                    self.status_dict['x'].append(cell)
                
            print('F_o:', temp_fo_dict)
            for cell, count in temp_fo_dict.items():
                if count == iter_count:
                    print('Modulation found map_open cell', cell, count)
                    self.map[cell[0]][cell[1]] = map_open(cell[0],cell[1])
                    changes_flag = 1
                    self.status_dict['b'].remove(cell)
                    self.status_dict['n'].append(cell)
            
            #final thoughs
            #Речекнуть
            if left_bombs == 1 and iter_count < len(temp_bomb_dict):
                for i in set(temp_bomb_dict.keys()) - set(temp_dict[i][2]):
                    print('Kinda final map_open', i)
                    self.map[i[0]][i[1]] = map_open(i[0],i[1])
                    changes_flag = 1
                    self.status_dict['b'].remove(i)
                    self.status_dict['n'].append(i)    
            
            if changes_flag == 1:
                break

        if changes_flag == 1:
            return 1
        else: return 0
        


def modulate_x(map, stat_dict, number, bomb, n_left):
    maybe_x_arr = [bomb]
    fake_map_opened_arr = []
    #check neighb
    #while?
    used_set = set(stat_dict['u'])
    used_numbers = []
    numbers = intersection(map, number, bomb,used_set)
    flag = 0
    
    while numbers and flag==0:
        numers_for_iteration = numbers.copy()
        fork_counter = 0
        for row, column in numers_for_iteration:
            #ЧЕКНУТЬ СОСЕДЕЙ НА ДРУГОЙ СТОРОНЕ
            #check neighb
            c_x, c_h, near = x_fake(map, maybe_x_arr, fake_map_opened_arr, row, column)
            ma_numb = int(map[row][column])
            if c_x + c_h == ma_numb:
                for r, c in near:
                    maybe_x_arr.append((r,c))
                    numbers.update(intersection(map,(row,column), (r,c), used_set))
                #remove from numbers
                fork_counter = 0
                numbers.remove((row,column))
                used_numbers.append((row,column))
            elif c_x == ma_numb:
                for r, c in near:
                    fake_map_opened_arr.append((r,c))
                    numbers.update(intersection(map,(row,column), (r,c), used_set))
                #remove from numbers
                fork_counter = 0
                numbers.remove((row,column))
                used_numbers.append((row,column))
            elif c_x + c_h > ma_numb:
                #развилка
                print('Код красный код красный')
                fork_counter += 1
                if len(maybe_x_arr) == n_left:
                    print('We are in fucked scenario')
                    flag = 1

                if fork_counter == len(numbers):
                    #вот сюды
                    if n_left - len(maybe_x_arr) == 1:
                        print('Fork intersection')
                        near_set = set()
                        for forks in numbers:
                            c_x2, c_h2, near2 = x_fake(map, maybe_x_arr, fake_map_opened_arr, forks[0], forks[1])
                            if near_set:
                                near_set.intersection_update(near2)
                            else:
                                near_set = set(near2)
                        
                        if len(near_set) == 1:
                            for r, c in near_set:
                                maybe_x_arr.append((r,c))
                                numbers.update(intersection(map,(row,column), (r,c), used_set))
                            #remove from numbers
                            fork_counter = 0
                            #numbers.remove((row,column))
                            #used_numbers.append((row,column))
                        else:
                            flag = 2
                    else:
                        flag = 2
                else:
                    print('не циклись')
            elif ma_numb - c_x > c_h:
                print('We are in fucked scenario')
                flag = 1
            elif c_h == 0 and c_x:
                print('We are in fucked scenario')
                flag = 1
            elif c_x == 0 and ma_numb!= 0:
                print('We are in fucked scenario')
                flag = 1
        if n_left - len(maybe_x_arr) > 0 and set(maybe_x_arr) | set(fake_map_opened_arr) == set(stat_dict['b']):
            print('We are in fucked scenario')
            flag = 1
            
    if n_left == len(maybe_x_arr):
        if set(stat_dict['n']) - set(used_numbers):
            print('We are in fucked scenario')
            flag = 1
        #print('Файнал чек',len(set(stat_dict['n'])), len(set(used_numbers)),  set(used_numbers) - set(stat_dict['n']), sep = '\n')
        #print(stat_dict)
    
    return maybe_x_arr, fake_map_opened_arr, flag


def x_fake(map, bomb_arr, fake_arr, n, m):
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
                        if (i,j) in fake_arr:
                            continue
                        elif (i,j) in bomb_arr:
                            count_x +=1
                        else:
                            count_h += 1
                            near_h.append((i,j))
                    elif map[i][j] == 'x':
                        count_x +=1
                except IndexError:
                    continue
    return count_x, count_h, near_h

def intersection(map, number, bomb, used_set):
    return (near_n(map, number)|near_n(map, bomb)) - used_set

def near_n(map, cell):
    n = cell[0]
    m = cell[1]
    near_n = set()
    for i in range(n-1, n+2):
        for j in range(m-1, m+2):
            if i == n and j == m:
                continue
            elif i < 0 or j < 0:
                continue
            else:
                try:
                    if str(map[i][j]) in '012345678':
                        near_n.add((i,j))
                except IndexError:
                    continue
    return near_n



def map_open(n,m):
    res = [i.split(' ') for i in result.split('\n')]
    if res[n][m] == 'x':
        print('MINE blowed(((')
        raise ValueError
    return res[n][m]

if __name__ == "__main__":
    print('Receiving cmd args: ',sys.argv[1])
    with open(sys.argv[1], 'r') as f:
        gamemap, result = json.load(f)
    print(solve_mine(gamemap, 4))