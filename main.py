import pygame
import ball
import pool_table
import cue


if __name__ == '__main__':
    pygame.init()
    game_display = pygame.display.set_mode((1600, 900))
    pygame.display.set_caption("Pool")
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)

    # Game variables.
    pool_table = pool_table.PoolTable(game_display.get_width(), game_display.get_height())
    cue = cue.Cue()

    # Spawn balls.
    sprite_group = pygame.sprite.Group()
    b1 = ball.Ball(pool_table, 700, 110, True)
    b2 = ball.Ball(pool_table, 770, 350, True)
    b3 = ball.Ball(pool_table, 750, 210, True)
    b4 = ball.Ball(pool_table, 800, 110, True)
    b5 = ball.Ball(pool_table, 800, 150, True)
    b6 = ball.Ball(pool_table, 800, 300, True)

    sprite_group = pygame.sprite.Group()
    sprite_group.add(b1)
    sprite_group.add(b2)
    sprite_group.add(b3)
    sprite_group.add(b4)
    sprite_group.add(b5)
    sprite_group.add(b6)

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.BUTTON_LEFT:
                pass

        sprite_group.update()
        pool_table.update(sprite_group)
        cue.update(sprite_group)

        game_display.fill("GRAY")
        pool_table.draw(game_display)
        #sprite_group.draw(game_display)
        cue.draw(game_display)

        collided = dict()
        for a in sprite_group:
            for b in sprite_group:
                if a != b and ball.overlaps(a, b) and b not in collided.get(a, []):
                    collided[b] = collided.get(b, []) + [a]
                    ball.collision(a, b)
                    #print("Crash bang oww!")

        for b in sprite_group:
            b.draw_self(game_display)

        pygame.display.update()
        delta_time = clock.tick(60)
