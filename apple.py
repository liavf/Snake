from typing import Tuple


class Apple:
    """
    This is an Apple class
    """
    def __init__(self, location: Tuple, score: int):
        self.__location = location
        self.__score = score
    def get_location(self) -> Tuple:
        """
        :return: apple location
        """
        return self.__location
    def get_score(self) -> int:
        """""
        :return: apple score
        """
        return self.__score


