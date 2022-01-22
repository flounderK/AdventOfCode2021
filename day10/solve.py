#!/usr/bin/env python3
import argparse
import re
from collections import defaultdict, namedtuple
import math
import enum


class Enclosure(enum.Enum):
    NONE = 0
    BRACKET = 1
    BRACE = 2
    PARENTHESIS = 3
    SQUEEZE = 4


ENCLOSURE_MAP = {'{': Enclosure.BRACKET,
                 '}': Enclosure.BRACKET,
                 '[': Enclosure.BRACE,
                 ']': Enclosure.BRACE,
                 '(': Enclosure.PARENTHESIS,
                 ')': Enclosure.PARENTHESIS,
                 '<': Enclosure.SQUEEZE,
                 '>': Enclosure.SQUEEZE}

CLOSE_MAP = {Enclosure.SQUEEZE: '>',
             Enclosure.BRACE: ']',
             Enclosure.PARENTHESIS: ')',
             Enclosure.BRACKET: '}',
             Enclosure.NONE: 'ERROR'}

OPEN_MAP = {Enclosure.SQUEEZE: '<',
            Enclosure.BRACE: '[',
            Enclosure.PARENTHESIS: '(',
            Enclosure.BRACKET: '{',
            Enclosure.NONE: 'ERROR'}
OPEN_SET = set('{([<')
CLOSE_SET = set('})]>')


def process_line(line):
    counts = {Enclosure.SQUEEZE: 0,
              Enclosure.BRACE: 0,
              Enclosure.PARENTHESIS: 0,
              Enclosure.BRACKET: 0}

    stack = []
    for i, c in enumerate(line):
        encl_type = ENCLOSURE_MAP[c]
        popped = Enclosure.NONE
        if c in OPEN_SET:
            counts[encl_type] += 1
            stack.append(encl_type)
        elif c in CLOSE_SET:
            counts[encl_type] -= 1
            popped = stack.pop()

        # Closed out of order
        if popped != Enclosure.NONE and encl_type != popped:
            expected = CLOSE_MAP[popped]
            print(f"Expected {expected} but found {c} instead: {i}")
            return (expected, c, i)

    newline = line
    # past here, error checking found no errors
    while stack:
        newline += CLOSE_MAP[stack.pop()]
    return newline


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default="input.txt")
args = parser.parse_args()

with open(args.file, "r") as f:
    data = [i for i in f.read().splitlines()]


errors = []
finished_entries = []
for i, line in enumerate(data):
    v = process_line(line)
    if isinstance(v, tuple):
        errors.append((i, v))
    elif isinstance(v, str):
        finished_entries.append((i, v))

