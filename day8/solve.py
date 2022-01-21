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
# len, val
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


five_segment_digits = [2, 3, 5]
six_segment_digits = [6, 9, 0]
known_standard_trans = {'acdfg': 3,
                        'acdeg': 2,
                        'abdfg': 5,
                        'abcefg': 0,
                        'abdefg': 6,
                        'abcdfg': 9}

"""
standard
 aaaa
b    c
b    c
 dddd
e    f
e    f
 gggg
"""
# standard, current
segment_translations = {}

easy_digits_keys = list(easy_digits_by_count.keys())
by_seg_len = defaultdict(str)
incompletes = 0

def get_trans(inp, out):
    trans = {}
    five_seg_entries = set()
    six_seg_entries = set()
    completed_values = set()
    # initial processing, get the easy digits
    for i in inp:
        length = len(i)
        v = easy_digits_by_count.get(length)
        if v is not None:
            trans[i] = v
            completed_values.add(v)
        if length == 5:
            five_seg_entries.add(i)
        if length == 6:
            six_seg_entries.add(i)
        by_seg_len[length] = i

    # try to find right line_intersect from (1, 4, 7)
    for a, b in itertools.combinations([2, 4, 3], 2):
        right_line_intersect = set(by_seg_len[a]).intersection(by_seg_len[b])
        if len(right_line_intersect) > 0:
            break

    # get 6 and 3 if present
    for i in inp:
        length = len(i)
        is_superset_of_right = set(i).issuperset(right_line_intersect)
        if length == 6 and not is_superset_of_right:
            trans[i] = 6
            completed_values.add(6)
            continue
        if length == 5 and is_superset_of_right:
            trans[i] = 3
            completed_values.add(3)
            continue

    # the left half of 4
    bd = set(by_seg_len[4]).symmetric_difference(right_line_intersect)
    for i in five_seg_entries:
        if set(i).issuperset(bd):
            trans[i] = 5
            completed_values.add(5)

    for i in six_seg_entries:
        if not set(i).issuperset(bd):
            trans[i] = 0
            completed_values.add(0)

    # get remaining 2 by process of elimination
    if 3 in completed_values and 5 in completed_values:
        two_key = [i for i in five_seg_entries if i not in trans.keys()]
        if len(two_key) > 0:
            trans[two_key[0]] = 2
            completed_values.add(2)

    # get remaining 9 by process of elimination
    if 6 in completed_values and 0 in completed_values:
        key = [i for i in six_seg_entries if i not in trans.keys()]
        if len(key) > 0:
            trans[key[0]] = 9
            completed_values.add(9)
    missing_out = 0
    for i in out:
        iset = set(i)
        if not any(iset == set(k) for k in trans.keys()):
            missing_out += 1
    # print(f"out: {len(out)-missing_out}/{len(out)} in: {len(set(completed_values))}/{len(set(inp))} ")
    return trans


def translate(out, trans):
    trans_set = [(set(k), v) for k, v in trans.items()]
    found = []
    for s, i in enumerate(out):
        iset = set(i)
        for k, v in trans_set:
            if iset == k:
                found.append(v)
                break
    return found


results = []
for inp, out in data:
    trans = get_trans(inp, out)
    result_digits = translate(out, trans)
    value = int(''.join("%d" % i for i in result_digits))
    results.append(value)


print(f"part 2 {sum(results)}")
