import pygame


class PoolTable(pygame.sprite.Sprite):
    def __init__(self, screen_width: int, screen_height: int):
        pygame.sprite.Sprite.__init__(self)

        self.BORDER = screen_width // 10
        self.HEIGHT = screen_height - self.BORDER
        self.WIDTH = self.HEIGHT // 2

        self.image = pygame.Surface([self.WIDTH, self.HEIGHT])
        self.image.fill("GREEN")
        self.rect = self.image.get_rect(center=(screen_width // 2, screen_height // 2))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def get_left_edge(self) -> int:
        return self.rect.left

    def get_right_edge(self) -> int:
        return self.rect.right

    def get_top_edge(self) -> int:
        return self.rect.top

    def get_bottom_edge(self) -> int:
        return self.rect.bottom
