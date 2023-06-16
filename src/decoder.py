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
        else:
            statistic = None
        self.number_range = NumberRange(statistic=statistic)

    # prints decoded characters to the output
    def decode(self, message: float, cap: int):
        for i in range(cap):
            character = self._find_character(message)
            if character is None:
                raise CharacterNotDefined(f"Character {character} not defined in the statistic")

            character_info = self.number_range.get_character_information(character=character)
            upper_bound = character_info["upper_bound"]
            lower_bound = character_info["lower_bound"]
            self.number_range.update_bounds(lower_bound=lower_bound,
                                            upper_bound=upper_bound)
            self.number_range.update_information(character=character,
                                                 count=1)
            self.number_range.update_probabilities()
            print(character)

    def _find_character(self, message: float) -> Union[str, None]:
        for character, char_info in self.number_range.get_range_information().items():
            if char_info["lower_bound"] <= message <= char_info["upper_bound"]:
                return character
        return None
