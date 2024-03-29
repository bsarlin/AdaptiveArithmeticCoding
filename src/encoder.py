from collections import Counter
from typing import List, Tuple

from number_range import NumberRange
from decoder import Decoder

from huffman import Huffman_Encoding
from charset_generator import *


class Encoder:

    def __init__(self, 
                 initial_string: str):
        if initial_string is not None:
            statistic = Counter(initial_string)
            stop_char = initial_string[len(initial_string) - 1]
        else:
            statistic = None
            stop_char = None
        self.number_range = NumberRange(statistic=statistic)
        self.stop_char = stop_char

    def encode(self, 
               message_to_encode: str) -> Tuple[float, float]:
        lower_bound = 0.0
        upper_bound = 1.0
        for i in range(len(message_to_encode)):
            character = message_to_encode[i]
            character_info = self.number_range.get_character_information(character=character)
            upper_bound = character_info["upper_bound"]
            lower_bound = character_info["lower_bound"]

            self.number_range.update_information(character=character,
                                                 count=1)
            self.number_range.update_probabilities()
            self.number_range.update_bounds(lower_bound=lower_bound,
                                            upper_bound=upper_bound)

        return lower_bound, upper_bound

    def get_number_range(self) -> NumberRange:
        return self.number_range
    
    def encode_using_integers(self,
                              message_to_encode: str) -> Tuple[str, List[int]]:
        lower_bound = 0
        upper_bound = 999999
        underflow_count = 0
        underflows = []
        result = ""
        for i in range(len(message_to_encode)):
            character = message_to_encode[i]
            character_info = self.number_range.get_character_information(character=character)
            range_size = upper_bound - lower_bound + 1
            upper_bound = int(lower_bound + (range_size * character_info["upper_bound"]) - 1)
            lower_bound = int(lower_bound + range_size * character_info["lower_bound"])
            lower_bound_as_string = "{:06d}".format(lower_bound)
            upper_bound_as_string = "{:06d}".format(upper_bound)
            stop_loop = False
            while not stop_loop:
                diff_by_one = abs(int(lower_bound_as_string[0]) - int(upper_bound_as_string[0])) == 1
                if lower_bound_as_string[0] == upper_bound_as_string[0]:
                    result = result + lower_bound_as_string[0]
                    lower_bound_as_string = lower_bound_as_string[1:] + '0'
                    lower_bound = int(lower_bound_as_string)
                    upper_bound_as_string = upper_bound_as_string[1:] + '9'
                    upper_bound = int(upper_bound_as_string)
                    if underflow_count != 0:
                        result += underflow_count
                        underflows.append(underflow_count)
                        underflow_count = 0
                elif diff_by_one and lower_bound_as_string[1] == '0' and upper_bound_as_string[1] == '9':
                    lower_bound_as_string = lower_bound_as_string[:2] + lower_bound_as_string[3:] + '0'
                    upper_bound_as_string = upper_bound_as_string[:2] + upper_bound_as_string[3:] + '9'
                    underflow_count += 1
                    lower_bound = int(lower_bound_as_string)
                    upper_bound = int(upper_bound_as_string)
                else:
                    stop_loop = True
            self.number_range.update_information(character=character,
                                                 count=1)
            self.number_range.update_probabilities()
            self.number_range.update_bounds(lower_bound=0.0,
                                            upper_bound=1.0)
        lower_bound_as_string = str(lower_bound)
        digits_to_append = str(int(lower_bound_as_string.rstrip('0')))
        result = result + digits_to_append
        return (result, underflows)

if __name__ == "__main__":
    initial_string = "ARYTMEK$"
    encoder = Encoder(initial_string)
    decoder = Decoder(initial_string)
    message_to_encode = "AR"
    result = encoder.encode(message_to_encode=message_to_encode)
    # take a number from the middle of the output range
    encoded_message = result[0] + ((result[1] - result[0]) / 2)

    bit_repr = get_bit_representation(result)
    bit_repr_huff, tree = Huffman_Encoding(message_to_encode)
    print("Bit representation: {}".format(bit_repr))
    print("Bit representation: {} (Huffman)".format(bit_repr_huff))
    print("B/C ratio: {} bits".format(len(bit_repr) / len(message_to_encode)))
    print("B/C ratio: {} bits (Huffman)".format(len(bit_repr_huff) / len(message_to_encode)))
    print("\"{}\" entropy: {} bits".format(message_to_encode, message_entropy(message_to_encode)))
    
    decoder.decode(message=encoded_message, cap=15)
    print(result)
