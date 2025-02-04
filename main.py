import pygame
import math
import random

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0
SPRING_CONSTANT = 0.5
DAMPING = 0.99
POINT_MASS = 1
MOUSE_RADIUS = 50
MOUSE_STRENGTH = 1

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.fixed = False

    def update(self):
        if not self.fixed:
            self.vy += GRAVITY
            self.x += self.vx
            self.y += self.vy
            self.vx *= DAMPING
            self.vy *= DAMPING

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), 5)

class Spring:
    def __init__(self, p1, p2, length):
        self.p1 = p1
        self.p2 = p2
        self.length = length

    def update(self):
        dx = self.p2.x - self.p1.x
        dy = self.p2.y - self.p1.y
        dist = math.hypot(dx, dy)
        force = (dist - self.length) * SPRING_CONSTANT
        angle = math.atan2(dy, dx)
        fx = math.cos(angle) * force
        fy = math.sin(angle) * force

        if not self.p1.fixed:
            self.p1.vx += fx / POINT_MASS
            self.p1.vy += fy / POINT_MASS
        if not self.p2.fixed:
            self.p2.vx -= fx / POINT_MASS
            self.p2.vy -= fy / POINT_MASS

def create_softbody_grid(x, y, cols, rows, spacing):
    points = []
    springs = []

    for i in range(rows):
        for j in range(cols):
            point = Point(x + j * spacing, y + i * spacing)
            points.append(point)

            if j > 0:
                springs.append(Spring(points[-1], points[-2], spacing))
            if i > 0:
                springs.append(Spring(points[-1], points[-cols - 1], spacing))

    return points, springs

# Create a softbody grid
points, springs = create_softbody_grid(300, 100, 4, 4, 20)

# Fix the top row of points
for point in points[:10]:
    point.fixed = False

# Main loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mouse interaction
    mouse_x, mouse_y = pygame.mouse.get_pos()
    left, _, _ = pygame.mouse.get_pressed()

    for point in points:
        if left:
            dx = mouse_x - point.x
            dy = mouse_y - point.y
            dist = math.hypot(dx, dy)
            if dist < MOUSE_RADIUS:
                force = (MOUSE_RADIUS - dist) / MOUSE_RADIUS * MOUSE_STRENGTH
                angle = math.atan2(dy, dx)
                point.vx += math.cos(angle) * force
                point.vy += math.sin(angle) * force

    # Update points and springs
    for spring in springs:
        spring.update()

    for point in points:
        point.update()
        point.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()