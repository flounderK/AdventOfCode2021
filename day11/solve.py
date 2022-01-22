#!/usr/bin/env python3
import argparse
import re
from collections import defaultdict, namedtuple
import math


class CoordData:
    # default directions
    DIRECTIONS = ['upleft', 'up', 'upright',
                  'down', 'downleft', 'downright',
                  'left', 'right']

    def __init__(self, grid, direction_list=None):
        self.grid = grid
        if direction_list is None:
            self.direction_list = self.DIRECTIONS
        else:
            self.direction_list = direction_list
        self.num_rows = num_rows = len(data)
        self.num_cols = num_cols = len(data[0])
        self.COORD_DATA_LIST = []
        self.COORD_DATA_MAP = {}
        for y in range(0, len(data)):
            for x in range(0, num_cols):

                adjacent = []
                directions = {i: None for i in self.direction_list}
                # up
                if y-1 >= 0 and 'up' in self.direction_list:
                    directions['up'] = grid[y-1][x]
                    adjacent.append((x, y-1))
                if y-1 >= 0 and x-1 >= 0 and \
                   'upleft' in self.direction_list:
                    directions['upleft'] = grid[y-1][x-1]
                    adjacent.append((x-1, y-1))
                if y-1 >= 0 and x+1 < num_cols and \
                   'upright' in self.direction_list:
                    directions['upright'] = grid[y-1][x+1]
                    adjacent.append((x+1, y-1))

                # down
                if y+1 < num_rows and \
                   'down' in self.direction_list:
                    directions['down'] = grid[y+1][x]
                    adjacent.append((x, y+1))
                if y+1 < num_rows and x-1 >= 0 and \
                   'downleft' in self.direction_list:
                    directions['downleft'] = grid[y+1][x-1]
                    adjacent.append((x-1, y+1))
                if y+1 < num_rows and x+1 < num_cols and \
                   'downright' in self.direction_list:
                    directions['downright'] = grid[y+1][x+1]
                    adjacent.append((x+1, y+1))

                # left and right
                if x-1 >= 0 and \
                   'left' in self.direction_list:
                    directions['left'] = grid[y][x-1]
                    adjacent.append((x-1, y))
                if x+1 < num_cols and \
                   'right' in self.direction_list:
                    directions['right'] = grid[y][x+1]
                    adjacent.append((x+1, y))

                adjacent = tuple(adjacent)
                value = grid[y][x]
                d = Coord(x, y, value, directions, adjacent)
                self.COORD_DATA_MAP[(x, y)] = d
                self.COORD_DATA_LIST.append(d)

    def get_basin_for(self, coord):
        # known points that are part of the basin
        basin_points = set()
        already_processed = set()
        already_processed.add(coord)
        # points that are adjacent to a known basin point
        basin_points_to_process = [coord]
        while len(basin_points_to_process) > 0:
            p = basin_points_to_process.pop()
            already_processed.add(p)
            if p.value == 9:
                continue
            basin_points.add(p)
            for v in p.adjacent:
                c = self.COORD_DATA_MAP[v]
                if c in already_processed:
                    continue
                basin_points_to_process.append(c)

        return list(basin_points)

    def print_with_marks(self, coords):
        for y in range(0, self.num_rows):
            for x in range(0, self.num_cols):
                c = self.COORD_DATA_MAP[(x, y)]
                if c in coords:
                    print('*', end='')
                else:
                    print('.', end='')
            print("")
        print("")

    def print(self):
        for y in range(0, self.num_rows):
            for x in range(0, self.num_cols):
                c = self.COORD_DATA_MAP[(x, y)]
                print('%d' % c.value, end='')
            print("")
        print("")


class Coord:

    def __init__(self, x, y, value, directions, adjacent):
        self.x = x
        self.y = y
        self.value = value
        self._directions = directions
        self.adjacent = adjacent
        for k, v in directions.items():
            setattr(self, k, v)

    def is_high_point(self):
        for i in self._directions.keys():
            v = getattr(self, i)
            if v is not None and self.value < v:
                return False
        return True

    def is_low_point(self):
        for i in self._directions.keys():
            v = getattr(self, i)
            if v is not None and self.value >= v:
                return False
        return True

    def __repr__(self):
        return f"CoordData({self.value})"


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default="input.txt")
args = parser.parse_args()

with open(args.file, "r") as f:
    data = [[int(k) for k in list(i)] for i in f.read().splitlines()]


# store a map of all of the values in the grid
grid = CoordData(data)

low_points = [i for i in grid.COORD_DATA_LIST if i.is_low_point()]
for i in low_points:
    grid.print_with_marks(grid.get_basin_for(i))
