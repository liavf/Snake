from apple import *
from bomb import *

class Board:
    def __init__(self, width, height):
        self.snake = snake
        self.apples = []
        self.bombs = []
        self.width = width
        self.height = height
        self.taken = {}

    #### getters ####
    def get_apples(self):
        return self.apples

    def get_bombs(self):
        return self.bombs

    def get_taken(self):
        return self.taken

    def cell_content(self, location):
        if location in self.taken:
            return self.taken[location]
        else:
            return None

    def get_empty_cells_num(self):
        return (self.width * self.height) - len(self.taken)

    #### checkers ####

    def legal_add(self, cells):
        for cell in cells:
            if self.check_borders(cell) and cell not in self.get_taken():
                return True
        return False

    def check_borders(self, location):
        x, y = location
        if x < 0 or x >= self.height:
            return False
        if y < 0 or y >= self.width:
            return False
        return True

    def check_empty(self, loc):
        if loc in self.taken:
            return False
        else:
            return True

    #### setters - add ####

    def add_snake(self, snake):
        if self.legal_add(snake.get_coordinates()):
            self.snake = snake

    def add_apple(self):
        location, score = get_apple_parameters()
        while not self.legal_add(location):
            location, score = get_apple_parameters()
        apple = Apple(location, score)
        self.apples.append(apple)

    def add_bomb(self):
        x, y, radius, time = get_bomb_parameters()
        while not self.legal_add((x, y)):
            x, y, radius, time = get_apple_parameters()
        bomb = Bomb(x, y, radius, time)
        self.bombs.append(bomb)

    ## setters - del ##
    def del_bomb(self):
        self.bombs.remove(bomb)

    def del_apple(self, apple):
        self.apples.remove(apple)

    ## setters - update ##
    #todo: needed?
    def move_snake(self, movekey):
        return self.snake.move_snake(movekey)

    def update_taken(self):
        """
        updates taken coordinates (assuming there is no overlap )
        :return:
        """
        self.taken[snake.get_coordinates()] = snake
        for apple in self.get_apples():
            self.taken[apple.get_location()] = apple
        for bomb in self.bombs():
            self.taken[bombs.get_location()] = bomb



