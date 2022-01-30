#!/usr/bin/env python3
import argparse
import re
from collections import defaultdict, namedtuple
import math


class CoordData:

    def __init__(self, coord_list, grid_size):
        self.num_cols, self.num_rows = grid_size
        self.COORD_DATA_MAP = {(x, y): Coord(x, y, 0) for x, y in coord_list}
        self._null_coord = Coord(-1, -1, '.')

    def print_with_marks(self, coords):
        # make a new coord map that only contains the given coords,
        # so that the coords don't have to already be in the grid
        m = self.COORD_DATA_MAP.copy()
        for c in coords:
            m[(c.x, c.y)] = c
        for y in range(0, self.num_rows):
            for x in range(0, self.num_cols):
                c = m.get((x, y), self._null_coord)
                if c in coords:
                    print('*', end='')
                else:
                    print('.', end='')
            print("")
        print("")

    def print(self):
        for y in range(0, self.num_rows):
            for x in range(0, self.num_cols):
                c = self.COORD_DATA_MAP.get((x, y), self._null_coord)
                print(f'{c.value}', end='')
            print("")
        print("")

    def do_fold(self, geodesic, ind):
        to_remove_locs = []
        to_add = []
        for c in self.COORD_DATA_MAP.values():
            x = c.x
            y = c.y
            modified_coord = False
            if geodesic == 'y' and ind < c.y:
                modified_coord = True
                # remove the coordinate that is being reflected
                orig_occupant = self.COORD_DATA_MAP.get((x, y))
                if orig_occupant is not None:
                    to_remove_locs.append((x, y))
                c.y = y = ((c.y * -1)) + (ind*2)
            elif geodesic == 'x' and ind < c.x:
                modified_coord = True
                # remove the coordinate that is being reflected
                orig_occupant = self.COORD_DATA_MAP.get((x, y))
                if orig_occupant is not None:
                    to_remove_locs.append((x, y))
                c.x = x = ((c.x * -1)) + (ind*2)

            if modified_coord is True:
                to_add.append(c)

        # adjust the boundaries of the grid appropriately
        if geodesic == 'y':
            self.num_rows = ind
        elif geodesic == 'x':
            self.num_cols = ind

        # remove locations that have been folded away
        for x, y in to_remove_locs:
            self.COORD_DATA_MAP.pop((x, y))

        # add in the new coordinates
        for i in to_add:
            self.COORD_DATA_MAP[(i.x, i.y)] = i


class Coord:

    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

    def __repr__(self):
        return f"CoordData({self.value})"


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default="input.txt")
args = parser.parse_args()

coord_rexp = re.compile(r"(\d+),(\d+)")
fold_rexp = re.compile(r"fold along (.)=(\d+)")

with open(args.file, "r") as f:
    raw_content = f.read()

marked_positions = [(int(a), int(b)) for a, b in re.findall(coord_rexp, raw_content)]
fold_along = [(a, int(b)) for a, b in re.findall(fold_rexp, raw_content)]

y_size = ([i for i in fold_along if i[0] == 'y'][0][1]*2)+1
x_size = ([i for i in fold_along if i[0] == 'x'][0][1]*2)+1

grid = CoordData(marked_positions, (x_size, y_size))
grid.do_fold(*fold_along[0])

print(f"part 1: {len(grid.COORD_DATA_MAP)}")

for i in range(1, len(fold_along)):
    grid.do_fold(*fold_along[i])

print("part 2")

grid.print()
