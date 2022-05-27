
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
BOMB_NUM = 1
APPLE_TIME_ADD = 3
FIRST_SNAKE_NODE = (WIDTH // 2, HEIGHT // 2)
SECOND_SNAKE_NODE = (WIDTH // 2, (HEIGHT // 2) - 1)
THIRD_SNAKE_NODE = (WIDTH // 2, (HEIGHT // 2) - 2)

COLORS_DICT = {APPLE: GREEN, BOMB: RED, SHOCKWAVE: ORANGE, SNAKE: BLACK}

def init_snake() -> Any:
    """
    inits snake with first nodes and direction
    in this game: first three nodes are given and direction is up
    :return: snake object
    """
    snake = Snake(direction=UP, head=Node(FIRST_SNAKE_NODE))
    snake.add_tail(Node(SECOND_SNAKE_NODE))
    snake.add_tail(Node(THIRD_SNAKE_NODE))
    return snake

def init_board() -> Any:
    """
    inits board with given params:
    -one snake (already initialized)
    -one bomb
    -three apples
    :return: board object
    """
    board = Board(WIDTH, HEIGHT)
    snake = init_snake()
    board.add_snake(snake)
    board.add_bomb()
    for i in range(APPLE_NUM):
        board.add_apple()
    return board

def draw_cells(gd: GameDisplay, board: Board) -> None:
    """
    Draws board in game display according
    :param gd: game display object
    :param board: board object
    """
    locations = board.get_taken_coordinates()
    for location in locations:
        x, y = location
        obj = board.cell_content(location)
        obj_type = type(obj).__name__
        if obj_type == BOMB and obj.is_shock():
            color = COLORS_DICT[SHOCKWAVE]
        else:
            color = COLORS_DICT[obj_type]
        gd.draw_cell(x, y, color)

def get_movekey(gd: GameDisplay, board: Board) -> str:
    """
    gets user's keyboard choice if given
    if none is given or key is illegal, continues with current
    :param gd: game display object
    :param board: current game board
    :return: movekey
    """
    movekey = gd.get_key_clicked()
    if movekey is None or not board.get_snake().is_legal_direction(movekey):
        movekey = board.get_snake().get_direction()
    return movekey

def apple_logic(gd: GameDisplay, board: Board, apple: Apple, cur_score: int) -> int:
    """
    if snake ate apple, fo the following:
    -update score
    -remove apple
    -set apple timer - for next 3 rounds dont remove tail
    :param apple: apple landed on
    :param cur_score: current score
    :return: updated score
    """
    cur_score += apple.get_score()
    gd.show_score(cur_score)
    board.del_apple(apple)
    board.get_snake().add_to_apple_timer(APPLE_TIME_ADD)
    return cur_score

def head_landing_logic(board: Board, is_playing: bool, cur_score: int, gd) -> Tuple[bool, int]:
    """
    handles head logic:
    -checks if in borders
    -if it landed on something, call head_in_taken function
    updates board after checking
    :return: updated score and if still playing
    """
    head_loc = board.get_snake().get_head().get_location()
    if not board.in_borders(head_loc):
        is_playing = False
    if head_loc in board.get_taken():
        is_playing, cur_score = head_in_taken(gd, board, head_loc, cur_score, is_playing)
    board.update_taken()
    return is_playing, cur_score

def head_in_taken(gd: GameDisplay, board: Board, head: Location, cur_score: int, is_playing: bool) -> Tuple[bool, int]:
    """
    if head landed on something, react accordingly
    :param head: head location
    :return: again, current score and if still playing
    """
    obj = board.cell_content(head)
    obj_type = type(obj).__name__
    if obj_type == APPLE:
        cur_score = apple_logic(gd, board, obj, cur_score)
    elif obj_type == BOMB:
        board.get_snake().rem_node(head)
        # board.update_location(head, obj)
        is_playing = False
    elif obj_type == SNAKE:
        # check if location is in updated coordinates -
        # if tail just left location it is legal
        if head in obj.get_coordinates()[1:]:
            is_playing = False
    return is_playing, cur_score

def shock_logic(shocks: List[Location], board: Board, hit: bool, is_playing: bool) -> Tuple[bool, bool]:
    """
    if bomb is in shock, checks to see if shock hit something
    :param shocks: all shock waves
    :param board: current board
    :param hit: did bomb hit
    :param is_playing: is still playing
    :return: hit, is_playing
    """
    for shock in shocks:
        if shock in board.get_taken():
            obj = board.cell_content(shock)
            if type(obj).__name__ == APPLE:
                board.del_apple(obj)
            if type(obj).__name__ == SNAKE:
                board.get_snake().rem_node(shock)
                hit = True
                is_playing = False
    return hit, is_playing

def bomb_logic(board: Board, is_playing: bool) -> bool:
    """
    after moving snake, update bomb timers
    now, check if the shockwave landed on something
    also, removes finished bombs
    :return: is still alive
    """
    hit = False
    for bomb in board.get_bombs():
        bomb.update_timer()
        if bomb.is_shock():
            shocks = bomb.get_shock_location()
            hit, is_playing = shock_logic(shocks, board, hit, is_playing)
        if bomb.finished() and not hit:
            board.del_bomb(bomb)
            if not board.add_bomb():  # no more place for bomb
                is_playing = False
    board.update_taken()
    return is_playing

def fill_missing_objects(board: Board, is_playing: bool) -> bool:
    """
    fills the bomb and apple capacity
    if board is empty, end game
    :return: is finished
    """
    for i in range(APPLE_NUM - len(board.get_apples())):
        if not board.add_apple() and (len(board.get_apples()) == 0):  # no more place for apple
            is_playing = False
    return is_playing

def main_loop(gd: GameDisplay) -> None:
    """
    this is the main loop of the game
    every round, the user presses a key and the snake moves accrodingly
    the board us updated and printed
    :param gd: game display object
    """
    board = init_board()
    is_playing = True
    cur_score = 0
    gd.show_score(cur_score)
    draw_cells(gd, board)
    gd.end_round()
    while is_playing:
        movekey = get_movekey(gd, board)
        board.get_snake().move_snake(movekey)
        board.get_snake().update_apple_timer()
        is_playing, cur_score = head_landing_logic(board, is_playing, cur_score, gd)
        if is_playing:
            is_playing = bomb_logic(board, is_playing)
        is_playing = fill_missing_objects(board, is_playing)
        draw_cells(gd, board)
        gd.end_round()