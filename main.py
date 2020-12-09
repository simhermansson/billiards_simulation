import pygame
import ball
import pool_table
import cue

"""
Simulates a billiards game, where balls interact with each other through elastic collisions with the effect
of friction. To set a ball in motion, place the cursor near the ball you want fired and take aim.
The force applied grows as the distance from the ball and cue increases.
"""


def run_game(game_display, game_clock):
    game_table = pool_table.PoolTable(game_display.get_width(), game_display.get_height())
    game_cue = cue.Cue()

    # Spawn balls.
    b1 = ball.Ball(game_table, 800, 400, "red")
    b2 = ball.Ball(game_table, 770, 360, "blue")
    b3 = ball.Ball(game_table, 830, 360, "green")
    b4 = ball.Ball(game_table, 800, 310, "black")
    b5 = ball.Ball(game_table, 750, 310, "brown")
    b6 = ball.Ball(game_table, 850, 310, "pink")
    white = ball.Ball(game_table, 800, 700, "white")

    sprite_group = pygame.sprite.Group()
    sprite_group.add(b1)
    sprite_group.add(b2)
    sprite_group.add(b3)
    sprite_group.add(b4)
    sprite_group.add(b5)
    sprite_group.add(b6)
    sprite_group.add(white)

    running = True
    while running:
        delta_time = game_clock.tick(60) / 10

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if not sprite_group:
            running = False

        # Update game.
        sprite_group.update(delta_time)
        game_table.update(sprite_group)
        game_cue.update(sprite_group)

        # Draw game.
        game_display.fill("GRAY")
        game_table.draw(game_display)
        game_cue.draw(game_display)

        """
        Checks collisions between balls, maintains a dict during this update, so the collision
        between ball a and b only happens once, and the collision between ball b and a is not
        handled separately.
        """
        collided = dict()
        for a in sprite_group:
            for b in sprite_group:
                if a != b and ball.overlaps(a, b) and b not in collided.get(a, []):
                    collided[b] = collided.get(b, []) + [a]
                    ball.collision(a, b)

        for b in sprite_group:
            b.draw_self(game_display)

        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    display = pygame.display.set_mode((1600, 900))
    pygame.display.set_caption("Pool")
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)

    while True:
        run_game(display, clock)

