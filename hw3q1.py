import random

N = 10
USER = 0
COMPUTER = 1
MAX_SIZE = 4

SHIPS = [0, 4, 3, 2, 1]

BATTLESHIP_MARK = '*'
MISS_MARK = 'X'
HIT_MARK = 'V'
EMPTY = ' '
HIT_CODE = 0
MISS_CODE = 1
INVALID_CODE = 2


def check_if_top_vertical(board, x, y):
    '''
    Check if board[y][x] is the top vertical part of the battleship
    :param board: a following table
    :param x: column coordinate
    :param y: row coordinate
    :return: True if the location is top vertical, else False.
    '''
    for j in range(x - 1, max(x - MAX_SIZE, -1), -1):
        if board[y][j] not in [BATTLESHIP_MARK, HIT_MARK]:
            return True
        if board[y][j] == BATTLESHIP_MARK:
            return False

    return True


def check_if_top_horizontal(board, x, y):
    '''
    Check if board[y][x] is the top horizontal part of the battleship.
    :param board: a following table
    :param x: column coordinate
    :param y: row coordinate
    :return: True if the location is top horizontal, else False.
    '''
    for i in range(y - 1, max(y - MAX_SIZE, -1), -1):
        if board[i][x] not in [BATTLESHIP_MARK, HIT_MARK]:
            return True
        if board[i][x] == BATTLESHIP_MARK:
            return False

    return True


def count_battleships(board):
    '''
    Counts the number of battleships left on the table.
    :param board: a following table
    :return: The number of battleships.
    '''
    counter = 0
    num_rows = num_cols = N
    for i in range(num_rows):
        for j in range(num_cols):
            if board[i][j] != BATTLESHIP_MARK:
                continue
            if check_if_top_horizontal(board, j,
                                       i) and check_if_top_vertical(board,
                                                                    j, i):
                counter += 1
    return counter


def print_game_status(user_board, computer_board):
    '''
    Prints the game status.
    :param user_board: the users board
    :param computer_board: the computers board
    :return:
    '''
    pass


def print_drown_battleship_message(player, count):
    '''
    Prints a message when a battleship has drown.
    :param player: the current player
    :param count: the count of battleships
    :return:
    '''
    pass


def print_winner_message(player):
    '''
    Prints a message when the game is over
    :param player: the winner player
    :return:
    '''
    if player == USER:
        print('Congrats! You are the winner :)')
    else:
        print('Game over! The computer won the fight :(')


def check_move(target_b, x, y):
    if target_b[x][y] == ' ':
        target_b[x][y] = MISS_MARK
    if target_b[x][y] == '*':
        target_b[x][y] = HIT_MARK
    return  target_b


def get_valid_computer_move(board):
    '''
    Randomize a valid move.
    :param board: The computer's following table.
    :return: a valid move
    '''
    pass


def get_valid_user_move(board):
    '''
    Scans a valid move from the user.
    :param board: The user's following table.
    :return: a valid move.
    '''
    pass


def attack_location(board, player):
    '''
    Given a player and its following table,
    get valid location and attack it.
    :param board: The players following table.
    :param player: The current player.
    :return: Whether the attack was hit or miss.
    '''
    pass


def board_generator():
    return [[' ' for x in range(N)] for y in range(N)]


def initialize_and_set_board(player):
    board = board_generator()
    if player == USER:
        print_board(board, player)
    sizes = len(SHIPS)
    for size in range(1, sizes):
        for i in range(0, SHIPS[size]):
            if not (size + 1 == sizes and i + 1 == SHIPS[-1]):
                if player == USER:
                    board = set_user_board(board, size, False)
                else:
                    board = set_machine_board(board, size, False)
            else:
                if player == USER:
                    board = set_user_board(board, size, True)
                else:
                    board = set_machine_board(board, size, True)
    if player == USER:
        print('All battleships have been located successfully!')
    return board


def set_user_board(board, size, is_last):
    print('Enter location for Battleship of size {}:'.format(size))
    loc = str(input()).split(',')
    x = int(loc[0])
    y = int(loc[1][:-2])
    side = str(loc[1][-1])
    # if its the last ship to place
    if is_last:
        return validate_and_place(board, x, y, side, size, True, USER)
    return validate_and_place(board, x, y, side, size, False, USER)


