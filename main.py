import math
import pygame


def game_loop():
    pass


if __name__ == '__main__':
    pygame.init()
    gameDisplay = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pool")
    clock = pygame.time.Clock()

    game_loop()
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.BUTTON_LEFT:
                pass

        pygame.display.update()
        clock.tick(60)
