LEFT = "Left"
RIGHT = "Right"
UP = "Up"
DOWN = "Down"
MOVEKEYS = [LEFT, RIGHT, UP, DOWN]
from typing import List, Tuple, Any, Optional

Location = Tuple[int, int]


class Node:
    """
    Node class for snake linked list
    """

    def __init__(self, location: Optional[Location] = None) -> None:
        """
        Initializes node object
        :param location: node location
        """
        self.__location = location
        self.__next = None
        self.__prev = None

    ## getters ##
    def get_location(self) -> Location:
        """
        :return: node location
        """
        return self.__location

    def get_next(self) -> Any:
        """
        :return: next node object
        """
        return self.__next

    def get_prev(self) -> Any:
        """
        :return: previous node object
        """
        return self.__prev

    ## setters ##
    def set_location(self, location: Location) -> None:
        """
        Sets node location
        :param location: new location for node
        """
        self.__location = location

    def set_next(self, next: Any) -> None:
        """
        Sets node next pointer
        :param next: next node to point to
        """
        self.__next = next

    def set_prev(self, prev: Any):
        """
        Sets node previous pointer
        :param next: previous node to point to
        """
        self.__prev = prev


class Snake:
    """
    Snake class for snake game, linked lists of nodes
    """

    def __init__(self, direction: str, head: Any = None):
        """
        Initializes snake class
        :param direction: starting direction for snake
        :param head: head node object for snake
        """
        self.__head = self.__tail = head
        self.__direction = direction
        self.__apple_timer = 0

    ## getters ##
    def get_head(self) -> Any:
        """
        :return: head node
        """
        return self.__head

    def get_direction(self) -> str:
        """
        :return: direction
        """
        return self.__direction

    def get_tail(self) -> Any:
        """
        :return: tail node
        """
        return self.__tail

    def get_coordinates(self) -> List[Location]:
        """
        :return: list of nodes location of snake
        """
        coords = []
        cur = self.__head
        while cur is not None:
            coords.append(cur.get_location())
            cur = cur.get_next()
        return coords

    ## setters ##
    def add_to_apple_timer(self, time: int) -> None:
        """
        Adds time to apple timer
        :param time: time
        :return:
        """
        self.__apple_timer += time

    def update_apple_timer(self) -> None:
        """
        :return: removes 1 from apple timer
        """
        if self.__is_eating():
            self.__apple_timer -= 1

    def add_head(self, new_head: Any) -> None:
        """
        Adds node as new snake head
        :param new_head: new node to add
        """
        if self.__head is None:
            self.__tail = new_head
        else:
            self.__head.set_prev(new_head)
            new_head.set_next(self.__head)
        self.__head = new_head

    def add_tail(self, new_tail: Any) -> None:
        """
        Adds node as new snake tail
        :param new_tail: new node to add
        """
        if self.__tail is None:
            self.__head = new_tail
        else:
            self.__tail.set_next(new_tail)
            new_tail.set_prev(self.__tail)
        self.__tail = new_tail

    def rem_head(self) -> None:
        """
        removes the snake's head
        """
        self.__head = self.__head.get_next()
        if self.__head is None:
            self.__tail = None
        else:
            self.__head.get_prev().set_next(None)
            self.__head.set_prev(None)

    def get_node_by_location(self, location: Location) -> Any:
        """
        return node in given location
        :param location: wanted location
        :return: relevant node
        """
        cur = self.__head
        while cur:
            if cur.get_location() == location:
                return cur
            cur = cur.get_next()

    def rem_node(self, location: Location) -> None:
        """
        removes node in given location
        can work on head, tail, or middle
        :param location: wanted location to remove
        """
        node = self.get_node_by_location(location)
        if node == self.__head:
            self.rem_head()
        elif node == self.__tail:
            self.__rem_tail()
        else:
            save_next = node.get_next()
            save_prev = node.get_prev()
            save_next.set_prev(save_prev)
            save_prev.set_next(save_next)

    ## movement ##
    def __rem_tail(self):
        """
        Cuts tail from snake
        """
        self.__tail = self.__tail.get_prev()
        if self.__tail is None:
            self.__head = None
        else:
            self.__tail.get_next().set_prev(None)
            self.__tail.set_next(None)

    # def __update_direction(self, movekey):
    #     """
    #     Updaes snake direction by movekey
    #     :param movekey: direction to move
    #     """
    #     self.__direction = movekey

    def __is_eating(self) -> bool:
        """
        Checks if the snake is eating based on apple timer
        :return: True for eating, False for none
        """
        return self.__apple_timer > 0

    def __movement_requirements(self, movekey: str) -> Optional[Location]:
        """
        :param movekey: direction to move, assuming it is valid
        :return:  the cell required for move by movekey, or False if the
        movekey doesn't match direction
        """
        x, y = self.__head.get_location()
        if movekey == UP:
            return x, y + 1
        elif movekey == DOWN:
            return x, y - 1
        elif movekey == LEFT:
            return x - 1, y
        elif movekey == RIGHT:
            return x + 1, y

    def is_legal_direction(self, movekey: str) -> bool:
        """
        Checks if the move is legal (doesn't contradict current direction)
        :param movekey: direction to move
        :return: True if legal, else False
        """
        if movekey == UP and self.__direction == DOWN:
            return False
        elif movekey == DOWN and self.__direction == UP:
            return False
        elif movekey == LEFT and self.__direction == RIGHT:
            return False
        elif movekey == RIGHT and self.__direction == LEFT:
            return False
        else:
            return True

    def move_snake(self, movekey: str) -> None:
        """
        Updates snake's head and tail based on move.
        :param movekey: direction to move, assuming it is valid
        :return: True for success, else False
        """
        new_head_location = self.__movement_requirements(movekey)
        self.add_head(Node(new_head_location))
        if not self.__is_eating():
            self.__rem_tail()
        self.__direction = movekey