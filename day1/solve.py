#!/usr/bin/env python3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default="input.txt")
args = parser.parse_args()

with open(args.file, "r") as f:
    data = [int(i) for i in f.read().splitlines()]


def get_increases(data, initial_increase=-1):
    total_increases = initial_increase
    last = 0
    for i in data:
        if i > last:
            total_increases += 1
        last = i
    return total_increases


# -1 because the first value gets no increase
total_increases = get_increases(data)

print(f"part 1 increases {total_increases}")

group_size = 3

sliding_window_data = data

sums = []

for i in range(0, len(data)):
    vals = data[i:i+group_size]
    if len(vals) == group_size:
        sums.append(sum(vals))

sliding_window_increases = get_increases(sums)

print(f"part2 {sliding_window_increases}")
