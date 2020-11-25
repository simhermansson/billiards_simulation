import pygame
import ball
import pool_table


if __name__ == '__main__':
    # Pygame code
    pygame.init()
    game_display = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pool")
    clock = pygame.time.Clock()

    # Game specific variables
    pool_table = pool_table.PoolTable(800, 600)

    sprite_group = pygame.sprite.Group()
    b1 = ball.Ball(pool_table, 330, 110)
    b2 = ball.Ball(pool_table, 370, 350)
    sprite_group.add(b1)
    sprite_group.add(b2)

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.BUTTON_LEFT:
                pass

        sprite_group.update()

        game_display.fill("BLACK")
        pool_table.draw(game_display)
        sprite_group.draw(game_display)

        for a in sprite_group:
            for b in sprite_group:
                if a != b and pygame.sprite.collide_circle(a, b):
                    ball.collision(a, b)

        pygame.display.update()
        clock.tick(60)
