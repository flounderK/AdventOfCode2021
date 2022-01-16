#!/usr/bin/env python3
import argparse
import re
import functools
from collections import defaultdict
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default="input.txt")
args = parser.parse_args()

with open(args.file, "r") as f:
    data = [int(i) for i in f.read().split(',')]

NEWBORN_TIMER = 8

fish = data.copy()


def slow_tick(fish):
    new_fish = []
    for i in range(0, len(fish)):
        if fish[i] == 0:
            new_fish.append(NEWBORN_TIMER)
            fish[i] = 6
        else:
            fish[i] -= 1

    fish.extend(new_fish)


def math_tick(fish, turns=80):
    """Track by generations rather than individual fish"""
    tickno = 0
    newly_created_fish = 0
    newly_created_fish_batches = defaultdict(functools.partial(int, 0))
    generations = turns // 7
    for i in fish:
        # num_created = int((turns / 7) - ((i+1) / 7))
        newly_created_fish_batches[i] += int((turns / 7) - ((i+1) / 7))

    for g in range(generations+1):
        keys = list(newly_created_fish_batches.keys())
        for i in keys:
            newly_created_fish_batches[i+9] += int(((turns - 9) / 7) - ((i+1) / 7))
        print(f"gen {g} {sum(newly_created_fish_batches.values())}")

    return newly_created_fish_batches


for i in range(80):
    slow_tick(fish)

print(f"part 1 Fish: {len(fish)}")

fish2 = data.copy()
a = math_tick(fish2, 80)
# for i in range(256):
#     slow_tick(fish2)
#
# print(f"part 2 Fish: {len(fish2)}")


