#!/usr/bin/env python3
import argparse
import re
from collections import defaultdict, namedtuple, deque
import math
import enum
import string

ReplacementPlan = namedtuple("ReplacementPlan", ['pattern', 'replacement', 'match'])

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default="input.txt")
args = parser.parse_args()

with open(args.file, "r") as f:
    data_lines = f.read().splitlines()
    polymer_template = data_lines[0]
    rules_raw = "\n".join(data_lines[1:])
    rules = [i.groups()
             for i in re.finditer(r'([a-zA-Z]+) -> ([a-zA-Z]+)',
                                  rules_raw)]

original_polymer_template = polymer_template

COMPILED_REXPS = {a: (re.compile(r'(?=(%s))' % a)) for a, _ in rules}

def do_replacement_step(polymer_template, rules):
    replacements = []
    for pattern, ins in rules:
        replacement = pattern[:1] + ins + pattern[1:]
        # hacky regex to capture a match, but keep the match length to 0
        # so that there aren't any overlapping matches anymore
        matches = list(re.finditer(COMPILED_REXPS[pattern], polymer_template))
        for i in matches:
            replacements.append(ReplacementPlan(pattern, replacement, i))

    # sort the list by the start position, reverse the list
    replacements.sort(key=lambda r: r.match.start(), reverse=True)

    for plan in replacements:
        start = plan.match.start()
        end = start + len(plan.pattern)
        lineend = polymer_template[end:]
        linestart = polymer_template[:start]
        # print(f"{linestart} ({plan.pattern} -> {plan.replacement}) {lineend}")
        polymer_template = linestart + plan.replacement + lineend

    return polymer_template


for _ in range(10):
    polymer_template = do_replacement_step(polymer_template, rules)

countdict = defaultdict(lambda: 0)
for i in polymer_template:
    countdict[i] += 1

element_count = list(countdict.values())
element_count.sort()
part1_res = element_count[-1] - element_count[0]
print(f"part 1 {part1_res}")


for _ in range(30):
    print("tick")
    polymer_template = do_replacement_step(polymer_template, rules)

element_count = list(countdict.values())
element_count.sort()
part1_res = element_count[-1] - element_count[0]
print(f"part 2 {part1_res}")

