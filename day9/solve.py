#!/usr/bin/env python3
import argparse
import re
from collections import defaultdict, namedtuple
import math
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default="input.txt")
args = parser.parse_args()

with open(args.file, "r") as f:
    data = [[int(k) for k in list(i)] for i in f.read().splitlines()]


CoordData = namedtuple("CoordData", ["height", "x", "y", "adjacent",
                                     "up", "down", "left", "right"])

# store a map of all of the values in the grid
coord_data = []
coord_data_map = {}
num_rows = len(data)
num_cols = len(data[0])
for y in range(0, len(data)):
    for x in range(0, num_cols):
        adjacent = []
        up = None
        down = None
        left = None
        right = None
        if y-1 >= 0:
            up = data[y-1][x]
            adjacent.append((x, y-1))
        if y+1 < num_rows:
            down = data[y+1][x]
            adjacent.append((x, y+1))
        if x-1 >= 0:
            left = data[y][x-1]
            adjacent.append((x-1, y))
        if x+1 < num_cols:
            right = data[y][x+1]
            adjacent.append((x+1, y))
        d = CoordData(data[y][x], x, y, tuple(adjacent), up, down, left, right)
        coord_data_map[(x, y)] = d
        coord_data.append(d)


def is_low_point(coord):
    for i in ['up', 'down', 'left', 'right']:
        v = getattr(coord, i)
        if v is not None and coord.height >= v:
            return False
    return True


def get_basin_for(coord, coord_data_map):
    # known points that are part of the basin
    basin_points = set()
    already_processed = set()
    already_processed.add(coord)
    # points that are adjacent to a known basin point
    basin_points_to_process = [coord]
    while len(basin_points_to_process) > 0:
        p = basin_points_to_process.pop()
        already_processed.add(p)
        if p.height == 9:
            continue
        basin_points.add(p)
        for v in p.adjacent:
            c = coord_data_map[v]
            if c in already_processed:
                continue
            basin_points_to_process.append(c)

    return list(basin_points)


for i in coord_data:
    assert i.height is not None
    assert i.height < 10 and i.height >= 0
    assert i.x >= 0 and i.x < num_cols
    assert i.y >= 0 and i.y < num_rows
    assert i.count(None) < 3

low_points = [i for i in coord_data if is_low_point(i)]

risk_level_sum = sum([i.height+1 for i in low_points])

print(f"part 1 {risk_level_sum}")


basin_lens = [len(get_basin_for(l, coord_data_map)) for l in low_points]

basin_lens.sort(reverse=True)
top3 = basin_lens[:3]
print(f"part 2 {math.prod(top3)}")

