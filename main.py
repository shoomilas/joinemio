from game_window import GameWindow
from pyglet import clock
from pyglet import app


def main():
    window = GameWindow()
    clock.schedule_interval(window.update, GameWindow.refresh_rate)
    app.run()


if __name__ == "__main__":
    main()
