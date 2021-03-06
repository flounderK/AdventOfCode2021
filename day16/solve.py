#!/usr/bin/env python3
import argparse
import re
from collections import defaultdict, namedtuple
from math import prod
import ctypes
from ctypes import sizeof, memmove, byref, c_ubyte, c_ushort
from struct import unpack
import struct
import enum

known_type_ids = {0: 'SUM',
                  1: 'PRODUCT',
                  2: 'MINIMUM',
                  3: 'MAXIMUM',
                  4: 'LITERAL',
                  5: 'GREATER_THAN',
                  6: 'LESS_THAN',
                  7: 'EQUAL_TO'}
# make a quick enum for packet types
PacketTypeID = enum.IntEnum('PacketTypeID',
                            ' '.join(known_type_ids.get(i, 'T%X' % i)
                                     for i in range(0, 16)),
                            start=0)


def decode_literal(bs, step=5):
    """decodes bits from bitstream and returns
    the decoded value along with the total number of
    encoded bits that were used (excluding end padding)"""
    i = 0
    val = ''
    while True:
        more = bool(int(bs[i:i+1], 2))
        val += bs[i+1:i+step].decode()
        i += step
        if more is False:
            break

    return int(val, 2), i


def sum_version_numbers(packet):
    total = 0
    if isinstance(packet, dict):
        subpackets = packet.get('subpackets', [])
        total += packet['version']
    elif isinstance(packet, list):
        subpackets = packet
    for i in subpackets:
        total += sum_version_numbers(i)
    return total




parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default="input.txt")
args = parser.parse_args()

with open(args.file, "r") as f:
    raw_data = f.read()

data = bytes.fromhex(raw_data)

bitstream_string = ''.join(bin(i)[2:].rjust(8, '0') for i in data)
# make a mutable bitstream
bitstream = bytearray(bitstream_string.encode())


VERSION_SLICE = slice(0, 3)
TYPE_ID_SLICE = slice(3, 6)
LITERAL_SLICE = slice(6, None)  # until packet end
LENGTH_TYPE_ID_SLICE = slice(6, 7)

# if length type id is 0
TOTAL_LENGTH_IN_BITS_SLICE = slice(7, 22)

# if length type id is 1
NUM_SUBPACKETS_IMM_CONTD_SLICE = slice(7, 18)


def calc_padding_bits(consumed, align_to=8):
    # calculate number of 0's used for padding to
    # hex aligned values
    d, r = divmod(consumed, 8)
    if r == 0:
        padding = 0
    else:
        padding = ((d+1)*8) - consumed
    # print(f"padding {padding}")
    return padding


