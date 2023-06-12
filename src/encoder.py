from collections import Counter

from number_range import NumberRange


class Encoder:

    def __init__(self, 
                 initial_string: str):
        if initial_string is not None:
            statistic = Counter(initial_string)
        else:
            statistic = None
        self.number_range = NumberRange(statistic=statistic)

    def encode(self, 
               message_to_encode: str):
        lower_bound = 0.0
        upper_bound = 1.0
        for i in range(len(message_to_encode)):
            character = message_to_encode[i]
            character_info = self.number_range.get_character_information(character=character)
            if character_info != None:
                is_new_character = False
                list_index = character_info["list_index"]
                temp_lower_bound = character_info["lower_bound"]
                temp_upper_bound = character_info["upper_bound"]
            else:
                is_new_character = True
                list_index = None
                temp_lower_bound = None
                temp_upper_bound = None
            self.number_range.update_information(character=character,
                                                 count=1,
                                                 is_new_character=is_new_character,
                                                 list_index=list_index,
                                                 lower_bound=temp_lower_bound,
                                                 upper_bound=temp_upper_bound)
            self.number_range.update_probabilities()
            self.number_range.update_bounds(lower_bound=lower_bound,
                                            upper_bound=upper_bound)
            character_info = self.number_range.get_character_information(character=character)
            upper_bound = character_info["upper_bound"]
            lower_bound = character_info["lower_bound"]
            self.number_range.update_bounds(lower_bound=lower_bound,
                                            upper_bound=upper_bound)
        return (lower_bound, upper_bound)

    def get_number_range(self) -> NumberRange:
        return self.number_range


if __name__ == "__main__":
    initial_string = "ARYTMETYKA"
    encoder = Encoder(initial_string)
    message_to_encode = "HELLO"
    result = encoder.encode(message_to_encode=message_to_encode)
    print(result)
