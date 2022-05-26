from typing import Tuple
Location = Tuple[int, int]

class Apple:
    """
    Apple class for snake game
    """
    def __init__(self, location: Location, score: int):
        """
        Initialized apple class
        :param location: apple location
        :param score: apple's worth in scores
        """
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


