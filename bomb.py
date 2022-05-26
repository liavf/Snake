
from typing import List, Tuple
Location = Tuple[int, int]

class Bomb:
    """
    this is a bomb class
    """
    def __init__(self, location: Location, radius: int, time: int):
        """
        inits a bomb object (with random params)
        :param location: bombs location
        :param radius: bombs radius when in shock
        :param time: bombs time until shock
        """
        self.__location = location
        self.__radius = radius
        self.__time = time
        self.__shock_timer = 0

    def get_time(self) -> int:
        """
        :return: bomb time
        """
        return self.__time

    def update_timer(self):
        """
        updates timer every round depending on shock state
        if not in shock - dec timer
        if in shock - dec shock timer
        when timer reaches zero - switch to chock mode
        """
        if self.__time >= 0:
            self.__time -= 1
        else:
            self.__shock_timer += 1

    def get_shock_couples(self) -> List[Tuple[int, int]]:
        """
        gets couple in range which add to manhattan value
        :return: all relevant couples for calculating shock
        """
        couples = []
        current_radius = self.__shock_timer
        for i in range(current_radius + 1):
            couples.append((i, current_radius - i))
        return couples

    def get_shock_location(self) -> List[Location]:
        """
        gets all locations of shock according to current radius
        :return: shock locations
        """
        x, y = self.__location
        coup_list = set()
        for coup in self.get_shock_couples():
            first, second = coup
            # all possible combinations
            coup_list.add((x + first, y + second))
            coup_list.add((x + first, y - second))
            coup_list.add((x - first, y + second))
            coup_list.add((x - first, y - second))
        return list(coup_list)

    def finished(self) -> bool:
        """
        checks if bomb finished shock wave
        :return: True / False
        """
        if self.__shock_timer == self.__radius:
            return True
        else:
            return False

    def is_shock(self) -> bool:
        """
        checks if bomb switched to shock mode
        :return: True / False
        """
        return self.__time < 0

    def get_location(self) -> List[Location]:
        """
        returns bomb's location - reg / shock
        :return: location (one or more)
        """
        if not self.is_shock():
            return [self.__location]
        else:
            return self.get_shock_location()

