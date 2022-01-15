#!/usr/bin/env python3
import argparse
import re
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default="input.txt")
args = parser.parse_args()

rexp = re.compile(r"(?P<DIRECTION>[^\s]+)\s+(?P<VALUE>\d+)")
with open(args.file, "r") as f:
    data = [re.search(rexp, i).groups() for i in f.read().splitlines()]


data = [(a, int(b)) for a, b in data]


horiz_pos = 0
depth = 0

for a, b in data:
    if a == 'forward':
        horiz_pos += b
    elif a == 'up':
        depth -= b
    elif a == 'down':
        depth += b

print(f"part 1 {horiz_pos*depth}")


horiz_pos = 0
depth = 0
aim = 0


for a, b in data:
    if a == 'forward':
        horiz_pos += b
        depth += (aim*b)
    elif a == 'up':
        aim -= b
    elif a == 'down':
        aim += b

print(f"part 2 {horiz_pos*depth}")
