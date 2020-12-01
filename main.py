import pygame
import ball
import pool_table
import cue


if __name__ == '__main__':
    # Pygame code
    pygame.init()
    game_display = pygame.display.set_mode((1600, 900))
    pygame.display.set_caption("Pool")
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)

    # Game specific variables
    pool_table = pool_table.PoolTable(game_display.get_width(), game_display.get_height())
    cue = cue.Cue()

    sprite_group = pygame.sprite.Group()
    b1 = ball.Ball(pool_table, 700, 110, True)
    b2 = ball.Ball(pool_table, 770, 350, True)
    b3 = ball.Ball(pool_table, 750, 210, True)
    sprite_group.add(b1)
    sprite_group.add(b2)
    sprite_group.add(b3)

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.BUTTON_LEFT:
                pass

        sprite_group.update()
        cue.update()

        game_display.fill("GRAY")
        pool_table.draw(game_display)
        sprite_group.draw(game_display)
        cue.draw(game_display, sprite_group)

        collided = dict()
        for a in sprite_group:
            for b in sprite_group:
                if a != b and ball.overlap(a, b) and b not in collided.get(a, []):
                    collided[b] = collided.get(b, []) + [a]
                    ball.collision(a, b)
                    print("Crash bang oww!")

        pygame.display.update()
        clock.tick(60)
