from collections import Counter


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

    def update_probabilities(self):
        for character in self._characters:
            self._range_information[character]["probability"] = self._range_information[character]["count"] / self._sum_of_counts

    def _create_range_information_from_statistic(self, 
                                                 statistic: Counter):
        list_index = 0
        for character in statistic.keys():
            count = statistic[character]
            self.update_information(character=character, 
                                    count=count, 
                                    list_index=list_index,
                                    is_new_character=True)
            list_index += 1

    def update_information(self, 
                           character: str, 
                           count: int, 
                           list_index: int = None, 
                           lower_bound: float = None,
                           upper_bound: float = None,
                           is_new_character: bool = False):
        self._sum_of_counts += count
        if is_new_character == True:
            current_count = 0
            self._characters.append(character)
            list_index = len(self._characters) - 1
        else:
            current_count = self._range_information[character]["count"]
        self._range_information[character] = {
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "count": current_count + count,
            "list_index": list_index          
            }   

    def get_range_information(self):
        return self._range_information
    
    def get_character_information(self, 
                                  character: str = None):
        try:
            if character is None:
                character = self._characters[len(self._characters) - 1]
            return self._range_information[character]
        except KeyError:
            return None
