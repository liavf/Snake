from game_parameters import *
from game_display import GameDisplay
from bomb import *
from snakey import *
from apple import *
from board import *

RED = "red"
BLACK = "black"
ORANGE = "orange"
GREEN = "green"
APPLE = "Apple"
BOMB = "Bomb"
SHOCKWAVE = "Shockwave"
SNAKE = "Snake"

COLORS_DICT = {APPLE: GREEN, BOMB: RED, SHOCKWAVE: ORANGE, SNAKE: BLACK}

def init_board():
    board = Board(WIDTH, HEIGHT)
    snake = Snake(head=Node(WIDTH//2, HEIGHT//2), direction=UP)
    snake.add_last(Node(WIDTH//2, (HEIGHT//2)-1))
    snake.add_last(Node(WIDTH//2, (HEIGHT//2)-2))
    board.add_snake(snake)
    for i in range(3):
        board.add_apple()
    board.add_bomb()
    return board


def draw_cells(board, gd: GameDisplay):
    """
    Draws board in game display
    :param board: board object
    :param gd:
    :return:
    """
    taken_locations = board.get_taken_coordinates()
    for location in taken_locations:
        if type(taken_locations[location]) == APPLE:
            gd.draw_cell(location[0], location[1], COLORS_DICT[APPLE])
        elif type(taken_locations[location]) == SNAKE:
            gd.draw_cell(location[0], location[1], COLORS_DICT[SNAKE])
        else: #bomb
            if bomb.get_is_shock():
                gd.draw_cell(location[0], location[1], COLORS_DICT[SHOCKWAVE])
            else: #BOMB
                gd.draw_cell(location[0], location[1], COLORS_DICT[BOMB])


def main_loop(gd: GameDisplay) -> None:
    board = init_board()
    #gd.show_score(0)
    is_playing = True
    while is_playing:
        #timers
        if board.snake.get_is_eating():
            board.snake.set_apple_timer(-1)
        movekey = gd.get_key_clicked()
        board.snake.move_snake(movekey)
        head = board.snake.get_head().get_location()
        if not (board.check_borders(head)):
            is_playing = False
        if head in board.get_taken():
            obj = board.taken[head]
            if type(obj) == APPLE:
                gz.score += obj.get_score()
                board.del_apple(obj)
                board.snake.set_apple_timer(3)
            elif type(obj) == BOMB:
                is_playing = False
            elif type(obj) == SNAKE:
                is_playing = False
        board.update_taken()
        for bomb in board.get_bombs:
            bomb.update_timer()
            if bomb.get_is_shock():
                shocks = bomb.get_shock_location()
                for shock in shocks:
                    if shock in board.get_taken():
                        obj = board.taken[shock]
                        if type(obj) == APPLE:
                            board.del_apple(obj)
                        if type(obj) == SNAKE:
                            is_playing = False
            if bomb.finished():
                board.del_bomb(bomb)

        #update
        board.update_taken()
        for i in range(3-len(board.get_apples())):
            board.add_apple()
        for i in range(1-len(board.get_apples())):
            board.add_bomb()

        draw_cells(board)
        gd.end_round()