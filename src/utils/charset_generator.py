from random import randrange
from math import log2

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