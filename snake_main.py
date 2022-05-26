
from game_display import GameDisplay
from snake import *
from board import *

RED = "red"
BLACK = "black"
ORANGE = "orange"
GREEN = "green"
APPLE = "Apple"
BOMB = "Bomb"
SHOCKWAVE = "Shockwave"
SNAKE = "Snake"

APPLE_NUM = 3

COLORS_DICT = {APPLE: GREEN, BOMB: RED, SHOCKWAVE: ORANGE, SNAKE: BLACK}

def init_board():
    board = Board(WIDTH, HEIGHT)
    snake = Snake(head=Node((WIDTH//2, HEIGHT//2)))
    snake.add_last(Node((WIDTH//2, (HEIGHT//2)-1)))
    snake.add_last(Node((WIDTH//2, (HEIGHT//2)-2)))
    board.add_snake(snake)
    for i in range(APPLE_NUM):
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
        x, y = location
        obj = taken_locations[location]
        if type(obj).__name__ == APPLE:
            gd.draw_cell(x, y, COLORS_DICT[APPLE])
        elif type(obj).__name__ == SNAKE:
            gd.draw_cell(x, y, COLORS_DICT[SNAKE])
        elif type(obj).__name__ == BOMB:
            if obj.get_is_shock():
                gd.draw_cell(x, y, COLORS_DICT[SHOCKWAVE])
            else: #BOMB
                gd.draw_cell(x, y, COLORS_DICT[BOMB])


def main_loop(gd: GameDisplay) -> None:
    board = init_board()
    is_playing = True
    cur_score = 0
    gd.show_score(cur_score)
    while is_playing:
        # draw_cells(board, gd)
        movekey = gd.get_key_clicked()
        if movekey is None or not board.snake.is_legal_direction(movekey):
            movekey = board.snake.direction
        board.snake.move_snake(movekey)
        if board.snake.get_is_eating():
            board.snake.update_apple_timer()
        head = board.snake.get_head().get_location()
        if not (board.in_borders(head)):
            is_playing = False
        if head in board.get_taken():
            obj = board.taken[head]
            if type(obj).__name__ == APPLE:
                cur_score += obj.get_score()
                gd.show_score(cur_score)
                board.del_apple(obj)
                board.snake.set_apple_timer(3)
            elif type(obj).__name__ == BOMB:
                board.taken[head] = obj
                is_playing = False
            elif type(obj).__name__ == SNAKE and not obj == head:
                is_playing = False
        board.update_taken()
        for bomb in board.get_bombs():
            bomb.update_timer()
            if bomb.get_is_shock():
                shocks = bomb.get_shock_location()
                for shock in shocks:
                    if shock in board.get_taken():
                        obj = board.taken[shock]
                        if type(obj).__name__ == APPLE:
                            board.del_apple(obj)
                        if type(obj).__name__ == SNAKE:
                            board.taken[head] = obj
                            is_playing = False
            if bomb.finished():
                board.del_bomb(bomb)

        #update
        board.update_taken()
        for i in range(3-len(board.get_apples())):
            if not board.add_apple(): # no more place for apple
                is_playing = False
        for i in range(1-len(board.get_bombs())):
            if not board.add_bomb(): # no more place for bomb
                is_playing = False

        draw_cells(board, gd)


        gd.end_round()
    # draw_cells(board, gd)
    # gd.end_round()