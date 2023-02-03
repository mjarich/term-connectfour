from termcolor import colored
import os

clear = lambda : os.system('clear')

__row__ = '--- '
__col__ = ' | '

long_line = '  ' + __row__ * 7

board_dict = {0: ' ',
              1: colored('O', color='red', attrs=['bold']),
              2: colored('O', color='yellow', attrs=['bold'])}

player_dict = {1: 'red',
               2: 'yellow'}

board_matrix = [[0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]


def execute_one_turn(player, previous_error, last_turn=False):
    clear()
    def print_row(i):
        print(
            __col__ + board_dict[board_matrix[i][0]] + __col__ + board_dict[board_matrix[i][1]] + __col__ + board_dict[
                board_matrix[i][2]] +
            __col__ + board_dict[board_matrix[i][3]] + __col__ + board_dict[board_matrix[i][4]] + __col__ + board_dict[
                board_matrix[i][5]] +
            __col__ + board_dict[board_matrix[i][6]] + __col__)

    print(long_line)
    for i in range(6):
        print_row(i)
        print(long_line)

    print('   1   2   3   4   5   6   7')
    if not last_turn:
        if previous_error is not None:
            print(previous_error)
        column = input(
            'It is {} turn! Enter a column number to complete your turn.\n'.format(
                colored(player + '\'s', color=player)))
        return column
    else:
        print('{} wins!'.format(colored(player, color=player)))


def play():
    first_player_decided = False
    game_over = False
    error = None

    while not first_player_decided:
        starter = input('Who gets the first move? Enter 0 for RED, 1 for YELLOW.\n')

        if starter.strip() == '0' or starter.strip() == '1':
            first_player_decided = True
            if starter.strip() == '0':
                curr_player = 1
            else:
                curr_player = 2
        else:
            print('Input cannot be interpreted.')

    while not game_over:
        column_num = execute_one_turn(player_dict[curr_player], previous_error=error)
        error = None
        try:
            column_num = int(column_num) - 1
            column = [board_matrix[i][column_num] for i in range(6)]
            if column_num in [0, 1, 2, 3, 4, 5, 6]:
                row_number = get_last_zero(column)
                if row_number > -1:
                    board_matrix[row_number][column_num] = curr_player
                    game_over = check_for_game_over()
                    if game_over:
                        execute_one_turn(player_dict[curr_player], previous_error=None, last_turn=True)
                    else:
                        curr_player = 3 - curr_player
                else:
                    error = 'This column is full. Pick a different column.'
        except ValueError:
            error = 'Input cannot be interpreted. Please try again.'
        except IndexError:
            error = 'Enter a number between 1 and 7.'
        if sum([sum(board_matrix[i]) for i in range(6)]) == 21 * 1 + 21 * 2:
            game_over = True
            print('Draw!')


def get_last_zero(column):
    # want to return -1 if full
    # return index to put marker in otherwise
    i = -1
    while column[i + 1] == 0:
        i += 1
        if i == 5:
            break
    return i


def check_for_game_over():
    # checks needed for below
    def check_right(row, column):
        return board_matrix[row][column] == board_matrix[row][column + 1] == board_matrix[row][column + 2] == \
               board_matrix[row][column + 3]

    def check_left(row, column):
        return board_matrix[row][column] == board_matrix[row][column - 1] == board_matrix[row][column - 2] == \
               board_matrix[row][column - 3]

    def check_up(row, column):
        return board_matrix[row][column] == board_matrix[row - 1][column] == board_matrix[row - 2][column] == \
               board_matrix[row - 3][column]

    def check_down(row, column):
        return board_matrix[row][column] == board_matrix[row + 1][column] == board_matrix[row + 2][column] == \
               board_matrix[row + 3][column]

    def check_up_right_diagonal(row, column):
        return board_matrix[row][column] == board_matrix[row - 1][column + 1] == board_matrix[row - 2][column + 2] == \
               board_matrix[row - 3][column + 3]

    def check_down_right_diagonal(row, column):
        return board_matrix[row][column] == board_matrix[row + 1][column + 1] == board_matrix[row + 2][column + 2] == \
               board_matrix[row + 3][column + 3]

    def check_up_left_diagonal(row, column):
        return board_matrix[row][column] == board_matrix[row - 1][column - 1] == board_matrix[row - 2][column - 2] == \
               board_matrix[row - 3][column - 3]

    def check_down_left_diagonal(row, column):
        return board_matrix[row][column] == board_matrix[row + 1][column - 1] == board_matrix[row + 2][column - 2] == \
               board_matrix[row + 3][column - 3]

    for row in range(6):
        for column in range(7):
            if board_matrix[row][column] == 0:
                continue
            else:
                if column < 3:
                    # check to the right
                    c1 = check_right(row, column)
                elif column > 3:
                    # check to the left
                    c1 = check_left(row, column)
                else:
                    c1 = check_left(row, column) or check_right(row, column)

                if row > 2:
                    # check above
                    c2 = check_up(row, column)
                else:
                    # check below
                    c2 = check_down(row, column)

                if column < 3 and row > 2:
                    c3 = check_up_right_diagonal(row, column)
                elif column < 3 and row <= 2:
                    c3 = check_down_right_diagonal(row, column)
                elif column > 3 and row > 2:
                    c3 = check_up_left_diagonal(row, column)
                elif column > 3 and row <= 2:
                    c3 = check_down_left_diagonal(row, column)
                elif column == 3 and row > 2:
                    c3 = check_up_right_diagonal(row, column) or check_up_left_diagonal(row, column)
                else:
                    c3 = check_down_right_diagonal(row, column) or check_down_left_diagonal(row, column)

                if c1 or c2 or c3:
                    return True

if __name__ == '__main__':
    try:
        play()
    except KeyboardInterrupt:
        clear()
        print('Game terminated by CRTL+C. Call it a draw!')
