#!/usr/bin/env python3
import argparse
import re
import string
import itertools
from collections import namedtuple
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default="input.txt")
args = parser.parse_args()

rexp = re.compile(r"(?P<x1>\d+),(?P<y1>\d+)\s+->\s+(?P<x2>\d+),(?P<y2>\d+)")
with open(args.file, "r") as f:
    data = [re.search(rexp, i).groups() for i in f.read().splitlines()]

Line = namedtuple('Line', ['x1', 'y1', 'x2', 'y2'])

data = [Line(*list(map(int, i))) for i in data]


def create_board(dim=10):
    row = ['.']*dim

    return [row.copy() for i in range(dim)]


def mark_line(board, line, diags=False):
    if line.x1 == line.x2:
        mn = min(line.y1, line.y2)
        mx = max(line.y1, line.y2)+1
        for y in range(mn, mx):

            existing_mark = board[y][line.x1]
            if existing_mark in string.digits:
                mark = str(int(existing_mark) + 1)
            elif existing_mark == '.':
                mark = '1'
            board[y][line.x1] = mark

    if line.y1 == line.y2:
        mn = min(line.x1, line.x2)
        mx = max(line.x1, line.x2)+1
        for x in range(mn, mx):
            existing_mark = board[line.y1][x]
            if existing_mark in string.digits:
                mark = str(int(existing_mark) + 1)
            elif existing_mark == '.':
                mark = '1'
            board[line.y1][x] = mark

    # diagonals
    if line.y1 != line.y2 and line.x1 != line.x2 and diags is True:
        xstep = 1
        ystep = 1
        neg_x = line.x1 > line.x2
        neg_y = line.y1 > line.y2
        # right to left, negative x
        if neg_x:
            # print("negative xstep")
            xstep = -1

        if neg_y:
            # print("negative ystep")
            ystep = -1
        # neg x and y is basically just a normal line,
        # so just swap all of the values to make it positive
        if neg_y and neg_x:
            neg_x = False
            neg_y = False
            xstep = 1
            ystep = 1
            line = line._replace(x1=line.x2,
                                 x2=line.x1,
                                 y1=line.y2,
                                 y2=line.y1)
        if neg_x:
            line = line._replace(x2=line.x2-1,
                                 y2=line.y2+1)
        else:
            line = line._replace(x2=line.x2+1)

        if neg_y:
            line = line._replace(y2=line.y2-1,
                                 x2=line.x2+1)
        else:
            line = line._replace(y2=line.y2+1)

        coords = list(zip(range(line.x1, line.x2, xstep),
                          range(line.y1, line.y2, ystep)))
        # for y in range(mny, mxy):
        #     for x in range(mnx, mxx):
        for x, y in coords:
            existing_mark = board[y][x]
            # print(f"{x}, {y}")
            if existing_mark in string.digits:
                mark = str(int(existing_mark) + 1)
            elif existing_mark == '.':
                mark = '1'
            else:
                print(f"existing mark wrong {existing_mark}")
                mark = '0'
            board[y][x] = mark


def print_board(board):
    print('\n'.join(''.join(i) for i in board))


board_size = 1000

board = create_board(board_size)

for i, line in enumerate(data):
    mark_line(board, line)

if board_size < 100:
    print_board(board)
board_vals = [i for i in list(itertools.chain(*board)) if i not in ['1', '.']]

print(f"\npart 1 {len(board_vals)}\n")

board = create_board(board_size)
for line in data:
    mark_line(board, line, True)

if board_size < 100:
    print_board(board)

board_vals = [i for i in list(itertools.chain(*board)) if i not in ['1', '.']]

print(f"\npart 2 {len(board_vals)}\n")
