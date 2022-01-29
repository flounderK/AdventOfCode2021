#!/usr/bin/env python3
import argparse
import re
from collections import defaultdict, namedtuple, deque
import math
import enum
import string


class CaveSize(enum.Enum):
    SMALL = 0
    LARGE = 1


class CaveNode:
    """Instance caching class"""
    _INST_MAP = {}

    def __new__(cls, name, **kwargs):
        inst = cls._INST_MAP.get(name)
        if inst is None:
            cls._INST_MAP[name] = super(CaveNode, cls).__new__(cls)
        return cls._INST_MAP[name]

    def __init__(self, name):
        self.name = name
        if name[0] in string.ascii_lowercase:
            self.size = CaveSize.SMALL
        elif name[0] in string.ascii_uppercase:
            self.size = CaveSize.LARGE

    def __repr__(self):
        return self.name


class CaveSystem:
    def __init__(self, data, allowed_visits=1):
        self._data = data.copy()
        self.parent_map = defaultdict(list)
        self.child_map = defaultdict(list)
        self.all_paths_map = defaultdict(set)
        self.all_nodes = set()
        self.allowed_small_cave_visits = allowed_visits
        self._null_cave = CaveNode("NULL")
        for k, v in data:
            frm = CaveNode(k)
            to = CaveNode(v)
            self.parent_map[frm].append(to)
            self.child_map[to].append(frm)
            self.all_paths_map[frm].add(to)
            self.all_paths_map[to].add(frm)
            self.all_nodes.add(frm)
            self.all_nodes.add(to)
        self.endpoints = set([CaveNode('start'), CaveNode('end')])
        self.small_caves = [i for i in self.all_nodes if i not
                            in self.endpoints and i.size == CaveSize.SMALL]
        self.special_small_cave = self._null_cave

    def paths_to(self, start, end, path, all_paths):
        """Recursive dfs from start to end that hits all paths rather
        than ending on the first one"""
        # print(f"\nCave {start}:")

        # return if end found
        if start == end:
            # print(f"start == end {start} {end}")
            all_paths.append(path.copy())
            path.pop()
            return

        for c in self.all_paths_map[start]:
            # print(f"{start}->{c}")

            # skip path if it is small and has been used already
            numfound = path.count(c)
            if c.size == CaveSize.SMALL:
                if numfound >= 1 and c != self.special_small_cave:
                    continue
                # handling for special cave
                if (self.special_small_cave == c and numfound >= self.allowed_small_cave_visits):
                    continue

            path.append(c)

            self.paths_to(c, end, path, all_paths)

        # pop off last node
        path.pop()

    def get_special_cave_paths(self, start, end):
        all_paths = []
        for i in self.small_caves:
            path = [start]
            self.special_small_cave = i
            self.paths_to(start, end, path, all_paths)

        self.special_small_cave = self._null_cave
        all_paths = [list(i) for i in set(tuple(i) for i in all_paths)]
        return all_paths



parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default="input.txt")
args = parser.parse_args()

with open(args.file, "r") as f:
    data = [re.search(r'([a-zA-Z]+)-([a-zA-Z]+)', i)
            for i in f.read().splitlines()]

assert all(data)
data = [i.groups() for i in data if i is not None]


cave_system = CaveSystem(data)

start = CaveNode('start')
end = CaveNode('end')

path = [start]
all_paths = []
cave_system.paths_to(start, end, path, all_paths)

print(f"part 1: {len(all_paths)}")

cave_system2 = CaveSystem(data, 2)
all_paths = cave_system2.get_special_cave_paths(start, end)
print(f"part 2: {len(all_paths)}")


