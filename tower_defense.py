import math
from dataclasses import dataclass

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.uix.label import Label
from kivy.uix.widget import Widget

GRID_SIZE = 10
CELL_SIZE = 50
PATH = [(i, GRID_SIZE // 2) for i in range(GRID_SIZE)]

@dataclass
class Tower:
    x: int
    y: int
    range: int = 2
    damage: int = 10

    def in_range(self, enemy) -> bool:
        return math.hypot(self.x - enemy.x, self.y - enemy.y) <= self.range

@dataclass
class Enemy:
    path_index: int = 0
    health: int = 30

    def move(self):
        if self.path_index + 1 < len(PATH):
            self.path_index += 1

    @property
    def x(self) -> int:
        return PATH[self.path_index][0]

    @property
    def y(self) -> int:
        return PATH[self.path_index][1]

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.towers = []
        self.enemies = []
        self.life = 5
        Clock.schedule_interval(self.update, 1 / 10)
        Clock.schedule_interval(lambda dt: self.spawn_enemy(), 3)
        self.bind(size=lambda *a: self.draw())

    def on_touch_down(self, touch):
        grid_x = int(touch.x // CELL_SIZE)
        grid_y = int(touch.y // CELL_SIZE)
        if (grid_x, grid_y) in PATH:
            return
        if any(t.x == grid_x and t.y == grid_y for t in self.towers):
            return
        self.towers.append(Tower(grid_x, grid_y))
        self.draw()

    def spawn_enemy(self):
        self.enemies.append(Enemy())

    def update(self, dt):
        for enemy in list(self.enemies):
            for tower in self.towers:
                if tower.in_range(enemy):
                    enemy.health -= tower.damage
            if enemy.health <= 0:
                self.enemies.remove(enemy)
                continue
            enemy.move()
            if enemy.path_index == len(PATH) - 1:
                self.life -= 1
                self.enemies.remove(enemy)
                if self.life <= 0:
                    self.game_over()
                    return
        self.draw()

    def game_over(self):
        self.canvas.clear()
        self.add_widget(Label(text="Game Over", font_size=40,
                               center=self.center))
        Clock.unschedule(self.update)

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
                    x1, y1 = i * CELL_SIZE, j * CELL_SIZE
                    Color(0.8, 0.8, 0.8 if (i, j) in PATH else 1)
                    Rectangle(pos=(x1, y1), size=(CELL_SIZE, CELL_SIZE))
            for tower in self.towers:
                Color(0, 0, 1)
                Ellipse(pos=(tower.x * CELL_SIZE + 10,
                               tower.y * CELL_SIZE + 10),
                        size=(CELL_SIZE - 20, CELL_SIZE - 20))
            for enemy in self.enemies:
                x = enemy.x * CELL_SIZE + CELL_SIZE / 2
                y = enemy.y * CELL_SIZE + CELL_SIZE / 2
                Color(1, 0, 0)
                Rectangle(pos=(x - 10, y - 10), size=(20, 20))

class TowerDefenseApp(App):
    def build(self):
        root = GameWidget(size=(GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE))
        return root

if __name__ == "__main__":
    TowerDefenseApp().run()
