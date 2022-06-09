
def load_words_dict(file_path):
    with open(file_path, 'r') as words:
        dictionary = {i[:-1]: True for i in words}
    return dictionary


def is_valid_path(board, path, words):
    used_cells = []
    word = ""
    if not path:
        return #path is empty
    for i in path:
        if not is_cell_in_board(i, board):
            return None  # invalid cell location in path
    for j in range(len(path) - 1):
        tup = path[j]
        word += board[tup[0]][tup[1]]
        x = path[j][0] - path[j + 1][0]
        y = path[j][1] - path[j + 1][1]
        if abs(x) > 1 or abs(y) > 1 or tup in used_cells:
            return None  # invalid step in path
        used_cells.append(tup)
    if path[-1] in used_cells:
        return None  # cell location appears more then once in path
    word += board[path[-1][0]][path[-1][1]]
    try:
        if words[word]:
            return word
    except KeyError:
        return None  # No word that matches path


def is_cell_in_board(cell, board):
    """checks if the cell is within the board
    :returns True or False"""
    rows = len(board)
    columns = len(board[0])
    if cell[0] > rows - 1 or cell[0] < 0 or cell[1] > columns - 1 or cell[1] < 0:
        return False
    else:
        return True


def valid_steps(cell, board):
    """returns a list with all the possible cells to move to, using one step"""
    u = (cell[0] - 1, cell[1])
    ur = (cell[0] - 1, cell[1] + 1)
    r = (cell[0], cell[1] + 1)
    rd = (cell[0] + 1, cell[1] + 1)
    d = (cell[0] + 1, cell[1])
    dl = (cell[0] + 1, cell[1] - 1)
    le = (cell[0], cell[1] - 1)
    lu = (cell[0] - 1, cell[1] - 1)
    lst = [u, ur, r, rd, d, dl, le, lu]
    temp = lst[:]
    for i in temp:
        if not is_cell_in_board(i, board):
            lst.remove(i)
    return lst


def find_length_n_words(n: int, board: list, words: dict) -> list:
    words_locations = []
    find_length_n_words_helper(n, board, words, words_locations)
    return words_locations


def find_length_n_words_helper(n, board, words, words_locations):
    for row in range(len(board)):
        for col in range(len(board[row])):
            find_length_n_words_helper_helper(n - 1, board, words, words_locations, (row, col), f'{row}{col} ')


def find_length_n_words_helper_helper(n, board, words, words_locations, current_location=(0, 0), current_path=''):
    if n == 0:
        path_nums = current_path.split(' ')[:-1]
        path = []
        for i in path_nums:
            path.append((int(i[0]), int(i[1])))
        word = is_valid_path(board, path, words)
        if word is not None:
            words_locations.append((word, path))
            return
        else:
            return
    poss_steps = valid_steps(current_location, board)
    for step in poss_steps:
        if str(step) not in current_path:
            find_length_n_words_helper_helper(n - 1, board, words, words_locations, step,
                                              current_path + f'{step[0]}{step[1]} ')

