import random

N = 10
USER = 0
COMPUTER = 1
MAX_SIZE = 4

SHIPS = [0, 4, 3, 2, 1]

SHIP_MARK = '*'
MISS_MARK = 'X'
HIT_MARK = 'V'
EMPTY = ' '
HIT_CODE = 0
MISS_CODE = 1
INVALID_CODE = 2


def board_generator():
    return [[' ' for x in range(N)] for y in range(N)]


def initialize_and_set_board(player):
    board = board_generator()
    if player == USER:
        print_board(board, player)
    for size in range(1, len(SHIPS)):
        for i in range(0, SHIPS[size]):
            if not (size + 1 == len(SHIPS) and i + 1 == SHIPS[-1]):
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
    try:
        loc = str(input()).split(',')
        x = int(loc[0])
        y = int(loc[1][:-2])
        side = str(loc[1][-1])
        if is_last:
            return validate_and_place(board, x, y, side, size, True, USER)
        return validate_and_place(board, x, y, side, size, False, USER)
    except:
        set_user_board(board, size, is_last)


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
        if vertical_surroundings_validation(board, x, y, size):
            return place_vertical_ship(board, x, y, size, is_last, user)
        else:
            if user == USER:
                return coordinates_retry(board, size, is_last)
            else:
                return set_machine_board(board, size, is_last)
    else:
        if horizontal_surroundings_validation(board, x, y, size):
            return place_side_ship(board, x, y, size, is_last, user)
        else:
            if user == USER:
                return coordinates_retry(board, size, is_last)
            else:
                return set_machine_board(board, size, is_last)


def vertical_surroundings_validation(board, x, y, size):
    if y + size > N or y < 0:
        return False
    if x == 0:
        if y == 0 and y + size + 1 <= N:
            return check_rectangle(board, x, y, x+1, y + size)
        elif y > 0 and y + size == N:
            return check_rectangle(board, x, y-1, x+1, y + size)
        elif y > 0 and y + size + 1 <= N:
            return check_rectangle(board, x, y-1, x+1, y + size)
    else:
        if y == 0 and y + size + 1 <= N:
            return check_rectangle(board, x-1, y, x+1, y + size)
        elif y > 0 and y + size == N:
            return check_rectangle(board, x-1, y-1, x+1, y + size)
        elif y > 0 and y + size + 1 <= N:
            return check_rectangle(board, x-1, y-1, x+1, y + size)
    return False


def horizontal_surroundings_validation(board, x, y, size):
    if x + size > N or x < 0:
        return False
    if y == 0:
        if x == 0 and x + size + 1 <= N:
            return check_rectangle(board, x, y, x+size, y+1)
        elif x > 0 and x + size == N:
            return check_rectangle(board, x-1, y, x+size, y+1)
        elif x > 0 and x + size + 1 <= N:
            return check_rectangle(board, x-1, y, x+size, y+1)
    else:
        if x == 0 and x + size + 1 <= N:
            return check_rectangle(board, x, y-1, x+size, y+1)
        elif x > 0 and x + size == N:
            return check_rectangle(board, x-1, y-1, x+size, y+1)
        elif x > 0 and x + size + 1 <= N:
            return check_rectangle(board, x-1, y-1, x+size, y+1)
    return False


def check_rectangle(board, x1, y1, x2, y2):
    for i in range(x1, min(x2+1, N)):
        for j in range(y1, min(y2+1, N)):
            if board[j][i] != ' ':
                return False
    return True


def place_vertical_ship(board, x, y, size, is_last, user):
    for index in range(y, y + size):
        board[index][x] = '*'
    if (not is_last) and user == USER:
        print('Your current board:')
        print_board(board, user)
    return board


def place_side_ship(board, x, y, size, is_last, user):
    for index in range(x, x + size):
        board[y][index] = '*'
    if (not is_last) and user == USER:
        print('Your current board:')
        print_board(board, user)
    return board


def coordinates_retry(board, size, is_last):
    print('ERROR: Invalid location')
    message = 'Please enter location for Battleship of size {} again:'
    print(message.format(size))
    loc = str(input()).split(',')
    x = int(loc[0])
    y = int(loc[1][:-2])
    side = str(loc[1][-1])
    return validate_and_place(board, x, y, side, size, is_last, USER)


