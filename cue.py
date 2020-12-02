import pygame
import pygame.gfxdraw
import math
from enum import Enum


class State(Enum):
    DRAWING = 1
    SHOOTING = 2
    AIMING = 3


class Cue(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 0
        self.y = 0
        self.drawing = False
        self.draw_distance = 0
        self.nearest_ball = None

    def update(self, *args, **kwargs) -> None:
        ball_group = args[0]
        self.nearest_ball = self.get_nearest_ball(ball_group)
        left, middle, right = pygame.mouse.get_pressed(num_buttons=3)
        if self.drawing:
            if left:
                self.draw_distance = 30
                self.x, self.y = pygame.mouse.get_pos()
            else:
                self.drawing = False
                self.x, self.y = pygame.mouse.get_pos()
        else:
            if left:
                self.drawing = True
                self.x, self.y = pygame.mouse.get_pos()
            else:
                self.x, self.y = pygame.mouse.get_pos()

    def get_nearest_ball(self, ball_group):
        nearest_ball = None
        ball_distance = 0
        for ball in ball_group:
            dist = self.distance(ball)
            if nearest_ball is None or dist < ball_distance:
                nearest_ball = ball
                ball_distance = dist
        return nearest_ball

    def draw(self, screen):
        if self.nearest_ball:
            angle = self.get_angle(self.nearest_ball)
            front_width = 2
            back_width = 5
            cue_length = 400

            back_left = (self.x - cue_length * math.cos(angle) + back_width * math.cos(angle + math.pi / 2),
                         self.y - cue_length * math.sin(angle) + back_width * math.sin(angle + math.pi / 2))
            back_right = (self.x - cue_length * math.cos(angle) - back_width * math.cos(angle + math.pi / 2),
                          self.y - cue_length * math.sin(angle) - back_width * math.sin(angle + math.pi / 2))

            front_left = (self.x + math.cos(angle) + front_width * math.cos(angle + math.pi / 2),
                          self.y + math.sin(angle) + front_width * math.sin(angle + math.pi / 2))
            front_right = (self.x + math.cos(angle) - front_width * math.cos(angle + math.pi / 2),
                           self.y + math.sin(angle) - front_width * math.sin(angle + math.pi / 2))

            pygame.gfxdraw.aapolygon(screen, [back_right, back_left, front_left, front_right], (66, 13, 9))
            pygame.gfxdraw.filled_polygon(screen, [back_right, back_left, front_left, front_right], (66, 13, 9))

    def distance(self, ball):
        return math.sqrt((self.x - ball.get_center_x())**2 + (self.y - ball.get_center_y())**2)

    def get_angle(self, ball):
        return math.atan2(ball.get_center_y() - self.y, ball.get_center_x() - self.x)
