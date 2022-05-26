LEFT = "Left"
RIGHT = "Right"
UP = "Up"
DOWN = "Down"
MOVEKEYS = [LEFT, RIGHT, UP, DOWN]

class Node:
    def __init__(self, location=None, next=None, prev=None):
        self.location = location
        self.next = next
        self.prev = prev

    def get_location(self):
        return self.location

    def get_next(self):
        return self.next

    def get_prev(self):
        return self.prev

    def set_location(self, location):
        self.location = location

    def set_next(self, next):
        self.next = next

    def set_prev(self, prev):
        self.prev = prev


class Snake:
    def __init__(self, head=None, direction=UP):
        self.head = self.tail = head
        self.length = 0
        self.direction = direction
        self.apple_timer = 0

    def get_head(self):
        return self.head

    def set_apple_timer(self, time):
        self.apple_timer += time

    def update_apple_timer(self):
        self.apple_timer -= 1

    def get_is_eating(self):
        return self.apple_timer > 0

    def add_head(self, new_head):
        if self.head is None:
            self.tail = new_head
        else:
            self.head.set_prev(new_head)
            new_head.set_next(self.head)
        self.head = new_head
        self.length += 1

    def add_last(self, node):
        if self.tail is None:
            self.head = node
        else:
            self.tail.next = node
            node.prev = self.tail
        self.tail = node
        self.length += 1

    def rem_tail(self):
        # last = self.tail.location
        self.tail = self.tail.get_prev()
        if self.tail is None:
            self.head = None
        else:
            self.tail.next.set_prev(None)
            self.tail.set_next(None)
        self.length -= 1
        # return last

    def get_coordinates(self):
        coords = []
        cur = self.head
        while cur is not None:
            coords.append(cur.get_location())
            cur = cur.get_next()
        return coords

    def is_empty(self):
        return self.head == None

    def movement_requirements(self, movekey):
        #todo: do we want to be able to move few steps at a time? return a
        # list?
        """
        returns the cell requirement for move by movekey, or False if the
        movekey doesn't match direction
        :param movekey:
        :return:
        """
        head_location = self.get_head().location
        if movekey == UP and self.direction != DOWN:
            return head_location[0], head_location[1] + 1
        elif movekey == DOWN and self.direction != UP:
            return head_location[0], head_location[1] - 1
        elif movekey == LEFT and self.direction != RIGHT:
            return head_location[0] - 1, head_location[1]
        elif movekey == RIGHT and self.direction != LEFT:
            return head_location[0] + 1, head_location[1]
        else: #unkown move
            return None

    def is_legal_direction(self, movekey):
        if movekey == UP and self.direction == DOWN:
            return False
        elif movekey == DOWN and self.direction == UP:
            return False
        elif movekey == LEFT and self.direction == RIGHT:
            return False
        elif movekey == RIGHT and self.direction == LEFT:
            return False
        else:
            return True

    def move_snake(self, movekey):
        """
        Updates snakes locations based on move.
        :param movekey: move direction
        :param is_growing: bool to decide if the tail of the snake should be
        removed after moving, or not (in case of eating the apple)
        :return: True for success, else False (in case of unkown movekey or
        movekey that does not match the current direction).
        """
        head_location = self.movement_requirements(movekey)
        if head_location is not None:
            self.add_head(Node(head_location))
            if not self.get_is_eating():
                self.rem_tail()
            self.update_direction(movekey)
            return True
        return False

    def update_direction(self, movekey):
        self.direction = movekey
