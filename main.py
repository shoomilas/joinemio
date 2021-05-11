from math import sin, cos, pi
from pyglet import app
from pyglet import clock
from pyglet import gl
from pyglet import graphics
from pyglet.window import Window
from pyglet.window import mouse

def column(x):
    return x // Game.columns_width

# TODO: base the game logic on a numpy matrix 
class Game:
    columns = 7
    rows = 6
    columns_width = row_height = 100
    red_color = (255, 0, 0, 0)
    blue_color = (0, 0, 255, 0)
    grid_color = red_color
    piece_radius = row_height * 0.4
    player_one_color = red_color
    player_two_color = blue_color
    win_width = columns * columns_width
    win_height = rows * row_height
    pieces_per_column = [0] * columns
    
    def __init__(self):
        self.grid = [[0] * Game.columns for i in range(Game.rows)]
        self.last_column_clicked = -1
        self.current_player = 1
        self.game_over = False
    
    # TODO: refactor into simpler method calls | simplify grid iteration
    def get_winning_line(self):
        for row in range(0, Game.rows):
            for col in range(0, 4):
                if all([game.grid[row][col] == value and value != 0 for value in game.grid[row][col:col + 4]]):
                    return (col, row), (col + 1, row), (col + 2, row), (col + 3, row)
        transpose = list(zip(*game.grid))
        for col in range(0, Game.columns):
            for row in range(0, 3):
                if all([transpose[col][row] == value and value != 0 for value in transpose[col][row:row + 4]]):
                    return (col, row), (col, row + 1), (col, row + 2), (col, row + 3)
        for row in range(3, Game.rows):
            for col in range(0, 4):
                if (game.grid[row][col] != 0
                        and game.grid[row][col] == game.grid[row - 1][col + 1]
                        and game.grid[row][col] == game.grid[row - 2][col + 2]
                        and game.grid[row][col] == game.grid[row - 3][col + 3]):
                    return (col + 3, row - 3), (col + 2, row - 2), (col + 1, row - 1), (col, row)
        for row in range(3, Game.rows):
            for col in range(3, Game.columns):
                if (game.grid[row][col] != 0
                        and game.grid[row][col] == game.grid[row - 1][col - 1]
                        and game.grid[row][col] == game.grid[row - 2][col - 2]
                        and game.grid[row][col] == game.grid[row - 3][col - 3]):
                    return (col - 3, row - 3), (col - 2, row - 2), (col - 1, row - 1), (col, row)
        return ()

    # TODO: simplify the ifology
    def update(self, dt):
    # global game.last_column_clicked, game.current_player, game.game_over
        if game.game_over:
            return
        if game.last_column_clicked != -1:
            if Game.pieces_per_column[game.last_column_clicked] < Game.rows:
                game.grid[Game.pieces_per_column[game.last_column_clicked]][game.last_column_clicked] = game.current_player
                Game.pieces_per_column[game.last_column_clicked] += 1
                winning_line = game.get_winning_line()
                if len(winning_line) == 4:
                    game.game_over = True
                game.current_player = 2 if game.current_player == 1 else 1
            game.last_column_clicked = -1

# TODO: coś z tym poniżej

game = Game()
window = Window(Game.win_width, Game.win_height)

# class Render:
@window.event
def on_mouse_press(x, y, button, modifiers):
    # global game.last_column_clicked
    if button == mouse.LEFT and game.last_column_clicked == -1:
        game.last_column_clicked = column(x)

@window.event
def on_draw():
    window.clear()
    draw_grid()
    draw_all_pieces()

def draw_all_pieces():
    for y, row in enumerate(game.grid):
        for x, player_piece in enumerate(row):
            if player_piece == 1:
                draw_piece(x, y, Game.player_one_color)
            elif player_piece == 2:
                draw_piece(x, y, Game.player_two_color)


def draw_grid():
    for i in range(Game.columns):
        draw_line(i * Game.row_height, 0, i * Game.row_height, Game.win_height, color=game.grid_color)
    for i in range(Game.rows):
        draw_line(0, i * Game.columns_width, Game.win_width, i * Game.columns_width, color=game.grid_color)


def draw_piece(x, y, color=(255, 255, 255, 0)):
    draw_reg_polygon(x * Game.columns_width + Game.columns_width // 2, y * Game.row_height + Game.row_height // 2, Game.piece_radius, 64, color)


def draw_reg_polygon(x, y, r, n, color=(255, 255, 255, 0)):
    vertices = []
    th = 0
    for _ in range(n):
        vertices += [x + r * sin(th), y + r * cos(th)]
        th += 2 * pi / n
    graphics.draw(n, gl.GL_POLYGON, ('v2f', vertices), ('c4B', color * n))


def draw_line(x1, y1, x2, y2, color=(255, 255, 255, 0)):
    graphics.draw(2, gl.GL_LINES, ('v2i', (x1, y1, x2, y2)), ('c4B', color * 2))



if __name__ == '__main__':
    clock.schedule_interval(game.update, 1 / 15)
    app.run()

