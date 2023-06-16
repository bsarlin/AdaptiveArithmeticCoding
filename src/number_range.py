from collections import Counter
from typing import Any, Dict, Union


class NumberRange:

    def __init__(self, 
                 statistic: Counter):
        self._characters = []
        self._range_information = {}
        self._sum_of_counts = 0
        if statistic is not None:
            self._create_range_information_from_statistic(statistic=statistic)
            self.update_probabilities()
            self.update_bounds(lower_bound=0.0,
                               upper_bound=1.0)

    # updates each character's bounds in relation to other characters' order and probability
    # 1st update operation
    def update_bounds(self,
                      lower_bound: float,
                      upper_bound: float):
        range_length = len(self._characters)
        range_size = upper_bound - lower_bound
        for character in self._characters:
            character_index = self._range_information[character]["list_index"]
            probability = self._range_information[character]["probability"]
            if character_index == 0:
                self._range_information[character]["lower_bound"] = lower_bound
            else:
                self._range_information[character]["lower_bound"] = self._range_information[self._characters[character_index - 1]]["upper_bound"]
            if character_index == range_length - 1:
                self._range_information[character]["upper_bound"] = upper_bound
            else:
                self._range_information[character]["upper_bound"] = self._range_information[character]["lower_bound"] + probability * range_size

    # updates each character's "probability" field based on each character's count and the sum of all counts
    # 3rd update operation
    def update_probabilities(self):
        for character in self._characters:
            self._range_information[character]["probability"] = self._range_information[character]["count"] / self._sum_of_counts

    def _create_range_information_from_statistic(self, 
                                                 statistic: Counter):
        list_index = 0
        for character in statistic.keys():
            count = statistic[character]
            self.update_information(character=character, 
                                    count=count)
            list_index += 1

    # updates a character's count and index information
    # 2nd update operation
    def update_information(self, 
                           character: str, 
                           count: int):
        self._sum_of_counts += count
        is_new_character = self.get_character_information(character=character) is None
        if is_new_character:
            current_count = 0
            self._characters.append(character)
            lower_bound = None
            upper_bound = None
            list_index = len(self._characters) - 1
        else:
            current_count = self._range_information[character]["count"]
            lower_bound = self._range_information[character]["lower_bound"]
            upper_bound = self._range_information[character]["upper_bound"]
            list_index = self._range_information[character]["list_index"]
        self._range_information[character] = {
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "count": current_count + count,
            "list_index": list_index
            }   

    def get_range_information(self) -> Dict[str, Dict]:
        return self._range_information
    
    def get_character_information(self, 
                                  character: str = None) -> Union[Dict[str, Any], None]:
        try:
            if character is None:
                character = self._characters[len(self._characters) - 1]
            return self._range_information[character]
        except KeyError:
            return None
