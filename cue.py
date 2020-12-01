import pygame
import pygame.gfxdraw
import math


class Cue(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 0
        self.y = 0

    def update(self, *args, **kwargs) -> None:
        left = pygame.mouse.get_pressed(num_buttons=3)
        if True:
            self.x, self.y = pygame.mouse.get_pos()

    def draw(self, screen, ball_group):
        nearest_ball = None
        ball_distance = 0
        for ball in ball_group:
            dist = self.distance(ball)
            if nearest_ball is None or dist < ball_distance:
                nearest_ball = ball
                ball_distance = dist

        if nearest_ball:
            angle = self.get_angle(nearest_ball)
            front_width = 2
            back_width = 5

            back_left = (self.x - 250 * math.cos(angle) + back_width * math.cos(angle + math.pi / 2),
                         self.y - 250 * math.sin(angle) + back_width * math.sin(angle + math.pi / 2))
            back_right = (self.x - 250 * math.cos(angle) - back_width * math.cos(angle + math.pi / 2),
                          self.y - 250 * math.sin(angle) - back_width * math.sin(angle + math.pi / 2))

            front_left = (self.x + 100 * math.cos(angle) + front_width * math.cos(angle + math.pi / 2),
                          self.y + 100 * math.sin(angle) + front_width * math.sin(angle + math.pi / 2))
            front_right = (self.x + 100 * math.cos(angle) - front_width * math.cos(angle + math.pi / 2),
                           self.y + 100 * math.sin(angle) - front_width * math.sin(angle + math.pi / 2))

            pygame.gfxdraw.aapolygon(screen, [back_right, back_left, front_left, front_right], (66, 13, 9))
            pygame.gfxdraw.filled_polygon(screen, [back_right, back_left, front_left, front_right], (66, 13, 9))

    def distance(self, ball):
        return math.sqrt((self.x - ball.get_center_x())**2 + (self.y - ball.get_center_y())**2)

    def get_angle(self, ball):
        return math.atan2(ball.get_center_y() - self.y, ball.get_center_x() - self.x)
