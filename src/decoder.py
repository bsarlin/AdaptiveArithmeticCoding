from collections import Counter
from typing import List, Tuple, Union

from number_range import NumberRange


class CharacterNotDefined(Exception):
    pass


class Decoder:

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

    # prints decoded characters to the output
    def decode(self, message: float, cap: int) -> str:
        result = ""
        for _ in range(cap):
            character = self._find_character(message)
            if character is None:
                raise CharacterNotDefined(f"Character {character} not defined in the statistic")
            result += character
            if character == self.stop_char:
                break

            character_info = self.number_range.get_character_information(character=character)
            upper_bound = character_info["upper_bound"]
            lower_bound = character_info["lower_bound"]

            self.number_range.update_information(character=character,
                                                 count=1)
            self.number_range.update_probabilities()
            self.number_range.update_bounds(lower_bound=lower_bound,
                                            upper_bound=upper_bound)
        return result

    def decode_using_integers(self,
                              message_to_decode: str) -> str:
        lower_bound = 0
        upper_bound = 999999
        right_offset = 6
        registry = message_to_decode[right_offset-6:right_offset]
        result = ""
        while True:
            helper = (int(registry) - lower_bound) / (upper_bound - lower_bound + 1)
            character = self._find_character(helper)
            if character is None:
                raise CharacterNotDefined(f"Character {character} not defined in the statistic")
            result += character
            if character == self.stop_char:
                break

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
                    lower_bound_as_string = lower_bound_as_string[1:] + '0'
                    lower_bound = int(lower_bound_as_string)
                    upper_bound_as_string = upper_bound_as_string[1:] + '9'
                    upper_bound = int(upper_bound_as_string)
                    right_offset += 1
                    registry = registry[1:]
                    if len(message_to_decode) >= right_offset:
                        registry += message_to_decode[right_offset-1]
                elif diff_by_one and lower_bound_as_string[1] == '0' and upper_bound_as_string[1] == '9':
                    lower_bound_as_string = lower_bound_as_string[:2] + lower_bound_as_string[3:] + '0'
                    upper_bound_as_string = upper_bound_as_string[:2] + upper_bound_as_string[3:] + '9'
                    right_offset += 1
                    registry = registry[:2] + registry[3:] + message_to_decode[right_offset-1]
                    lower_bound = int(lower_bound_as_string)
                    upper_bound = int(upper_bound_as_string)
                else:
                    stop_loop = True
            self.number_range.update_information(character=character,
                                                 count=1)
            self.number_range.update_probabilities()
            self.number_range.update_bounds(lower_bound=0.0,
                                            upper_bound=1.0)
        return result

    def _find_character(self, message: float) -> Union[str, None]:
        for character, char_info in self.number_range.get_range_information().items():
            if char_info["lower_bound"] <= message < char_info["upper_bound"]:
                return character
        return None
