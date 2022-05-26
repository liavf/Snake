from apple import *
from bomb import *
from game_parameters import *

class Board:
    def __init__(self, width, height):
        self.apples = []
        self.bombs = []
        self.width = width
        self.height = height
        self.taken = {}
        self.snake=None

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
        if x < 0 or x >= self.width:
            return False
        if y < 0 or y >= self.height:
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
            for cell in snake.get_coordinates():
                self.taken[cell] = snake

    def add_apple(self):
        x, y, score = get_random_apple_data()
        while not self.legal_add([(x, y)]):
            x, y, score = get_random_apple_data()
        apple = Apple((x, y), score)
        self.apples.append(apple)
        self.taken[(x,y)] = apple

    def add_bomb(self):
        x, y, radius, time = get_random_bomb_data()
        while not self.legal_add([(x, y)]):
            x, y, radius, time = get_random_bomb_data()
        bomb = Bomb((x, y), radius, time)
        self.bombs.append(bomb)
        self.taken[(x,y)] = bomb

    ## setters - del ##
    def del_bomb(self, bomb):
        self.bombs.remove(bomb)

    def del_apple(self, apple):
        self.apples.remove(apple)

    ## setters - update ##
    #todo: needed?
    def move_snake(self, movekey):
        return self.snake.move_snake(movekey)

    def get_taken_coordinates(self):
        return self.taken

    def update_taken(self):
        """
        updates taken coordinates (assuming there is no overlap )
        :return:
        """
        self.taken = {}
        if self.snake is not None:
            for cell in self.snake.get_coordinates():
                if self.check_borders(cell):
                    self.taken[cell] = self.snake
        for apple in self.get_apples():
            self.taken[apple.get_location()] = apple
        for bomb in self.bombs:
            for cell in bomb.get_location():
                if self.check_borders(cell):
                    self.taken[cell] = bomb

    def remove_snake(self):
        self.snake = None



