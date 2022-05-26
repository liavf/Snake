import game_parameters
from game_display import GameDisplay

RED = "red"
BLACK = "black"
ORANGE = "orange"
GREEN = "green"
APPLE = "Apple"
BOMB = "Bomb"
SHOCKWAVE = "Shockwave"
SNAKE = "Snake"

COLORS_DICT = {APPLE: GREEN, BOMB: RED, SHOCKWAVE: ORANGE, SNAKE: BLACK}

def main_loop(gd: GameDisplay) -> None:


    gd.show_score(0)
    x, y = 10, 10
    while True:
        key_clicked = gd.get_key_clicked()
        if (key_clicked == 'Left') and (x > 0):
            x -= 1
        elif (key_clicked == 'Right') and (x < game_parameters.WIDTH):
            x += 1
        gd.draw_cell(x, y, "red")
        gd.end_round()


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
