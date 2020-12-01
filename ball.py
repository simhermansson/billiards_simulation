import pygame
import pygame.gfxdraw
import pool_table
import random
import math


class Ball(pygame.sprite.Sprite):
    def __init__(self, table: pool_table, x: int, y: int, random_speed=False):
        pygame.sprite.Sprite.__init__(self)

        self.table = table

        self.RADIUS = 20    # mm
        self.MASS = 0.16   # kg

        self.image = pygame.Surface([self.RADIUS*2 + 1, self.RADIUS*2 + 1], pygame.SRCALPHA)

        if random_speed:
            self.dx = random.randint(0, 3)
            self.dy = random.randint(0, 3)
        else:
            self.dx = 0
            self.dy = 0

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

    def set_velocity(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def get_center_x(self):
        return self.rect.centerx

    def get_center_y(self):
        return self.rect.centery

    def get_velocity(self):
        return math.sqrt(self.dx**2 + self.dy**2)

    def get_velocity_x(self):
        return self.dx

    def get_velocity_y(self):
        return self.dy

    def get_movement_angle(self):
        return math.atan2(self.dy, self.dx)


def get_contact_angle(a, b):
    return math.atan2(b.get_center_y() - a.get_center_y(), b.get_center_x() - a.get_center_x())


def get_collision_values(a, b, contact_angle):
    adx = b.get_velocity() * math.cos(b.get_movement_angle() - contact_angle) * math.cos(contact_angle) \
          + a.get_velocity() * math.sin(a.get_movement_angle() - contact_angle) * math.cos(contact_angle + math.pi / 2)

    ady = b.get_velocity() * math.cos(b.get_movement_angle() - contact_angle) * math.sin(contact_angle) \
          + a.get_velocity() * math.sin(a.get_movement_angle() - contact_angle) * math.sin(contact_angle + math.pi / 2)

    bdx = (a.get_velocity() * math.cos(a.get_movement_angle() - contact_angle) * math.cos(contact_angle)
           + b.get_velocity() * math.sin(b.get_movement_angle() - contact_angle) * math.cos(contact_angle + math.pi / 2))

    bdy = (a.get_velocity() * math.cos(a.get_movement_angle() - contact_angle) * math.sin(contact_angle)
           + b.get_velocity() * math.sin(b.get_movement_angle() - contact_angle) * math.sin(contact_angle + math.pi / 2))

    return adx, ady, bdx, bdy


def distance(a, b):
    return math.sqrt((a.get_center_x() - b.get_center_x())**2 + (a.get_center_y() - b.get_center_y())**2)


def overlap(a, b):
    return distance(a, b) <= 20 * 2


def collision(a, b):
    contact_angle = get_contact_angle(a, b)

    a.rect.x -= a.get_velocity_x()
    a.rect.y -= a.get_velocity_y()
    b.rect.x -= b.get_velocity_x()
    b.rect.y -= b.get_velocity_y()

    adx, ady, bdx, bdy = get_collision_values(a, b, contact_angle)
    #bdx, bdy = get_collision_values(b, a, contact_angle)

    totx = a.get_velocity_x() + b.get_velocity_x()
    toty = a.get_velocity_y() + b.get_velocity_y()

    a.set_velocity(adx, ady)
    b.set_velocity(bdx, bdy)
