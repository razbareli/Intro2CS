########################################
#  File: ex8.py
#  Authors: Yuval Omer and Raz Bareli
########################################
# We chose when running the intersection_row function To leave uncertain members as uncertain members
# Since we didn't want the program to start guessing answers and then we might get to a situation where
# The board can't be solved anymore.
from copy import deepcopy


# A function the creates a list with all the possible ways to paint a row with length n and a list of constraints
def constraint_satisfactions(n, blocks):
    if sum(blocks) > n:
        return []
    results = []
    constraint_satisfactions_helper(n, blocks, blocks[0], results, n)
    return results


# A helper function for the constraint_satisfactions function
def constraint_satisfactions_helper(n, constraints, current_constraint, results, length, con_ind=0, poss=''):
    if len(poss) > length:  # If the length of the current combination is longer than n stop.
        return

    elif (n >= 0) and (current_constraint == 0) and (con_ind == len(constraints) - 1):
        for i in range(n):
            poss += '0'
        poss_list = [int(num) for num in poss]
        results.append(poss_list)
        return

    elif (n < current_constraint) or (len(poss) > length):
        return

    if current_constraint > 0:
        constraint_satisfactions_helper(n - 1, constraints, current_constraint - 1, results, length, con_ind,
                                         poss + '1')
        if (n < current_constraint) or (len(poss) > length):
            return
        poss_list_check = [num for num in poss]

        if len(poss) > 0:
            if poss_list_check[len(poss_list_check) - 1] == '0':
                constraint_satisfactions_helper(n - 1, constraints, current_constraint,
                                                 results, length, con_ind, poss + '0')

        else:
            # If the current combination is empty add a 0 to current combination
            constraint_satisfactions_helper(n - 1, constraints, current_constraint,
                                             results, length, con_ind, poss + '0')

        if (n < current_constraint) or (len(poss) > length):
            return

    elif current_constraint == 0:  # If we have finished a constraint add a 0 and move to the next constraint.
        constraint_satisfactions_helper(n - 1, constraints, constraints[con_ind + 1], results, length, con_ind + 1,
                                         poss + '0')


# A function the returns all the possible ways to complete a row while adhering to the constraints
def row_variations(row, blocks):
    if sum(blocks) == 0:
        # if there are no constraints on the list then the row must be empty to be valid.
        result = []
        for num in row:
            if num == 1:
                return []
            elif num == 0 or num == -1:
                result.append(0)
        return [result]
    result_lst = []
    row_variations_helper(blocks[0], row, result_lst, blocks)
    return result_lst


# A helper function to the row_variations function
def row_variations_helper(current_constraint, row_lst, result_lst, _constraints, poss='', constraint_ind=0):
    if len(row_lst) < current_constraint + sum(_constraints[constraint_ind + 1:]):
        # If there is no place left in the row_lst to complete
        # the constraints the current possibility is invalid.
        return

    if not row_lst:
        # If row_lst is empty and all constraints are fulfilled
        # then the current possibility is valid
        result = [int(n) for n in poss]
        if sum(result) == sum(_constraints):
            result_lst.append(result)
        return

    if current_constraint == 0:
        # If the current constraint is fulfilled and the next number on the list is
        # 1 then that means the current possibility is invalid
        if row_lst[0] == 1:
            return
        else:
            # Else move to the next constraint and add 0 to current possibility
            if constraint_ind < len(_constraints) - 1:
                constraint_ind += 1
                current_constraint = _constraints[constraint_ind]
            row_variations_helper(current_constraint, row_lst[1:], result_lst, _constraints, poss + '0', constraint_ind)

    # If we have started to fulfill a constraint and the next number on the list is -1
    # Then the number must be assigned as 1 for the row to be valid.
    elif (current_constraint < _constraints[constraint_ind]) and (row_lst[0] == -1):
        if poss[len(poss) - 1] == '1':
            current_constraint -= 1
            row_variations_helper(current_constraint, row_lst[1:], result_lst, _constraints, poss + '1', constraint_ind)

    # If the next number on the row_lst is 0 then add 0 to the current possibility
    elif row_lst[0] == 0:
        row_variations_helper(current_constraint, row_lst[1:], result_lst, _constraints, poss + '0', constraint_ind)

    # If the next number on the row_lst is 1 then add 1 to the current possibility and decrease the current
    # constraint by 1
    elif row_lst[0] == 1:
        current_constraint -= 1
        row_variations_helper(current_constraint, row_lst[1:], result_lst, _constraints, poss + '1', constraint_ind)

    # If we current constraint is still at it's original value and the first number on
    # the row list is -1 then try to check if a valid row is created when you add 0 to the current
    # possibility, and then again but add 1 instead.
    else:
        row_variations_helper(current_constraint, row_lst[1:], result_lst, _constraints, poss + '0', constraint_ind)
        current_constraint -= 1
        row_variations_helper(current_constraint, row_lst[1:], result_lst, _constraints, poss + '1', constraint_ind)


