from random import randint


def play(board):

    while sum(board) != 0:
        diceone = randint(1, 6)
        dicetwo = randint(1, 6)

        total = diceone + dicetwo

        my_list = [diceone, dicetwo, total]

        # ao. koodi tutkii
        # if 1 in my_list:
        #     return 1
        # else:
        #     return 0

        if total == 7 or total == 8 or total == 9 and total in board:
            board[total - 1] = 0

        elif diceone in board or dicetwo in board or total in board:
            if board[0] in my_list:
                board[0] = 0
            elif board[1] in my_list:
                board[1] = 0
            elif board[2] in my_list:
                board[2] = 0
            elif board[3] in my_list:
                board[3] = 0
            elif board[4] in my_list:
                board[4] = 0
            elif board[5] in my_list:
                board[5] = 0

        else:
            return 0
    return 1


lost = 0
won = 0
n = 1000000

for game in range(n):

    print(f'game number {game}')
    board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    result = play(board)

    if result == 0:
        lost += 1
    else:
        won += 1

print(f'game was won {won} times and lost {lost} times')






