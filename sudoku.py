import sys; args = sys.argv[1:]
from time import perf_counter
with open(args[0]) as f:
    line_list = [line.strip() for line in f]
square, subblock_width, subblock_height, total_symbol_set, symbol_set, n, neighbors,symbol_set_set = {0, 1, 256, 4, 9, 16, 144, 400, 529, 25, 289, 36, 169, 49, 441, 64, 576, 196, 324, 81, 225, 100, 484, 361, 121}, 0,0, ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q','r','s', 't', 'u'], [], 0, dict(), set()
list_of_sets = []
def factor1(start, end):
    for i in range(start + 1, end):
        if (end % i) == 0:
            return int(i)
def factor2(start, end):
    for i in range(0, start):
        if (end % (start - i)) == 0:
            return int(start - i)
def symbol_count(board):
    temp_dict = {}
    for i in symbol_set:
        temp_dict[i] = 0
    for i in board.values():
        if i[0] in symbol_set:
            temp_dict[i[0]] = temp_dict[i[0]] + 1
    return temp_dict
def print_puzzle(puzzle):
    global subblock_width, subblock_height, symbol_set, symbol_set_set
    n = int(len(puzzle) ** 0.5)
    for i in range(0, n):
            symbol_set.append(total_symbol_set[i].upper())
    symbol_set_set = set(symbol_set)
    if n in square:
        subblock_width, subblock_height = int(n ** 0.5), int(n ** 0.5)
    else:
        subblock_width, subblock_height = factor1(int(n ** 0.5), n), factor2(int(n ** 0.5), n)    
def convert(puzzle):
    str_symbol_set = "".join(symbol_set)
    puzzle_dict = {}
    for i in range(0, len(puzzle)):
        if puzzle[i] == '.':
            puzzle_dict[i] = (str_symbol_set)
        else:
            puzzle_dict[i] = puzzle[i]
    return puzzle_dict
def constraint_sets(puzzle):
    global list_of_sets
    temp_set1 = set()
    for i in range(0, len(puzzle)): #row
        temp_set1.add(i)
        if ((i + 1) % (n) == 0):
            list_of_sets.append(temp_set1)
            temp_set1 = set()
    for i in range(0, n): #column
        for j in range(0, len(puzzle), n):
            temp_set1.add(i + j)
        list_of_sets.append(temp_set1)
        temp_set1 = set()
    for i in range(0, subblock_width):  #width = 5
        for j in range(0, subblock_height): #height = 2
            for x in range(0, subblock_width):
                for y in range(0, subblock_height):
                    temp_set1.add(i * (n * subblock_height) + j * subblock_width + y * n + x)
            list_of_sets.append(temp_set1)
            temp_set1 = set()
    global neighbors
    for i in range(0, len(puzzle)):
        temp = set()
        for s in list_of_sets:
            if i in s:
                for j in s:
                    temp.add(j)
        temp.remove(i)
        neighbors[i] = temp
        temp = set()

def get_next_unassigned_var(state):
    temp_dict = {}
    for i in symbol_set:
        temp_dict[i] = 0
    for i in state:
        if i[0] in symbol_set:
            temp_dict[i[0]] = temp_dict[i[0]] + 1
    return temp_dict
    return False
def print_p(puzzle):
    for i in range(n):
        for j in range(n):
            print(puzzle[i*n + j], end= " ")
        print("\n")
def get_most_constrained_var(puzzle):
    min = n + 1
    min_index = 0
    for i in puzzle:
        temp = len(puzzle[i])
        if (temp < min and  temp > 1):
            min = temp
            min_index = i
    # print(min_index)
    return min_index
def get_sorted_values(puzzle, var, dict_of_values):
    temp_set = set()
    sorted_values = []
    for i in dict_of_values[var]:
        temp_set.add(puzzle[i])
    for i in symbol_set:
        if i not in temp_set:
            sorted_values.append(i)
    return sorted_values
