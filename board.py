
class Board:
    def __init__(self, snake, width, height):
        self.snake = snake
        self.apples = []
        self.bomb = None
        self.width = width
        self.height = height
        self.taken_coordinates = {}

    def legal_add(self, cells):
        for cell in cells:
            if not (self.check_borders(cell) and self.is_empty(cell)):
                return False
        return True

    def check_borders(self, loc):
        x, y = loc
        if x < 0 or x >= self.height:
            return False
        if y < 0 or y >= self.width:
            return False
        return True

    def check_empty(self, loc):
        if loc in self.taken_coordinates.keys():
            return False
        else:
            return True

    def add_snake_to_board(self):
        if self.lagal_add(snake.get_coordinates()):
            for cell in self.snake.get_coordinates():
                self.taken_coordinates[cell] = snake

    def add_apple(self):
        location, score = get_apple_parameters()
        while not self.legal_add(location):
            location, score = get_apple_parameters()
        apple = Apple(location, score)
        self.taken_coordinates[location] = apple
        self.apples.append(apple)

    def add_bomb(self):
        x, y, radius, time = get_bomb_parameters()
        while not self.legal_add((x, y)):
            x, y, radius, time = get_apple_parameters()
        bomb = Bomb(x, y, radius, time)
        self.taken_coordinates[(x, y)] = bomb
        self.bomb = bomb

    def del_bomb(self):
        del self.taken_coordinates[(self.bomb.x, self.bomb.y)]
        self.bomb = None

    def del_apple(self, apple):
        del self.taken_coordinates[apple.location]
        self.apples.remove(apple)

    def get_apples(self):
        return self.apples

    def cell_content(self, location):
        if location in self.taken_coordinates:
            return self.taken_coordinates[location]
        else:
            return None

    def get_empty_cells_num(self):
        return (self.width * self.height) - len(self.taken_coordinates)

    def move_snake(self, movekey):
        return self.snake.move_snake(movekey)