# A function that returns the intersection of members between rows.
def intersection_row(rows):
    num_of_rows = len(rows)
    result = []
    for ind in range(len(rows[0])):
        num_of_1 = 0
        num_of_0 = 0
        current_col = []
        for row in rows:
            current_col.append(row[ind])
        for num in current_col:
            if num == 1:
                num_of_1 += 1
            elif num == 0:
                num_of_0 += 1
        if num_of_1 == num_of_rows:
            result.append(1)
        elif num_of_0 == num_of_rows:
            result.append(0)
        else:
            result.append(-1)
    return result


# A function that solves simple nonogram
def solve_easy_nonogram(constraints):
    board = []
    for row in range(len(constraints[0])):
        new_row = []
        for col in range(len(constraints[1])):
            new_row.append(-1)
        board.append(new_row)
    col_indexes_to_solve = [i for i in range(len(board[0]))]
    row_indexes_to_solve = [i for i in range(len(board))]
    board = solve_easy_nonogram_helper(constraints, board, col_indexes_to_solve, row_indexes_to_solve)
    return board


# A helper function for the solve_easy_nonogram function
def solve_easy_nonogram_helper(constraints, board=None, col_indexes_to_solve=None, row_indexes_to_solve=None):
    while True:
        lines_changed1 = solve_easy_nonogram_helper_helper(board, constraints, row_indexes_to_solve,
                                                           col_indexes_to_solve)
        if lines_changed1 is None:
            return []
        board = col_to_row(board)
        lines_changed2 = solve_easy_nonogram_helper_helper(board, constraints, row_indexes_to_solve,
                                                           col_indexes_to_solve, True)
        if lines_changed2 is None:
            return []
        board = col_to_row(board)
        if lines_changed1 + lines_changed2 == 0:
            break
    return board


# A helper for the solve_easy_nonogram_helper
def solve_easy_nonogram_helper_helper(board, constraints, row_indexes, col_indexes,
                                      is_col_board=False, lines_changed=0):
    if not is_col_board:
        current_indexes = row_indexes
    else:
        current_indexes = col_indexes
    for num in current_indexes:
        results_possibilities = row_variations(board[num], constraints[0 + int(is_col_board)][num])
        if not results_possibilities:
            return
        if len(results_possibilities[0]) > 1:
            certain_result = intersection_row(results_possibilities)
        else:
            certain_result = results_possibilities[0]
        if board[num] != certain_result:
            lines_changed += 1
            board[num] = certain_result
        if sum(board[num]) == sum(constraints[0 + int(is_col_board)][num]):
            current_indexes.remove(num)
    return lines_changed


# A function that transposes the board
def col_to_row(board):
    col_board = [[board[j][i] for j in range(len(board))] for i in range(len(board[0]))]
    return col_board


# A program that solves nonograms of all kinds and if there are more than one option it will return all options.
def solve_nonogram(constraints):
    solutions = []
    board = []
    for row in range(len(constraints[0])):
        new_row = []
        for col in range(len(constraints[1])):
            new_row.append(-1)
        board.append(new_row)
    col_indexes_to_solve = [i for i in range(len(board[0]))]
    row_indexes_to_solve = [i for i in range(len(board))]
    board = solve_easy_nonogram_helper(constraints, board, col_indexes_to_solve, row_indexes_to_solve)
    if board == []:
        return []
    if not col_indexes_to_solve and not row_indexes_to_solve:
        solutions.append(board)
    else:
        solve_nonogram_helper(board, col_indexes_to_solve, row_indexes_to_solve, solutions, constraints)
    return solutions


# A helper program for the solve_nonogram function
def solve_nonogram_helper(board, col_to_solve, row_to_solve, solutions_list, constraints):
    row_options = row_variations(board[row_to_solve[0]], constraints[0][row_to_solve[0]])
    for option in row_options:
        co = deepcopy(col_to_solve)
        ro = deepcopy(row_to_solve)
        temp_board = deepcopy(board)
        temp_board[row_to_solve[0]] = option
        temp_board = solve_easy_nonogram_helper(constraints, temp_board, co, ro)
        if not co and not ro:
            solutions_list.append(temp_board)
        elif temp_board:
            solve_nonogram_helper(temp_board, co, ro, solutions_list, constraints)