def parse_bitstream(bitstream, start_ind=0, calc_padding=False):
    packet = {}
    packet['start_ind'] = start_ind
    packet['version'] = int(bitstream[VERSION_SLICE], 2)
    type_id = PacketTypeID(int(bitstream[TYPE_ID_SLICE], 2))
    packet['type_id'] = type_id
    consumed = 0
    if type_id == PacketTypeID.LITERAL:
        # print("parsing literal")
        consumed += TYPE_ID_SLICE.stop
        packet['header_bits'] = bitstream[:consumed]
        # decode literal
        lit, consumed_by_lit = decode_literal(bitstream[LITERAL_SLICE], 5)
        packet['literal'] = lit
        consumed += consumed_by_lit
        if calc_padding is True:
            padding = calc_padding_bits(consumed + start_ind, 8)
            consumed += padding
        packet['consumed_total'] = consumed
        packet['bits'] = bitstream[:consumed]
        packet['body_bits'] = bitstream[len(packet['header_bits']):consumed]
        return packet, bitstream[consumed:]

    length_type_id = int(bitstream[LENGTH_TYPE_ID_SLICE], 2)
    packet['length_type_id'] = length_type_id
    # unknown number of subpackets
    if length_type_id == 0:
        total_length_in_bits = int(bitstream[TOTAL_LENGTH_IN_BITS_SLICE], 2)
        packet['total_length_in_bits'] = total_length_in_bits
        consumed += TOTAL_LENGTH_IN_BITS_SLICE.stop
        packet['header_bits'] = bitstream[:consumed]
        subpacket_bits = bitstream[consumed:consumed+total_length_in_bits]
        original_subpackets_len = len(subpacket_bits)
        subpacket_bits_consumed = 0
        subpackets = []
        while subpacket_bits_consumed < total_length_in_bits:
            # print(f"parsing subpacket 1 {subpacket_bits}")
            retnd, new_subpacket_bits = parse_bitstream(subpacket_bits,
                                                        start_ind=consumed,
                                                        calc_padding=False)
            subpackets.append(retnd)
            consumed_this_iter = len(subpacket_bits) - len(new_subpacket_bits)
            # to calculate padding correctly
            subpacket_bits_consumed += consumed_this_iter
            consumed += consumed_this_iter
            subpacket_bits = new_subpacket_bits
        # padding = calc_padding_bits(consumed + start_ind, 8)
        # consumed += padding
        packet['subpackets'] = subpackets
        packet['consumed_total'] = consumed
        packet['bits'] = bitstream[:consumed]
        packet['body_bits'] = bitstream[len(packet['header_bits']):consumed]
        return packet, bitstream[consumed:]
    # known number of subpackets
    elif length_type_id == 1:
        num_subpackets = int(bitstream[NUM_SUBPACKETS_IMM_CONTD_SLICE], 2)
        packet['num_subpackets'] = num_subpackets
        consumed += NUM_SUBPACKETS_IMM_CONTD_SLICE.stop
        packet['header_bits'] = bitstream[:consumed]
        subpacket_bits = bitstream[consumed:]
        subpackets = []
        i = 0
        while i < num_subpackets:
            # print(f"parsing subpacket 2 {subpacket_bits}")
            # print(f"consumed {consumed}")
            retnd, new_subpacket_bits = parse_bitstream(subpacket_bits,
                                                        start_ind=consumed,
                                                        calc_padding=False)
            subpackets.append(retnd)
            # to calculate padding correctly
            consumed += len(subpacket_bits) - len(new_subpacket_bits)
            subpacket_bits = new_subpacket_bits
            i += 1
        # padding = calc_padding_bits(consumed + start_ind, 8)
        # consumed += padding
        packet['subpackets'] = subpackets
        packet['consumed_total'] = consumed
        packet['bits'] = bitstream[:consumed]
        packet['body_bits'] = bitstream[len(packet['header_bits']):consumed]
        return packet, bitstream[consumed:]


def packet_ast_codegen(packet):
    """Do the lazy thing and just generate code that python
    can easily handle"""
    if not isinstance(packet, dict):
        raise Exception("Non dict packet")

    type_id = packet['type_id']
    if type_id == PacketTypeID.LITERAL:
        return str(packet['literal'])

    # make bool values express as integers
    open_token = 'int('
    close_token = ')'
    comparator_token = None

    if type_id == PacketTypeID.SUM:
        open_token = 'sum(['
        close_token = '])'
    elif type_id == PacketTypeID.PRODUCT:
        open_token = 'prod(['
        close_token = '])'
    elif type_id == PacketTypeID.MINIMUM:
        open_token = 'min(['
        close_token = '])'
    elif type_id == PacketTypeID.MAXIMUM:
        open_token = 'max(['
        close_token = '])'
    elif type_id == PacketTypeID.GREATER_THAN:
        comparator_token = '>'
    elif type_id == PacketTypeID.LESS_THAN:
        comparator_token = '<'
    elif type_id == PacketTypeID.EQUAL_TO:
        comparator_token = '=='

    subpackets = packet.get('subpackets', [])
    child_node_values = []
    for i in subpackets:
        child_node_values.append(packet_ast_codegen(i))

    if comparator_token is None:
        result = "%s%s%s" % (open_token,
                             ', '.join(child_node_values),
                             close_token)
    else:
        lchild, rchild = child_node_values
        result = "%s%s %s %s%s" % (open_token,
                                   lchild,
                                   comparator_token,
                                   rchild,
                                   close_token)

    return result


packet, _ = parse_bitstream(bitstream)

part1_res = sum_version_numbers(packet)
print(f"part 1: {part1_res}")
a = packet_ast_codegen(packet)
print(a)
part2_res = eval(a)

print(f"part 2: {part2_res}")
