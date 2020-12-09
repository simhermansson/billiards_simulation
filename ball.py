import pygame
import pygame.gfxdraw
import pool_table
import math


class Ball(pygame.sprite.Sprite):
    def __init__(self, table: pool_table, x: int, y: int, color):
        """
        The ball objects belong to a pygame.sprite.Group and can be pushed around on a pool table.

        :param table: The pool table the ball belongs to.
        :param x: X-position of ball
        :param y: Y-position of ball
        :param color: Color of ball
        """
        pygame.sprite.Sprite.__init__(self)

        self.px = x
        self.py = y
        self.dx = 0
        self.dy = 0
        self.ax = 0
        self.ay = 0

        self.table = table
        self.color = color
        self.rect = pygame.Rect(x, y, Ball.get_radius(), Ball.get_radius())
        self.RADIUS = Ball.get_radius()
        self.MASS = 0.16

    @staticmethod
    def get_radius():
        return 20

    def update(self, *args, **kwargs) -> None:
        """
        Updates the values for ball. Applies friction and handles wall-collisions.

        :param args: args[0]: DeltaTime, time since last tick.
        """

        dt = args[0]
        mu = self.table.get_friction()  # Friction constant
        self.ax = -self.dx * mu
        self.ay = -self.dy * mu

        self.dx += self.ax * dt
        self.dy += self.ay * dt
        self.px += self.dx * dt
        self.py += self.dy * dt

        if self.px - Ball.get_radius() < self.table.get_left_edge():
            self.dx = -self.dx
        if self.px + Ball.get_radius() > self.table.get_right_edge():
            self.dx = -self.dx
        if self.py - Ball.get_radius() < self.table.get_top_edge():
            self.dy = -self.dy
        if self.py + Ball.get_radius() > self.table.get_bottom_edge():
            self.dy = -self.dy

    def get_velocity(self):
        return math.sqrt(self.dx**2 + self.dy**2)

    def set_position(self, x, y):
        self.px = x
        self.py = y

    def get_movement_angle(self):
        return math.atan2(self.dy, self.dx)

    def get_friction_angle(self):
        return -math.atan2(self.dy, self.dx)

    def draw_self(self, display):
        """
        Draws both anti-aliased edge and a filled polygon to get an anti-aliased circle.

        :param display: Game screen to draw on.
        """
        pygame.gfxdraw.aacircle(display, int(self.px), int(self.py), Ball.get_radius(), pygame.Color(self.color))
        pygame.gfxdraw.filled_circle(display, int(self.px), int(self.py), Ball.get_radius(), pygame.Color(self.color))

    def apply_force(self, force, angle):
        """
        Applies a force to the ball which changes its velocity.
        """
        self.dx += force * math.cos(angle)
        self.dy += force * math.sin(angle)

    def set_velocity(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def get_center_x(self):
        return self.px

    def get_center_y(self):
        return self.py


def distance(a, b):
    return math.sqrt((a.px - b.px)**2 + (a.py - b.py)**2)


def overlaps(a, b):
    return distance(a, b) <= Ball.get_radius() * 2


def get_contact_angle(a, b):
    return math.atan2(b.py - a.py, b.px - a.px)


def collision(a, b):
    """
    Implements elastic collisions between two ball objects through simple 2D-physics.
    """

    """

    a.set_position(a.get_center_x() - a.get_velocity() * math.cos(a.get_movement_angle()),
                   a.get_center_y() - a.get_velocity() * math.sin(a.get_movement_angle()))

    b.set_position(b.get_center_x() - b.get_velocity() * math.cos(b.get_movement_angle()),
                   b.get_center_y() - b.get_velocity() * math.sin(b.get_movement_angle()))
   """

    contact_angle = get_contact_angle(a, b)

    # Get vector between the two balls and normalize
    nx = (b.px - a.px) / distance(a, b)
    ny = (b.py - a.py) / distance(a, b)

    # Fix a bug where they stick
    a.px -= nx
    a.py -= ny

    adx = (b.get_velocity() * math.cos(b.get_movement_angle() - contact_angle) * math.cos(contact_angle)
           + a.get_velocity() * math.sin(a.get_movement_angle() - contact_angle) * math.cos(contact_angle + math.pi/2))

    ady = (b.get_velocity() * math.cos(b.get_movement_angle() - contact_angle) * math.sin(contact_angle)
           + a.get_velocity() * math.sin(a.get_movement_angle() - contact_angle) * math.sin(contact_angle + math.pi/2))

    bdx = (a.get_velocity() * math.cos(a.get_movement_angle() - contact_angle) * math.cos(contact_angle)
           + b.get_velocity() * math.sin(b.get_movement_angle() - contact_angle) * math.cos(contact_angle + math.pi/2))

    bdy = (a.get_velocity() * math.cos(a.get_movement_angle() - contact_angle) * math.sin(contact_angle)
           + b.get_velocity() * math.sin(b.get_movement_angle() - contact_angle) * math.sin(contact_angle + math.pi/2))

    a.dx = adx
    a.dy = ady
    b.dx = bdx
    b.dy = bdy
