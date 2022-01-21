#!/usr/bin/env python3
import argparse
import re
from collections import defaultdict, namedtuple
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default="input.txt")
args = parser.parse_args()

with open(args.file, "r") as f:
    data = [[int(k) for k in list(i)] for i in f.read().splitlines()]


CoordData = namedtuple("CoordData", ["height", "x", "y",
                                     "up", "down", "left", "right"])

# store a map of all of the values in the grid
coord_data = []
num_rows = len(data)
num_cols = len(data[0])
for y in range(0, len(data)):
    for x in range(0, num_cols):
        up = data[y-1][x] if y-1 >= 0 else None
        down = data[y+1][x] if y+1 < num_rows else None
        left = data[y][x-1] if x-1 >= 0 else None
        right = data[y][x+1] if x+1 < num_cols else None
        d = CoordData(data[y][x], x, y, up, down, left, right)
        coord_data.append(d)


def is_low_point(coord):
    for i in ['up', 'down', 'left', 'right']:
        v = getattr(coord, i)
        if v is not None and coord.height >= v:
            return False
    return True


for i in coord_data:
    assert i.height is not None
    assert i.height < 10 and i.height >= 0
    assert i.x >= 0 and i.x < num_cols
    assert i.y >= 0 and i.y < num_rows
    assert i.count(None) < 3

low_points = [i for i in coord_data if is_low_point(i)]

risk_level_sum = sum([i.height+1 for i in low_points])

print(f"part 1 {risk_level_sum}")
