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

        self.table = table

        self.RADIUS = 20
        self.MASS = 1
        self.color = color

        self.px = x
        self.py = y
        self.dx = 0
        self.dy = 0
        self.ax = 0
        self.ay = 0

    def get_radius(self):
        return self.RADIUS

    def update(self, *args, **kwargs) -> None:
        """
        Updates the values for ball. Applies friction and handles wall-collisions.
        :param args: args[0]: DeltaTime, time since last tick.
        """
        dt = args[0]

        """
        Force by friction is equal to the kinetic friction constant (mu) times the normal force, which on this
        horizontal surface is mg. Work done by this force is the force times the distance, where the
        distance is equal to the initial velocity times the delta time.
        
        Now we have the work. This work is equal to the change in kinetic energy. So W = Ki - Kf. Where 
        K = 1/2 * mv^2. We remove m from both sides and solve for v. Finally we get that
        v = sqrt(vi^2 - 2 * mu * g * vi * dt).
        """
        right_hand_side = 2 * self.table.get_kinetic_friction() * 9.81 * self.get_speed() * dt
        if right_hand_side > self.get_speed()**2:
            self.set_velocity(0, 0)
        else:
            v = math.sqrt(self.get_speed() ** 2 - right_hand_side)
            self.set_velocity(v * math.cos(self.get_movement_angle()), v * math.sin(self.get_movement_angle()))

        self.px += self.dx
        self.py += self.dy

        if self.px - self.RADIUS < self.table.get_left_edge():
            self.dx = -self.dx
        if self.px + self.get_radius() > self.table.get_right_edge():
            self.dx = -self.dx
        if self.py - self.get_radius() < self.table.get_top_edge():
            self.dy = -self.dy
        if self.py + self.get_radius() > self.table.get_bottom_edge():
            self.dy = -self.dy

    def get_speed(self):
        return math.sqrt(self.dx**2 + self.dy**2)

    def set_position(self, x, y):
        self.px = x
        self.py = y

    def get_movement_angle(self):
        return math.atan2(self.dy, self.dx)

    def draw_self(self, display):
        """
        Draws both anti-aliased edge and a filled polygon to get an anti-aliased circle.

        :param display: Game screen to draw on.
        """
        pygame.gfxdraw.aacircle(display, int(self.px), int(self.py), self.get_radius(), pygame.Color(self.color))
        pygame.gfxdraw.filled_circle(display, int(self.px), int(self.py), self.get_radius(), pygame.Color(self.color))

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
    return distance(a, b) <= a.get_radius() * 2


def get_contact_angle(a, b):
    return math.atan2(b.py - a.py, b.px - a.px)


def collision(a, b):
    """
    Implements elastic collisions between two ball objects through simple 2D-physics.
    """

    """

    a.set_position(a.get_center_x() - a.get_speed() * math.cos(a.get_movement_angle()),
                   a.get_center_y() - a.get_speed() * math.sin(a.get_movement_angle()))

    b.set_position(b.get_center_x() - b.get_speed() * math.cos(b.get_movement_angle()),
                   b.get_center_y() - b.get_speed() * math.sin(b.get_movement_angle()))
   """

    contact_angle = get_contact_angle(a, b)

    # Get vector between the two balls and normalize
    nx = (b.px - a.px) / distance(a, b)
    ny = (b.py - a.py) / distance(a, b)

    # Fix a bug where they stick
    a.px -= nx
    a.py -= ny

    adx = (b.get_speed() * math.cos(b.get_movement_angle() - contact_angle) * math.cos(contact_angle)
           + a.get_speed() * math.sin(a.get_movement_angle() - contact_angle) * math.cos(contact_angle + math.pi / 2))

    ady = (b.get_speed() * math.cos(b.get_movement_angle() - contact_angle) * math.sin(contact_angle)
           + a.get_speed() * math.sin(a.get_movement_angle() - contact_angle) * math.sin(contact_angle + math.pi / 2))

    bdx = (a.get_speed() * math.cos(a.get_movement_angle() - contact_angle) * math.cos(contact_angle)
           + b.get_speed() * math.sin(b.get_movement_angle() - contact_angle) * math.cos(contact_angle + math.pi / 2))

    bdy = (a.get_speed() * math.cos(a.get_movement_angle() - contact_angle) * math.sin(contact_angle)
           + b.get_speed() * math.sin(b.get_movement_angle() - contact_angle) * math.sin(contact_angle + math.pi / 2))

    a.dx = adx
    a.dy = ady
    b.dx = bdx
    b.dy = bdy
