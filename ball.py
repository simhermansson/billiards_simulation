import pygame
import pygame.gfxdraw
import pool_table
import math


class Ball(pygame.sprite.Sprite):
    def __init__(self, table: pool_table, x: int, y: int, color):
        pygame.sprite.Sprite.__init__(self)

        # Float coordinates.
        self.px = x
        self.py = y
        self.dx = 0
        self.dy = 0

        self.table = table
        self.color = color
        self.rect = pygame.Rect(x, y, Ball.get_radius(), Ball.get_radius())
        self.RADIUS = Ball.get_radius()
        self.MASS = 0.16

    @staticmethod
    def get_radius():
        return 20

    def update(self, *args, **kwargs) -> None:
        dt = args[0]
        self.px += self.dx * dt
        self.py += self.dy * dt

        self.dx = self.dx * (1 - self.table.get_friction())
        self.dy = self.dy * (1 - self.table.get_friction())
        if abs(self.dx) < 0.1:
            self.dx = 0
        if abs(self.dy) < 0.1:
            self.dy = 0

        if self.px - Ball.get_radius() < self.table.get_left_edge():
            self.dx = -self.dx
        if self.px + Ball.get_radius() > self.table.get_right_edge():
            self.dx = -self.dx
        if self.py - Ball.get_radius() < self.table.get_top_edge():
            self.dy = -self.dy
        if self.py + Ball.get_radius() > self.table.get_bottom_edge():
            self.dy = -self.dy

    def apply_force(self, force, angle):
        self.dx += force * math.cos(angle)
        self.dy += force * math.sin(angle)

    def set_velocity(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def get_center_x(self):
        return self.px

    def get_center_y(self):
        return self.py

    def get_velocity(self):
        return math.sqrt(self.dx**2 + self.dy**2)

    def get_velocity_x(self):
        return self.dx

    def get_velocity_y(self):
        return self.dy

    def get_movement_angle(self):
        return math.atan2(self.dy, self.dx)

    def draw_self(self, display):
        # Draws both anti-aliased edge and a filled polygon to get an anti-aliased circle.
        pygame.gfxdraw.aacircle(display, int(self.px), int(self.py), Ball.get_radius(), pygame.Color(self.color))
        pygame.gfxdraw.filled_circle(display, int(self.px), int(self.py), Ball.get_radius(), pygame.Color(self.color))


def get_contact_angle(a, b):
    return math.atan2(b.py - a.py, b.px - a.px)


def collision(a, b):

    contact_angle = get_contact_angle(a, b)

    adx = (b.get_velocity() * math.cos(b.get_movement_angle() - contact_angle) * math.cos(contact_angle)
          + a.get_velocity() * math.sin(a.get_movement_angle() - contact_angle) * math.cos(contact_angle + math.pi / 2))

    ady = (b.get_velocity() * math.cos(b.get_movement_angle() - contact_angle) * math.sin(contact_angle)
          + a.get_velocity() * math.sin(a.get_movement_angle() - contact_angle) * math.sin(contact_angle + math.pi / 2))

    bdx = (a.get_velocity() * math.cos(a.get_movement_angle() - contact_angle) * math.cos(contact_angle)
           + b.get_velocity() * math.sin(b.get_movement_angle() - contact_angle) * math.cos(contact_angle + math.pi / 2))

    bdy = (a.get_velocity() * math.cos(a.get_movement_angle() - contact_angle) * math.sin(contact_angle)
           + b.get_velocity() * math.sin(b.get_movement_angle() - contact_angle) * math.sin(contact_angle + math.pi / 2))

    a.dx = adx
    a.dy = ady
    b.dx = bdx
    b.dy = bdy


def distance(a, b):
    return math.sqrt((a.px - b.px)**2 + (a.py - b.py)**2)


def overlaps(a, b):
    return distance(a, b) <= Ball.get_radius() * 2


def collision_wall(b):
    if b.px - Ball.get_radius() <= b.table.get_left_edge():
        b.dx = -b.dx
    if b.px + Ball.get_radius() >= b.table.get_right_edge():
        b.dx = -b.dx
    if b.py - Ball.get_radius() <= b.table.get_top_edge():
        b.dy = -b.dy
    if b.py + Ball.get_radius() >= b.table.get_bottom_edge():
        b.dy = -b.dy
