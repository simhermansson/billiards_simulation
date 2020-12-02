import pygame
import pygame.gfxdraw
import math


class PoolPocket(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        """
        :param x: X position of origin.
        :param y: Y position of origin.
        """
        pygame.sprite.Sprite.__init__(self)

        self.RADIUS = self.get_radius()

        self.image = pygame.Surface([self.RADIUS*2 + 1, self.RADIUS*2 + 1], pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))

        pygame.gfxdraw.aacircle(self.image, self.image.get_rect().centerx, self.image.get_rect().centery,
                                self.RADIUS, (0, 0, 0))
        pygame.gfxdraw.filled_circle(self.image, self.image.get_rect().centerx, self.image.get_rect().centery,
                                     self.RADIUS, (0, 0, 0))

    def distance(self, ball):
        return math.sqrt((self.rect.centerx - ball.get_center_x())**2 + (self.rect.centery - ball.get_center_y())**2)

    def overlap(self, b):
        return self.distance(b) <= self.get_radius()

    @staticmethod
    def get_radius():
        return 30


class PoolTable(pygame.sprite.Sprite):
    def __init__(self, screen_width: int, screen_height: int):
        pygame.sprite.Sprite.__init__(self)

        self.EDGE_BORDER = screen_width // 10
        self.HEIGHT = screen_height - self.EDGE_BORDER
        self.WIDTH = self.HEIGHT // 2
        self.FRICTION = 0.01

        self.table = pygame.Surface([self.WIDTH, self.HEIGHT])
        self.table.fill((54, 89, 74))
        self.rect = self.table.get_rect(center=(screen_width // 2, screen_height // 2))

        self.border_size = PoolPocket.get_radius() * 3
        self.border = pygame.Surface([self.WIDTH + self.border_size, self.HEIGHT + self.border_size])
        self.border.fill((133, 94, 66))
        self.border_rect = self.border.get_rect(center=(screen_width // 2, screen_height // 2))

        self.pocket_group = pygame.sprite.Group()
        self.pocket_group.add(PoolPocket(self.rect.left, self.rect.top))
        self.pocket_group.add(PoolPocket(self.rect.left, self.rect.centery))
        self.pocket_group.add(PoolPocket(self.rect.left, self.rect.bottom))
        self.pocket_group.add(PoolPocket(self.rect.right, self.rect.top))
        self.pocket_group.add(PoolPocket(self.rect.right, self.rect.centery))
        self.pocket_group.add(PoolPocket(self.rect.right, self.rect.bottom))

    def update(self, balls):
        for pocket in self.pocket_group:
            for ball in balls:
                if pocket.overlap(ball):
                    ball.kill()

    def draw(self, screen):
        screen.blit(self.border, self.border_rect)
        screen.blit(self.table, self.rect)
        self.pocket_group.draw(screen)

    def get_friction(self):
        return self.FRICTION

    def get_left_edge(self) -> int:
        return self.rect.left

    def get_right_edge(self) -> int:
        return self.rect.right

    def get_top_edge(self) -> int:
        return self.rect.top

    def get_bottom_edge(self) -> int:
        return self.rect.bottom
