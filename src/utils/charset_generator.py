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
    bit_str = ""
    up = 1
    down = 0
    
    while True:
        # sleep(1)
        delimeter = (up - down)/2
        head = down + delimeter
        # print("down: {}, up: {}, head: {} , delimeter: {}".format(down,  up, head, delimeter))
        if down >= lower_bound and up <= upper_bound:
            return bit_str       
        
        if (head <= upper_bound) and (head >= lower_bound):
            if abs(head - upper_bound) > abs(head - lower_bound):
                down += delimeter
                bit_str += "1"
            else:
                up -= delimeter
                bit_str += "0"
            continue

        if up > upper_bound and (up-delimeter)>lower_bound:
            up -= delimeter
            bit_str += "0"
            continue

        if down < lower_bound and (down+delimeter)<upper_bound:
            down += delimeter
            bit_str += "1"
            continue