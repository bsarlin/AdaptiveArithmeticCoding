from random import randrange
from math import log2
from typing import Tuple
from time import sleep

def file_reader(filename: str, numeric_output: bool = False):
    with open(filename, 'r') as file:
        text = file.read()
        for char in text:
            yield ord(char) if numeric_output else char

def random_character_stream(batch_size: int, numeric_output: bool = False):
    for i in range(batch_size):
        char = randrange(64, 127)
        yield char if numeric_output else chr(char)

def file_charset_stats(filename: str):
    char_dict = {}
    with open(filename, 'r') as file:
        text = file.read()
        for char in text:
            if char not in char_dict:
                char_dict[char] = 0
            char_dict[char] += 1
    return char_dict

def file_charset_entropy(filename: str):
    stats = file_charset_stats(filename=filename)
    denominator = sum(stats.values())
    if denominator == 0:
        raise ValueError("No characters found")
    entropy = 0
    for val in stats.values():
        entropy += (val/denominator)*log2(denominator/val)
    return entropy

def message_entropy(message: str):
    char_dict = {}
    for char in message:
        if char not in char_dict:
            char_dict[char] = 0
        char_dict[char] += 1
    denominator = sum(char_dict.values())    
    if denominator == 0:
        raise ValueError("No characters found")
    entropy = 0
    for val in char_dict.values():
        entropy += (val/denominator)*log2(denominator/val)
    return entropy

def get_bit_representation(bounds: Tuple[float, float]) -> str:
    lower_bound = bounds[0]
    upper_bound = bounds[1]
    print("upper_bound: {}, lower_bound: {}".format(upper_bound,  lower_bound))
    bit_str = ""
    up = 1
    down = 0
    while True:
        if lower_bound <= down and upper_bound >= up:
            return bit_str        
        if up >= upper_bound and (up - (up - down)/2) > down and (up - (up - down)/2) > lower_bound:
            up = up - (up - down)/2
            bit_str += "0"
        else:
            down = down + (up - down)/2
            bit_str += "1"