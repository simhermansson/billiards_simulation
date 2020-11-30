import pygame
import pygame.gfxdraw
import pool_table
import random


class Ball(pygame.sprite.Sprite):
    def __init__(self, table: pool_table, x: int, y: int):
        pygame.sprite.Sprite.__init__(self)

        self.table = table

        self.RADIUS = 20    # mm
        self.MASS = 0.16   # kg

        self.image = pygame.Surface([self.RADIUS*2 + 1, self.RADIUS*2 + 1], pygame.SRCALPHA)
        self.dx = random.randint(0, 1)
        self.dy = random.randint(0, 1)
        self.rect = self.image.get_rect(center=(x, y))

        pygame.gfxdraw.aacircle(self.image, self.image.get_rect().centerx, self.image.get_rect().centery,
                                self.RADIUS, (255, 255, 255))
        pygame.gfxdraw.filled_circle(self.image, self.image.get_rect().centerx, self.image.get_rect().centery,
                                     self.RADIUS, (255, 255, 255))

    def update(self, *args, **kwargs) -> None:
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.left < self.table.get_left_edge():
            self.dx = -self.dx
            self.rect.x += 2 * (self.table.get_left_edge() - self.rect.left)
        elif self.rect.right > self.table.get_right_edge():
            self.dx = -self.dx
            self.rect.x -= 2 * (self.rect.right - self.table.get_right_edge())
        elif self.rect.top < self.table.get_top_edge():
            self.dy = -self.dy
            self.rect.y += 2 * (self.table.get_top_edge() - self.rect.top)
        elif self.rect.bottom > self.table.get_bottom_edge():
            self.dy = -self.dy
            self.rect.y -= 2 * (self.rect.bottom - self.table.get_bottom_edge())

    def get_center_x(self):
        return self.rect.centerx

    def get_center_y(self):
        return self.rect.centery


def collision(a: pygame.sprite.Sprite, b: pygame.sprite.Sprite):
    pass