def set_machine_board(board, size, is_last):
    x = int(random.randint(0, N-1))
    y = int(random.randint(0, N-1))
    side = 'h' if int(random.randint(0, 1)) == 0 else 'v'
    if is_last:
        return validate_and_place(board, x, y, side, size, True, COMPUTER)
    return validate_and_place(board, x, y, side, size, False, COMPUTER)


def print_board(board, player):
    print('    ', end='')
    print(' '.join([str(row) for row in range(N)]))
    print('    ', end='')
    print(' '.join(['-' for _ in range(N)]))
    for row in range(0, N, 1):
        print(row, end=' | ')
        if player == COMPUTER:
            print(' '.join(board[row]).replace('*', ' '))
        else:
            print(' '.join(board[row]))
    print()


def validate_and_place(board, x, y, side, size, is_last, user):
    if side in 'v':
        return place_vertical_ship(board, x, y, size, is_last, user)
    else:
        return place_side_ship(board, x, y, size, is_last, user)


def place_vertical_ship(board, x, y, size, is_last, user):
    placeable = True
    if y >= 0 and x >= 0 and y + size <= N:
        for index in range(y, y + size):
            if board[index][x] != ' ':
                placeable = False
    else:
        placeable = False
    if placeable:
        for index in range(y, y + size):
            board[index][x] = '*'
        if (not is_last) and user == USER:
            print('Your current board:')
            print_board(board, user)
        return board
    else:
        return retry(board, size, is_last, user)


def place_side_ship(board, x, y, size, is_last, user):
    placeable = True
    if x >= 0 and y >= 0 and x + size <= N:
        for index in range(x, x + size):
            if board[y][index] != ' ':
                placeable = False
    else:
        placeable = False
    if placeable:
        for index in range(x, x + size):
            board[y][index] = '*'
        if (not is_last) and user == USER:
            print('Your current board:')
            print_board(board, user)
        return board
    else:
        return retry(board, size, is_last, user)


def retry(board, size, is_last, user):
    if user == COMPUTER:
        return set_machine_board(board, size, is_last)
    else:
        return coordinates_retry(board, size, is_last)


def coordinates_retry(board, size, is_last):
    print('ERROR: Invalid location')
    message = 'Please enter location for Battleship of size {} again:'
    print(message.format(size))
    loc = str(input()).split(',')
    x = int(loc[0])
    y = int(loc[1][:-2])
    side = str(loc[1][-1])
    return validate_and_place(board, x, y, side, size, is_last, USER)


def game_manager(boards, user_b, computer_b, player):
    if player % 2 == 0:
        computer_b = play_turn(boards[1], USER)
    else:
        user_b = play_turn(boards[0], COMPUTER)
    game_manager(boards, user_b, computer_b, player + 1)


def play_turn(target_b, player):
    loc = ''
    if player == USER:
        print("It's your turn!")
        print('Enter location for attack:')
        loc = str(input())[::-1].split(',')
        print('Your following table:')
    else:
        print("The computer's following table:")
        loc = computer_attack_generator()
    target_b = check_move(target_b, int(loc[0]), int(loc[1]))
    print_board(target_b, player + 1)
    return target_b


def computer_attack_generator():
    return [random.randint(0, N-1), random.randint(0, N-1)]


def first_part():
    print('Your current board:')
    user_board = initialize_and_set_board(USER)
    print('Your following table:')
    computer_board = initialize_and_set_board(COMPUTER)
    print_board(computer_board, USER)
    print("The computer's following table:")
    print_board(user_board, USER)
    return [user_board, computer_board]


def main():
    print('Welcome to Battleship!')
    print('Please enter seed:')
    seed = int(input())
    random.seed(seed)

    # boards initialisation
    boards = first_part()
    user_following_table = board_generator()
    comp_following_table = board_generator()
    game_manager(boards, user_following_table, comp_following_table, 2)


if __name__ == '__main__':
    main()