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


def check_move(target_b, x, y):
    if target_b[x][y] == ' ':
        return False
    if target_b[x][y] == '*':
        return True


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
            return check_rectangle(board, x, y, x+1, y + size+1)
        elif y > 0 and y + size == N:
            return check_rectangle(board, x, y-1, x+1, y + size)
        elif y > 0 and y + size + 1 <= N:
            return check_rectangle(board, x, y-1, x+1, y + size+1)
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
            return check_rectangle(board, x, y, x+size+1, y+1)
        elif x > 0 and x + size == N:
            return check_rectangle(board, x-1, y, x+size, y+1)
        elif x > 0 and x + size + 1 <= N:
            return check_rectangle(board, x-1, y, x+size+1, y+1)
    else:
        if x == 0 and x + size + 1 <= N:
            return check_rectangle(board, x, y-1, x+size+1, y+1)
        elif x > 0 and x + size == N:
            return check_rectangle(board, x-1, y-1, x+size, y+1)
        elif x > 0 and x + size + 1 <= N:
            return check_rectangle(board, x-1, y-1, x+size+1, y+1)
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
    while not user_drw == N or comp_drw == N:
        [comp_b, user_drw] = user_turn(boards[1], user_drw)
        [user_b, comp_drw] = comp_turn(boards[0], comp_drw)
        print('Your following table:')
        print_board(comp_b, COMPUTER)
        print("The computer's following table:")
        print_board(user_b, USER)
        # game_manager(boards, user_b, comp_b, user_drw, comp_drw)


def user_turn(target_b, drowned):
    print("It's your turn!")
    print('Enter location for attack:')
    loc = str(input())[::-1].split(',')
    if check_move(target_b, int(loc[0]), int(loc[1])):
        target_b[int(loc[0])][int(loc[1])] = HIT_MARK
        if state_update(target_b, USER, int(loc[0]), int(loc[1])):
            drowned += 1
            print('{}/10 battleships remain!'.format(N - drowned))
    else:
        target_b[int(loc[0])][int(loc[1])] = MISS_MARK
    return [target_b, drowned]


def comp_turn(target_b, drowned):
    loc = computer_attack_generator(target_b)
    if loc == [2, 2]:
        pass
    if check_move(target_b, int(loc[0]), int(loc[1])):
        target_b[int(loc[0])][int(loc[1])] = HIT_MARK
        if state_update(target_b, COMPUTER, int(loc[0]), int(loc[1])):
            drowned += 1
            print('{}/10 battleships remain!'.format(N - drowned))
    else:
        target_b[int(loc[0])][int(loc[1])] = MISS_MARK
    return [target_b, drowned]


def computer_attack_generator(board):
    y = random.randint(0, N-1)
    x = random.randint(0, N-1)
    while board[x][y] == HIT_MARK or board[x][y] == MISS_MARK:
        y = random.randint(0, N - 1)
        x = random.randint(0, N - 1)
    return [x, y]


def state_update(board, player, x, y):
    if drw(board, x, y):
        if player % 2 == 0:
            print("The computer's battleship has been drowned.")
        else:
            print("Your battleship has been drowned.")
        return True


def drw(brd, x, y):
    for i in range(max(x-1, 0), min(x + 2, N)):
        for j in range(max(y-1, 0), min(y+2, N)):
            # if brd[i][j] == ' ':
            #     print('-', end='')
            # else:
            #     print(brd[i][j])
            if brd[i][j] == SHIP_MARK:
                return False
            if brd[i][j] == HIT_MARK and i != x and j != y:
                return drw(brd, i, j)
        # print()
    return True


    # try:
    #     # if * in surroundings
    #     s = [brd[x-1][y], brd[x+1][y], brd[x][y-1], brd[x][y+1]]
    #     if SHIP_MARK in s:
    #         return False
    #     # if all surroundings are X or empty
    #     if brd[x-1][y] == brd[x+1][y] == brd[x][y-1] == brd[x][y+1]:
    #         return True
    # except IndexError:
    #     if x-1 == 0:
    #         if brd[x-1][y] == SHIP_MARK:
    #             return False
    #         else:
    #             return drw(brd, x + 1, y)
    #     elif x+1 == N:
    #         if brd[x+1][y] == SHIP_MARK:
    #             return False
    #         else:
    #             return drw(brd, x - 1, y)
    #     if x - 1 >= 0 and x+1 <= N:
    #         if brd[x - 1][y] == brd[x + 1][y] == HIT_MARK:
    #             return drw(brd, x - 1, y) + drw(brd, x + 1, y)
    #         if brd[x - 1][y] == HIT_MARK:
    #             return drw(brd, x-2, y)
    #         if brd[x+1][y] == HIT_MARK:
    #             return drw(brd, x+2, y)
    #         if brd[x - 1][y] == SHIP_MARK or brd[x + 1][y] == SHIP_MARK:
    #             return False
    #     if y-1 == 0:
    #         if brd[x][y-1] == SHIP_MARK:
    #             return False
    #         else:
    #             return drw(brd, y + 1, x)
    #     elif y+1 == N:
    #         if brd[x][y+1] == SHIP_MARK:
    #             return False
    #         else:
    #             return drw(brd, y - 1, x)
    #     if y - 1 >= 0 and y+1 <= N:
    #         if brd[x][y - 1] == brd[x][y + 1] == HIT_MARK:
    #             return drw(brd, x, y - 1) + drw(brd,x, y + 1)
    #         if brd[x][y - 1] == HIT_MARK:
    #             return drw(brd, x, y-2)
    #         if brd[x][y+1] == HIT_MARK:
    #             return drw(brd, x, y+2)
    #         if brd[x][y - 1] == SHIP_MARK or brd[x][y + 1] == SHIP_MARK:
    #             return False
    #     return True

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
    game_manager(boards, user_play_board, comp_play_board, 0, 0)


if __name__ == '__main__':
    main()