def game_manager(boards, user_b, comp_b, user_drw, comp_drw):
    while not (user_drw == N or comp_drw == N):
        [comp_b, user_drw, u_succ] = user_turn(boards[1], user_drw, False)
        [user_b, comp_drw, c_succ] = comp_turn(boards[0], comp_drw, False)
        if u_succ:
            print("The computer's battleship has been drowned.")
            print('{}/10 battleships remain!'.format(N - user_drw))
        if c_succ:
            print("Your battleship has been drowned.")
            print('{}/10 battleships remain!'.format(N - comp_drw))
        if user_drw == N or comp_drw == N:
            return [user_drw == N, comp_drw == N]
        print('Your following table:')
        print_board(comp_b, COMPUTER)
        print("The computer's following table:")
        print_board(user_b, USER)


def is_digit(x1, x2):
    try:
        int(x1)
        int(x2)
        return True
    except:
        return False

def address_getter():
    adress = EMPTY
    while adress == EMPTY:
        try:
            adress = input()
        except EOFError:
            print("EOFError")
            break
    adress = adress.split(',')
    if is_digit(adress[0], adress[1]):
        x1 = int(adress[1])
        x2 = int(adress[0])
        while x1 < 0 or x2 > N or x2 < 0 or x2 > N:
            print("Error: Invalid attack...\nPlease try again:")
            return address_getter()
        return [x1, x2]


def user_turn(target_b, drowned, succeed):
    print("It's your turn!\nEnter location for attack:")
    address = address_getter()
    x1 = address[0]
    x2 = address[1]
    if SHIP_MARK in target_b[x1][x2]:
        target_b[x1][x2] = HIT_MARK
        if drw(target_b, x1, x2):
            drowned += 1
            succeed = True
    else:
        target_b[x1][x2] = MISS_MARK
    return [target_b, drowned, succeed]


def comp_turn(target_b, drowned, succeed):
    loc = computer_attack_generator(target_b)
    if SHIP_MARK in target_b[int(loc[0])][int(loc[1])]:
        target_b[int(loc[0])][int(loc[1])] = HIT_MARK
        if drw(target_b, int(loc[0]), int(loc[1])):
            drowned += 1
            succeed = True
    else:
        target_b[int(loc[0])][int(loc[1])] = MISS_MARK
    return [target_b, drowned, succeed]


def computer_attack_generator(board):
    y = random.randint(0, N-1)
    x = random.randint(0, N-1)
    while board[x][y] == HIT_MARK or board[x][y] == MISS_MARK:
        y = random.randint(0, N - 1)
        x = random.randint(0, N - 1)
    return [x, y]


def surrounders(brd, i, j):
    for m in range(max(i - 1, 0), min(i + 2, N)):  # row
        for n in range(max(j - 1, 0), min(j + 2, N)):  # col
            if brd[m][n] == SHIP_MARK:
                return False
    return True


def recursion_checker():



def drw(brd, y, x, rec=False):
    tmp = True
    if rec:
        sur = True
        for i in range(max(y-1, 0), min(y+2, N)):  #row
            for j in range(max(x-1, 0), min(x + 2, N)): #col
                if brd[i][j] == SHIP_MARK:
                    return False
                if brd[i][j] == HIT_MARK and (j != x or i != y):
                    if not surrounders(brd, i, j):
                        return False
                    # sur = surrounders(brd, i, j)
                    # if not sur:
                    #     return False
        return True
    for i in range(max(y-1, 0), min(y+2, N)):  #y
        for j in range(max(x-1, 0), min(x + 2, N)): #x
            if brd[i][j] == SHIP_MARK:
                return False
            if brd[i][j] == HIT_MARK and (j != x or i != y):
                tmp = drw(brd, i, j, True)
                if not tmp:
                    return False
    return True and tmp

def first_part():
    print('Your current board:')
    user_board = initialize_and_set_board(USER)
    print('Your following table:')
    computer_board = initialize_and_set_board(COMPUTER)
    print_board(computer_board, COMPUTER)
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
    user_play_board = board_generator()
    comp_play_board = board_generator()
    results = game_manager(boards, user_play_board, comp_play_board, 0, 0)
    if results[0]:
        print("Congrats! You are the winner :)")
    else:
        print("Game over! The computer won the fight :(")


if __name__ == '__main__':
    main()