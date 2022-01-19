#!/usr/bin/env python3
import argparse
import re
import itertools
from collections import defaultdict
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default="input.txt")
args = parser.parse_args()

rexp = re.compile(r'([a-g]+)')
with open(args.file, "r") as f:
    data_raw = [i.split('|') for i in f.read().splitlines()]
    f.seek(0)
    all_patterns = [i[0] for i in re.finditer(rexp, f.read())]

data = [(a.strip().split(' '), b.strip().split(' ')) for a, b in data_raw]

counts = defaultdict(lambda: 0)
easy_digits_by_count = {2: 1,
                        4: 4,
                        3: 7,
                        7: 8}

for inp, out in data:
    for i in out:
        counts[len(i)] += 1

total = 0
for k, v in counts.items():
    if k in easy_digits_by_count.keys():
        total += v

print(f"part 1 {total}")
