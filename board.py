from apple import *
from bomb import *
from game_parameters import *
from typing import List, Tuple, Any, Dict

Location = Tuple[int, int]


class Board:
    """
    Board class for snake game, containing snake, bombs and apples
    """

    def __init__(self, width: int, height: int) -> None:
        """
        Initialized board object
        :param width: board width
        :param height: board hight
        """
        self.__apples = []
        self.__bombs = []
        self.__width = width
        self.__height = height
        self.__taken = {}
        self.__snake = None

    #### getters ####
    def get_snake(self) -> Any:
        """
        :return: snake object
        """
        return self.__snake

    def get_apples(self) -> List[Any]:
        """
        :return: apples list
        """
        return self.__apples

    def get_bombs(self) -> List[Any]:
        """
        :return: bombs list
        """
        return self.__bombs

    def get_taken(self) -> Dict[Location]:
        """
        :return: taken locations list of tuples [(x,y)]
        """
        return self.__taken

    def cell_content(self, location: Location) -> Any:
        """
        :param location: location index (x,y)
        :return: class of location in board
        """
        if location in self.__taken:
            return self.__taken[location]
        return None

    def get_empty_cells_num(self) -> int:
        """
        :return: how many empty cells are in board
        """
        return (self.__width * self.__height) - len(self.__taken)

    #### checkers ####
    def __legal_add(self, cells: List[Location]) -> bool:
        """
        :param cells: cells to add an object in
        :return:
        """
        for cell in cells:
            if self.in_borders(cell) and cell not in self.__taken:
                return True
        return False

    def in_borders(self, location: Location) -> bool:
        """
        :param location: location tuple
        :return: True if cell in board, else False
        """
        x, y = location
        if x < 0 or x >= self.__width:
            return False
        if y < 0 or y >= self.__height:
            return False
        return True

    #### setters - add ####
    def add_snake(self, snake: Any) -> None:
        """
        Adds snake in board
        :param snake: Snake class object
        """
        if self.__legal_add(snake.get_coordinates()):
            self.__snake = snake
            for cell in snake.get_coordinates():
                self.__taken[cell] = snake

    def add_apple(self) -> bool:
        """
        Adds random apple in board
        :return: True if succeeded, False if not (in case of zero valid
        locations for apple
        """
        if self.get_empty_cells_num() > 0:
            x, y, score = get_random_apple_data()
            while not self.__legal_add([(x, y)]):
                x, y, score = get_random_apple_data()
            apple = Apple((x, y), score)
            self.__apples.append(apple)
            self.__taken[(x, y)] = apple
            return True
        return False

    def add_bomb(self) -> bool:
        """
        Adds random bomb in board
        :return: True if succeeded, False if not (in case of zero valid
        locations for bomb
        """
        if self.get_empty_cells_num() > 0:
            x, y, radius, time = get_random_bomb_data()
            while not self.__legal_add([(x, y)]):
                x, y, radius, time = get_random_bomb_data()
            bomb = Bomb((x, y), radius, time)
            self.__bombs.append(bomb)
            self.__taken[(x, y)] = bomb
            return True
        return False

    ## setters - del ##
    def del_bomb(self, bomb: Any) -> None:
        """
        Removes bomb from board
        :param bomb: Bomb class object
        """
        self.__bombs.remove(bomb)

    def del_apple(self, apple: Any) -> None:
        """
        Removes apple from board
        :param bomb: Apple class object
        """
        self.__apples.remove(apple)

    ## setters - update ##
    def get_taken_coordinates(self) -> Dict[Location, Any]:
        """
        :return: taken coordinates dict {(x,y): object}
        """
        return self.__taken

    def update_location(self, location: Location, object: Any) -> None:
        """
        Adds object in given location to taken cells dictionary
        :param location: location to add
        :param object: object to add
        """
        self.__taken[location] = object

    def update_taken(self) -> None:
        """
        Updates taken coordinates based on board content, assuming there is no
        overlaps.
        """
        self.__taken = {}  # eliminates previous taken
        if self.__snake:
            for cell in self.__snake.get_coordinates():
                if self.in_borders(cell):
                    self.__taken[cell] = self.__snake
        for apple in self.__apples:
            self.__taken[apple.get_location()] = apple
        for bomb in self.__bombs:
            for cell in bomb.get_location():
                if self.in_borders(cell):
                    self.__taken[cell] = bomb
