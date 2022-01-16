#!/usr/bin/env python3
import argparse
import re
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default="input.txt")
args = parser.parse_args()

with open(args.file, "r") as f:
    data = [i for i in f.read().splitlines()]

gamma = ''
epsilon = ''
inverted_data = list(zip(*data))
num_entries = len(data)
half = num_entries // 2
oxygen_gen_data = data.copy()
co2_scrubber_data = data.copy()
oxy = ''
scrb = ''
equally_common = ''
for i in inverted_data:
    ones = i.count('1')
    if ones >= half:
        gamma += '1'
        epsilon += '0'
    else:
        gamma += '0'
        epsilon += '1'

    if ones == half:
        equally_common += '*'
    else:
        equally_common += '-'

gamma_val = int(gamma, 2)
epsilon_val = int(epsilon, 2)

print(f"part 1 {gamma_val*epsilon_val}")


def get_commonality(data, col, most=True):
    inverted_data = list(zip(*data))

    i = inverted_data[col]
    ones = i.count('1')
    zeroes = i.count('0')

    if ones == zeroes:
        return '*'
    elif ones > zeroes:
        most_common = '1'
        least_common = '0'
    elif ones < zeroes:
        most_common = '0'
        least_common = '1'

    return most_common if most is True else least_common


for i in range(0, len(gamma)):
    if len(oxygen_gen_data) > 1:
        matchval = get_commonality(oxygen_gen_data, i)
        if matchval == '*':
            matchval = '1'
        oxygen_gen_data = [o for o in oxygen_gen_data if o[i] == matchval]
    if len(co2_scrubber_data) > 1:
        matchval = get_commonality(co2_scrubber_data, i, False)
        if matchval == '*':
            matchval = '0'
        co2_scrubber_data = [o for o in co2_scrubber_data if o[i] == matchval]


co2_scrubber_rating = co2_scrubber_data[0]
oxygen_generator_rating = oxygen_gen_data[0]

print(f"part 2 {int(co2_scrubber_rating, 2)*int(oxygen_generator_rating, 2)}")
