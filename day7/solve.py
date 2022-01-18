#!/usr/bin/env python3
import argparse
import re
from collections import defaultdict
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default="input.txt")
args = parser.parse_args()

with open(args.file, "r") as f:
    data = [int(i) for i in f.read().split(',')]

positions = defaultdict(lambda: 0)
for i in data:
    positions[i] += 1

sorted_positions = sorted(positions.items(),
                          key=lambda a: a[1],
                          reverse=True)

# lowest_cost_position = sorted_positions[0][0]

costs = defaultdict(lambda: 0)
costs_p2 = defaultdict(lambda: 0)
largest = max(data)
total_cost = 0
for i in range(largest):
    for k, v in sorted_positions:
        if k == i:
            cost_diff = 0
            cost_diff_p2 = 0
        else:
            cost_diff = abs(k - i)
            # just the triangle sum of the p1 answer
            cost_diff_p2 = int((cost_diff*(cost_diff+1))/2)
        position_total_cost = (v*cost_diff)
        position_total_cost_p2 = (v*cost_diff_p2)
        costs[i] += position_total_cost
        costs_p2[i] += position_total_cost_p2
        # total_cost += (v*cost_diff)


cost_sorted_positions = sorted(costs.items(),
                               key=lambda a: a[1])

cost_sorted_positions_p2 = sorted(costs_p2.items(),
                                  key=lambda a: a[1])

for i in range(3):
    print(f"{cost_sorted_positions[i][0]}")


print(f"part 1 {cost_sorted_positions[0][1]}")
print(f"part 2 {cost_sorted_positions_p2[0][1]}")