def get_sorted_values_forward_looking(puzzle, var):
    return puzzle[var]

def forward_looking_first(board):
    solved_indices = []
    for i in board:
        if len(board[i]) == 1:
            for j in neighbors[i]:
                # if (len(board[j][1]) == 0):
                #     return None
                # print(neighbors[i])
                # print(j, i)
                # print(board[j], board[i])
                temp = len(board[j])
                board[j] = board[j].replace(board[i], '')
                if (temp == 2) and (len(board[j]) == 1):
                    solved_indices.append(j)  
    return forward_looking(board, solved_indices)

def forward_looking(board, solved_indices):
    # for j in neighbors[solved]:
    #     board[j] = board[j].replace(board[solved], '')
    #     if len(board[j]) == 0:
    #         return None
    # return board
    # print(solved)
    # solved_indices = [solved]

    while solved_indices:
        solved = solved_indices.pop()
        for j in neighbors[solved]:
            temp = len(board[j])
            board[j] = board[j].replace(board[solved], '')
            if len(board[j]) == 0:
                return None
            if (temp == 2) and (len(board[j]) == 1):
                solved_indices.append(j) 
        # solved_indices.remove(solved)   
    return board
def constraint_propagation(board):
    solved_indices = []
    for constraint in list_of_sets:
        for symbol in symbol_set:
            occurrences = [index for index in constraint if symbol in board[index]]
            num_of_occ = len(occurrences)
            if num_of_occ == 1 and len(board[occurrences[0]]) > 1:
                board[occurrences[0]] = symbol
                solved_indices.append(occurrences[0])
            elif num_of_occ == 0:
                return None
    return forward_looking(board,solved_indices)
def goal_test(converted_dict):
    # # print(converted_dict)
    # temp_dict = {i:0 for i in symbol_set}
    # for i in converted_dict.values():
    #     for j in i:
    #     # if len(i) != 1:
    #     #     return False
    #         temp_dict[j] += 1
    # for i in temp_dict:
    #     if temp_dict[i] != n:
    #         return False
    # return True
    return solution_checker(converted_dict)
def csp_backtracking_forward_looking(converted_dict):
    goal_test_boolean = solution_checker(converted_dict)
    if goal_test_boolean:
        return converted_dict
    var = get_most_constrained_var(converted_dict)
    for val in get_sorted_values_forward_looking(converted_dict, var):
        new_dict = converted_dict.copy()
        new_dict[var] = val
        checked_board = forward_looking(new_dict,[var])
        if checked_board is not None:
            checked_board = constraint_propagation(checked_board)
            if checked_board is not None:
                result = csp_backtracking_forward_looking(checked_board)
                if result is not None:
                    return "".join([result[i] for i in range(len(result))])
    return None

def solution_checker(board):
    for i in list_of_sets:
        # print(i)
        # input()
        temp_set = {board[j] for j in i}
        # temp_set.add(board[i])
        # print(temp_set)
        # print(symbol_set_set)
        # print(temp_set == symbol_set_set)
        # input()
        if temp_set != symbol_set_set:
            return False
        temp_set.clear()
    return True
start = perf_counter()
c = 1
for i in line_list:
    t = perf_counter()
    n = int(len(i) ** 0.5)
    print_puzzle(i)
    converted_dict = convert(i)
    constraint_sets(i)
    converted_dict = forward_looking_first(converted_dict)
    print(c, ":", i)
    s = ' ' * len(str(c)) + '   '
    if solution_checker(converted_dict):
        for i in converted_dict:
            s += converted_dict[i]
        print(s, 324, f'{(perf_counter() - t):.4g}')
    else:
        s += (csp_backtracking_forward_looking(converted_dict))
        print(s, 324, f'{(perf_counter() - t):.4g}')

    symbol_set = []
    list_of_sets = []
    neighbors = dict()
    # input()
    # input()
    c += 1
# print(perf_counter() - start)
# Kunal Bham, pd 3, 2024