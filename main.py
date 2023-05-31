import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.graphics import Color as Clr
from kivy.uix.widget import Widget
from pygame.locals import *
import pygame
import random

# Define constants
CELL_SIZE = 20
BOARD_WIDTH = Window.width // CELL_SIZE
BOARD_HEIGHT = Window.height // CELL_SIZE
SNAKE_START_LENGTH = 3
SNAKE_START_POSITION = (BOARD_WIDTH // 2, BOARD_HEIGHT // 2)
SNAKE_START_DIRECTION = (1, 0)
FOOD_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
BACKGROUND_COLOR = (0, 0, 0)
FPS = 10

# Initialize Pygame
pygame.init()

# Define classes
class Snake:
    def __init__(self, position, direction, length):
        self.position = position
        self.direction = direction
        self.length = length
        self.body = [position] * length

    def move(self):
        x, y = self.position
        dx, dy = self.direction
        self.position = (x + dx, y + dy)
        self.body.insert(0, self.position)
        self.body.pop()

    def change_direction(self, direction):
        if direction[0] != -self.direction[0] or direction[1] != -self.direction[1]:
            self.direction = direction

    def draw(self, canvas):
        for x, y in self.body:
            canvas.add(Clr(*SNAKE_COLOR))
            canvas.add(Rectangle(pos=(x * CELL_SIZE, y * CELL_SIZE), size=(CELL_SIZE, CELL_SIZE)))

    def check_collision(self):
        x, y = self.position
        if x < 0 or x >= BOARD_WIDTH or y < 0 or y >= BOARD_HEIGHT:
            return True
        for i, (bx, by) in enumerate(self.body[1:], 1):
            if x == bx and y == by:
                return True
        return False

class Food:
    def __init__(self):
        self.position = (random.randint(0, BOARD_WIDTH - 1), random.randint(0, BOARD_HEIGHT - 1))

    def draw(self, canvas):
        x, y = self.position
        canvas.add(Clr(*FOOD_COLOR))
        canvas.add(Rectangle(pos=(x * CELL_SIZE, y * CELL_SIZE), size=(CELL_SIZE, CELL_SIZE)))

from kivy.uix.label import Label

class SnakeGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.snake = Snake(SNAKE_START_POSITION, SNAKE_START_DIRECTION, SNAKE_START_LENGTH)
        self.food = Food()
        self.score = 0
        self.game_over = False
        self.canvas = self._init_canvas()
        self.score_label = Label(text=f"[color=0000FF]Score: {self.score}", pos=(0, Window.height - 50), size=(Window.width, 50))
        self.add_widget(self.score_label)
        self._update_canvas()

    def _init_canvas(self):
        canvas = self.canvas
        canvas.clear()
        canvas.add(Clr(*BACKGROUND_COLOR))
        canvas.add(Rectangle(pos=self.pos, size=self.size))
        return canvas

    def _update_canvas(self):
        self.canvas.clear()
        self.canvas.add(Clr(*BACKGROUND_COLOR))
        self.canvas.add(Rectangle(pos=self.pos, size=self.size))
        self.snake.draw(self.canvas)
        self.food.draw(self.canvas)

    def on_touch_down(self, touch):
        x, y = touch.pos
        dx, dy = self.snake.direction
        if abs(x - self.snake.position[0] * CELL_SIZE) > abs(y - self.snake.position[1] * CELL_SIZE):
            if x > self.snake.position[0] * CELL_SIZE:
                self.snake.change_direction((1, 0))
            else:
                self.snake.change_direction((-1, 0))
        else:
            if y > self.snake.position[1] * CELL_SIZE:
                self.snake.change_direction((0, 1))
            else:
                self.snake.change_direction((0, -1))

    def update(self, dt):
        if self.game_over:
            return
        self.snake.move()
        if self.snake.check_collision():
            self.game_over = True
            return
        if self.snake.position == self.food.position:
            self.score += 1
            self.snake.length += 1
            x, y = self.snake.position
            dx, dy = self.snake.position
            self.snake.body.insert(0, (x + dx, y + dy))
            self.food = Food()
            self.score_label.text = f"Score: {self.score}"
        self._update_canvas()

class SnakeApp(App):
    def build(self):
        game = SnakeGame()
        Clock.schedule_interval(game.update, 1.0 / FPS)
        return game

if __name__ == '__main__':
    SnakeApp().run()