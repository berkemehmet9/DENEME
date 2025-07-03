import tkinter as tk
from dataclasses import dataclass
import math
import random

GRID_SIZE = 10
CELL_SIZE = 50
CANVAS_WIDTH = GRID_SIZE * CELL_SIZE
CANVAS_HEIGHT = GRID_SIZE * CELL_SIZE

PATH = [(i, GRID_SIZE//2) for i in range(GRID_SIZE)]

@dataclass
class Tower:
    x: int
    y: int
    range: int = 2
    damage: int = 10
    def in_range(self, enemy):
        return math.hypot(self.x - enemy.x, self.y - enemy.y) <= self.range

@dataclass
class Enemy:
    path_index: int = 0
    health: int = 30
    def move(self):
        if self.path_index + 1 < len(PATH):
            self.path_index += 1
    @property
    def x(self):
        return PATH[self.path_index][0]
    @property
    def y(self):
        return PATH[self.path_index][1]

class Game(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.canvas = tk.Canvas(self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='white')
        self.canvas.pack()
        self.towers = []
        self.enemies = []
        self.life = 5
        self.master.after(1000, self.spawn_enemy)
        self.master.after(200, self.game_loop)
        self.canvas.bind('<Button-1>', self.place_tower)
        self.draw_grid()

    def draw_grid(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                x1, y1 = i * CELL_SIZE, j * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                fill = 'lightgray' if (i, j) in PATH else 'white'
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline='gray')

    def place_tower(self, event):
        grid_x = event.x // CELL_SIZE
        grid_y = event.y // CELL_SIZE
        if (grid_x, grid_y) in PATH:
            return
        if any(t.x == grid_x and t.y == grid_y for t in self.towers):
            return
        tower = Tower(grid_x, grid_y)
        self.towers.append(tower)
        self.canvas.create_oval(grid_x*CELL_SIZE+10, grid_y*CELL_SIZE+10,
                                (grid_x+1)*CELL_SIZE-10, (grid_y+1)*CELL_SIZE-10,
                                fill='blue')

    def spawn_enemy(self):
        self.enemies.append(Enemy())
        self.master.after(3000, self.spawn_enemy)

    def game_loop(self):
        self.canvas.delete('enemy')
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
            x, y = enemy.x * CELL_SIZE + CELL_SIZE//2, enemy.y * CELL_SIZE + CELL_SIZE//2
            self.canvas.create_rectangle(x-10, y-10, x+10, y+10, fill='red', tags='enemy')
        self.master.after(200, self.game_loop)

    def game_over(self):
        self.canvas.delete('all')
        self.canvas.create_text(CANVAS_WIDTH//2, CANVAS_HEIGHT//2, text='Game Over', font=('Arial', 24))

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Tower Defense')
    game = Game(master=root)
    game.mainloop()
