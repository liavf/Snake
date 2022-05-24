LEFT = "Left"
RIGHT = "Right"
UP = "Up"
DOWN = "Down"
MOVEKEYS = [LEFT, RIGHT, UP, DOWN]

class Snake:
    def __init__(self, direction, coordinates, is_growing):
        self.direction = direction
        self.coordinates = coordinates
        self.is_growing = is_growing

    def get_coordinates(self, coordinates):
        return self.coordinates

    def move_snake(self, movekey, is_growing):
        """
        Updates snakes locations based on move.
        :param movekey: move direction
        :param is_growing: bool to decide if the tail of the snake should be
        removed after moving, or not (in case of eating the apple)
        :return: True for success, else False (in case of unkown movekey or
        movekey that does not match the current direction).
        """
        head_location = self.coordinates[0]
        if movekey == UP and self.direction != DOWN:
            new_head_location = head_location[0], head_location[1] + 1
        elif movekey = DOWN and self.direction != UP:
            new_head_location = head_location[0], head_location[1] - 1
        elif movekey == LEFT and self.direction != RIGHT:
            new_head_location = head_location[0] - 1, head_location[1]
        elif movekey == RIGHT and self.direction != LEFT:
            new_head_location = head_location[0] + 1, head_location[1]
        else: #unkown move
            return False

        if new_head_location in self.coordinates(): #ovverrun itself
            return False
        else:
            self.coordinates[0] = new_head_location
            if not self.is_growing: #remove tail
                self.coordinates.pop(-1)
            return True

