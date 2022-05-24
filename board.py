
class Board:
    def __init__(self, snake, width, height):
        self.snake = snake
        self.apples = []
        self.bombs = []
        self.width = width
        self.height = height
        self.taken = {}

    def legal_add(self, cell):
        if self.check_borders(cell) and

    def check_borders(self, loc):
        x, y = loc
        if x < 0 or x >= self.height:
            return False
        if y < 0 or y >= self.width:
            return False
        return True

    def check_empty(self, loc):

    def add_snake_to_board(self):
        for cell in self.snake.get_coordinates():
            self.taken[]


    def add_apple(self, apple):

    def add_bomb(self, apple):

    def move_snake(self, movekey):
        move_requiremnet
        snake.move
        update_board

    def del_bomb(self):

    def del_apple(self):

    def get_apples(self):
        return self.apples

    def cell_content

    def get_empty_cells

    def taken_locations
        dict[location] = object
        bomb more than one

    def check_borders

    def check_empty

    def check_legal_cells
        is boreders
        is empty

