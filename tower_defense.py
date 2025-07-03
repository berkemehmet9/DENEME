import pygame
import sys
import random

# Game settings
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Tower settings
TOWER_RANGE = 150
TOWER_FIRE_RATE = 30  # frames per shot

# Enemy settings
ENEMY_SPEED = 2
ENEMY_HEALTH = 3

class Enemy(pygame.sprite.Sprite):
    def __init__(self, path):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.path = path
        self.path_index = 0
        self.rect.center = self.path[self.path_index]
        self.health = ENEMY_HEALTH

    def update(self):
        if self.path_index < len(self.path) - 1:
            target = self.path[self.path_index + 1]
            dx, dy = target[0] - self.rect.centerx, target[1] - self.rect.centery
            dist = (dx**2 + dy**2) ** 0.5
            if dist != 0:
                dx, dy = dx / dist, dy / dist
                self.rect.centerx += dx * ENEMY_SPEED
                self.rect.centery += dy * ENEMY_SPEED
            if dist < ENEMY_SPEED:
                self.path_index += 1
        else:
            # Reached end
            self.kill()

class Tower(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=pos)
        self.range = TOWER_RANGE
        self.fire_rate = TOWER_FIRE_RATE
        self.timer = 0

    def update(self):
        self.timer += 1

    def shoot(self, enemies, projectiles_group):
        if self.timer >= self.fire_rate:
            for enemy in enemies:
                if self.in_range(enemy):
                    projectile = Projectile(self.rect.center, enemy)
                    projectiles_group.add(projectile)
                    self.timer = 0
                    break

    def in_range(self, enemy):
        dx = self.rect.centerx - enemy.rect.centerx
        dy = self.rect.centery - enemy.rect.centery
        return dx * dx + dy * dy <= self.range * self.range

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, target):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=pos)
        self.target = target
        self.speed = 5

    def update(self):
        if not self.target.alive():
            self.kill()
            return
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        dist = (dx**2 + dy**2) ** 0.5
        if dist != 0:
            dx, dy = dx / dist, dy / dist
            self.rect.centerx += dx * self.speed
            self.rect.centery += dy * self.speed
        if self.rect.colliderect(self.target.rect):
            self.target.health -= 1
            if self.target.health <= 0:
                self.target.kill()
            self.kill()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Define path from left to right
    path = [(0, HEIGHT // 2), (WIDTH, HEIGHT // 2)]

    enemies = pygame.sprite.Group()
    towers = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()

    # Place a tower in the middle
    towers.add(Tower((WIDTH // 2, HEIGHT // 2 - 100)))

    spawn_timer = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                towers.add(Tower(event.pos))

        if spawn_timer <= 0:
            enemies.add(Enemy(path))
            spawn_timer = 120
        spawn_timer -= 1

        towers.update()
        enemies.update()
        projectiles.update()

        for tower in towers:
            tower.shoot(enemies, projectiles)

        screen.fill(WHITE)
        for pos in path:
            pygame.draw.circle(screen, BLACK, pos, 5)
        enemies.draw(screen)
        towers.draw(screen)
        projectiles.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
