from math import sin, cos, pi

from pyglet import app
from pyglet import clock
from pyglet import gl
from pyglet import graphics
from pyglet.window import Window
from pyglet.window import mouse

COLUMNS = 7
ROWS = 6
COLUMNS_WIDTH = ROW_HEIGHT = 100
RED_COLOR = (255, 0, 0, 0)
BLUE_COLOR = (0, 0, 255, 0)
GRID_COLOR = RED_COLOR
PIECE_RADIUS = ROW_HEIGHT * 0.4
PLAYER_ONE_COLOR = RED_COLOR
PLAYER_TWO_COLOR = BLUE_COLOR

WIN_WIDTH = COLUMNS * COLUMNS_WIDTH
WIN_HEIGHT = ROWS * ROW_HEIGHT

GRID = [[0] * COLUMNS for i in range(ROWS)]
PIECES_PER_COLUMN = [0] * COLUMNS

LAST_COLUMN_CLICKED = -1
ACTUAL_PLAYER = 1
GAME_OVER = False

window = Window(WIN_WIDTH, WIN_HEIGHT)


@window.event
def on_mouse_press(x, y, button, modifiers):
    global LAST_COLUMN_CLICKED
    if button == mouse.LEFT and LAST_COLUMN_CLICKED == -1:
        LAST_COLUMN_CLICKED = column(x)


def update(dt):
    global LAST_COLUMN_CLICKED, ACTUAL_PLAYER, GAME_OVER
    if GAME_OVER:
        return
    if LAST_COLUMN_CLICKED != -1:
        if PIECES_PER_COLUMN[LAST_COLUMN_CLICKED] < ROWS:
            GRID[PIECES_PER_COLUMN[LAST_COLUMN_CLICKED]][LAST_COLUMN_CLICKED] = ACTUAL_PLAYER
            PIECES_PER_COLUMN[LAST_COLUMN_CLICKED] += 1
            winning_line = get_winning_line()
            if len(winning_line) == 4:
                GAME_OVER = True
            ACTUAL_PLAYER = 2 if ACTUAL_PLAYER == 1 else 1
        LAST_COLUMN_CLICKED = -1


@window.event
def on_draw():
    window.clear()
    draw_grid()
    draw_all_pieces()


def draw_all_pieces():
    for y, row in enumerate(GRID):
        for x, player_piece in enumerate(row):
            if player_piece == 1:
                draw_piece(x, y, PLAYER_ONE_COLOR)
            elif player_piece == 2:
                draw_piece(x, y, PLAYER_TWO_COLOR)


def draw_grid():
    for i in range(COLUMNS):
        draw_line(i * ROW_HEIGHT, 0, i * ROW_HEIGHT, WIN_HEIGHT, color=GRID_COLOR)
    for i in range(ROWS):
        draw_line(0, i * COLUMNS_WIDTH, WIN_WIDTH, i * COLUMNS_WIDTH, color=GRID_COLOR)


def draw_piece(x, y, color=(255, 255, 255, 0)):
    draw_reg_polygon(x * COLUMNS_WIDTH + COLUMNS_WIDTH // 2, y * ROW_HEIGHT + ROW_HEIGHT // 2, PIECE_RADIUS, 64, color)


def draw_reg_polygon(x, y, r, n, color=(255, 255, 255, 0)):
    vertices = []
    th = 0
    for _ in range(n):
        vertices += [x + r * sin(th), y + r * cos(th)]
        th += 2 * pi / n
    graphics.draw(n, gl.GL_POLYGON, ('v2f', vertices), ('c4B', color * n))


def draw_line(x1, y1, x2, y2, color=(255, 255, 255, 0)):
    graphics.draw(2, gl.GL_LINES, ('v2i', (x1, y1, x2, y2)), ('c4B', color * 2))


def get_winning_line():
    for row in range(0, ROWS):
        for col in range(0, 4):
            if all([GRID[row][col] == value and value != 0 for value in GRID[row][col:col + 4]]):
                return (col, row), (col + 1, row), (col + 2, row), (col + 3, row)
    transpose = list(zip(*GRID))
    for col in range(0, COLUMNS):
        for row in range(0, 3):
            if all([transpose[col][row] == value and value != 0 for value in transpose[col][row:row + 4]]):
                return (col, row), (col, row + 1), (col, row + 2), (col, row + 3)
    for row in range(3, ROWS):
        for col in range(0, 4):
            if (GRID[row][col] != 0
                    and GRID[row][col] == GRID[row - 1][col + 1]
                    and GRID[row][col] == GRID[row - 2][col + 2]
                    and GRID[row][col] == GRID[row - 3][col + 3]):
                return (col + 3, row - 3), (col + 2, row - 2), (col + 1, row - 1), (col, row)
    for row in range(3, ROWS):
        for col in range(3, COLUMNS):
            if (GRID[row][col] != 0
                    and GRID[row][col] == GRID[row - 1][col - 1]
                    and GRID[row][col] == GRID[row - 2][col - 2]
                    and GRID[row][col] == GRID[row - 3][col - 3]):
                return (col - 3, row - 3), (col - 2, row - 2), (col - 1, row - 1), (col, row)
    return ()


def column(x):
    return x // COLUMNS_WIDTH


if __name__ == '__main__':
    clock.schedule_interval(update, 1 / 15)
    app.run()
