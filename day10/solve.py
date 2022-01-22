#!/usr/bin/env python3
import argparse
import re
from collections import defaultdict, namedtuple
import math
import enum


class Chunk(enum.Enum):
    BRACE = 1
    BRACKET = 2
    PARENTHESIS = 3


def process_subsystem(line):
    brace = 0
    parenth = 0
    bracket = 0

    starting_chunk_type = None
    open_brackets = []

    for i, c in enumerate(line):
        incorrect_pair = False
        closing_chunk = False
        if starting_chunk_type is None:
            starting_chunk_type = c

        popped = ''
        if c == '(':
            parenth += 1
            open_brackets.append(c)
        elif c == '{':
            bracket += 1
            open_brackets.append(c)
        elif c == '[':
            brace += 1
            open_brackets.append(c)
        elif c == ')':
            parenth -= 1
            popped = open_brackets.pop()
        elif c == '}':
            bracket -= 1
            popped = open_brackets.pop()
        elif c == ']':
            brace -= 1
            popped = open_brackets.pop()

        if brace < 0 or parenth < 0 or bracket < 0:
            print(f"underflow Expected {starting_chunk_type}, but found {c} instead.")
            return (c, i)

        expected = None
        if (popped == '{' and c != '}') or (popped not in ['{', ''] and c == '}'):
            incorrect_pair = True
        elif (popped == '(' and c != ')') or (popped not in ['(', ''] and c == ')'):
            incorrect_pair = True
        if (popped == '[' and c != ']') or (popped not in ['[', ''] and c == ']'):
            incorrect_pair = True

        if incorrect_pair is True:
            print(f"expected {popped}")

        if closing_chunk is True and any([x > 0 for x in [brace, parenth, bracket]]):
            # print(f"brace {brace}, parenth {parenth}, bracket {bracket}")
            # print(f"extra Expected {starting_chunk_type}, but found {c} instead.")
            print(f"extra found {c} instead.")
            return (c, i)



    print(f"brace {brace}, parenth {parenth}, bracket {bracket}")
    if starting_chunk_type is not None or any([brace, parenth, bracket]):
        # print(f"end Expected {starting_chunk_type}, but found {c} instead.")
        print(f"brace {brace}, parenth {parenth}, bracket {bracket}")
        print(f"end extra value found {c}")



parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default="input.txt")
args = parser.parse_args()

with open(args.file, "r") as f:
    data = [i for i in f.read().splitlines()]


for s, i in enumerate(data):
    print(s)
    process_subsystem(i)
    print("")

