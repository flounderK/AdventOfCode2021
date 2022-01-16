#!/usr/bin/env python3
import argparse
import re
import itertools
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default="input.txt")
args = parser.parse_args()

with open(args.file, "r") as f:
    raw_data = f.read()

split_raw_data = raw_data.split('\n\n')
numbers = [int(i) for i in split_raw_data[0].split(',')]
boards_raw = [i.strip() for i in split_raw_data[1:]]

boards = []

for board in boards_raw:
    board_vals = [int(i[0]) for i in re.finditer(r'\d+', board)]
    # split board values into groups of 5
    split_board = list(zip(*(iter(board_vals),)*5))
    boards.append(split_board)


def is_winning_diagonal(board, numbers_called):
    win = True
    for i in range(0, len(board[0])):
        if board[i][i] not in numbers_called:
            win = False
            break
    return win


def is_winning_row(board, numbers_called):
    for row in board:
        win = True
        for val in row:
            if val not in numbers_called:
                win = False
                break
        if win is True:
            return True
    return False


def is_winning_board(board, numbers_called):
    if len(numbers_called) < len(board[0]):
        return False

    # whoops, I guess diagonals aren't included
    # if is_winning_diagonal(board, numbers_called) is True:
    #     print("win on top left to bottom right diag")
    #     return True

    # if is_winning_diagonal(board[::-1], numbers_called) is True:
    #     print("win on bottom left to top right diag")
    #     return True

    if is_winning_row(board, numbers_called) is True:
        print("win on row")
        return True

    inverted_board = list(zip(*board))
    if is_winning_row(inverted_board, numbers_called) is True:
        print("win on column")
        return True


def get_unmarked_numbers(board, numbers):
    board = board.copy()
    board_vals = list(itertools.chain(*board))
    for i in numbers:
        if i in board_vals:
            board_vals.remove(i)
    return board_vals


result = 0
part1_result = 0
part2_result = 0
won_boards = set()
board_won = False
part2_board_won = False
for i in range(5, len(numbers)):
    print(f"number {i}")
    for ind, board in enumerate(boards):
        if is_winning_board(board, numbers[:i]) is True:
            print(f"winning board {ind+1}: {numbers[:i]}")
            unmarked_numbers = get_unmarked_numbers(board, numbers[:i])
            last_called = numbers[:i][-1]
            result = sum(unmarked_numbers)
            print(f"unmarked sum {result}")
            result = result*last_called
            won_boards.add(ind)
            print(f"won boards {won_boards}")
            # first win
            if board_won is False:
                part1_result = result

            if len(boards) == len(won_boards):
                part2_result = result
                part2_board_won = True
                break

            board_won = True
    if part2_board_won is True:
        break
    print("")

print(f"part 1 {part1_result}")
print(f"part 2 {part2_result}")
