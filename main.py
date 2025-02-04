import pygame
import math
import random

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0
SPRING_CONSTANT = 0.3
DAMPING = 0.9
POINT_MASS = 10
MOUSE_RADIUS = 50
MOUSE_STRENGTH = 0.1

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Laser:
    def __init__(self):
        self.x = 0  # Start from the left
        self.y = HEIGHT // 2
        self.speed = 0.2
        self.width = 10
        self.height = HEIGHT  # Full height laser

    def update(self):
        self.x += self.speed  # Move right

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, 0, self.width, HEIGHT))

    def check_collision(self, points):
        for point in points:
            if self.x <= point.x <= self.x + self.width:
                return True  # Collision detected
        return False



class Point:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.fixed = False
        self.mass = mass

    def update(self):
        if not self.fixed:
            self.vy += GRAVITY
            self.x += self.vx
            self.y += self.vy
            self.vx *= DAMPING
            self.vy *= DAMPING

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), 5)
    
    def draw_blue(self):
        pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), 5)

    def update_mass(self, mass):
        self.mass = mass

class Spring:
    def __init__(self, p1, p2, length, diagonal=False):
        self.p1 = p1
        self.p2 = p2
        self.length = length
        self.diagonal = diagonal

    def update(self):
        dx = self.p2.x - self.p1.x
        dy = self.p2.y - self.p1.y
        dist = math.hypot(dx, dy)
        force = (dist - self.length) * SPRING_CONSTANT
        angle = math.atan2(dy, dx)
        fx = math.cos(angle) * force
        fy = math.sin(angle) * force

        if not self.p1.fixed:
            self.p1.vx += fx / self.p1.mass 
            self.p1.vy += fy / self.p1.mass
        if not self.p2.fixed:
            self.p2.vx -= fx / self.p2.mass
            self.p2.vy -= fy / self.p2.mass
    
    def update_length(self, n):
        self.length = n
        return
    def draw(self):
        pygame.draw.line(screen, BLACK, (int(self.p1.x), int(self.p1.y)), (int(self.p2.x), int(self.p2.y)), 1)
    
def create_softbody_grid(x, y, cols, rows, spacing):
    points = []
    springs = []


        
    for i in range(rows):
        for j in range(cols):
            point = Point(x + j * spacing, y + i * spacing, POINT_MASS)
            points.append(point)

            if j > 0:
                springs.append(Spring(points[-1], points[-2], spacing))
            if i > 0:
                springs.append(Spring(points[-1], points[-cols - 1], spacing))
            if i > 0 and j > 0:
                springs.append(Spring(points[-1], points[-cols - 2], math.sqrt(2) * spacing, True))
                springs.append(Spring(points[-2], points[-cols - 1], math.sqrt(2) * spacing, True))

    return points, springs

# Create a softbody grid
points, springs = create_softbody_grid(300, 100, 4, 4, 20)

laser = Laser()

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

        if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print("Spacebar pressed!")
                        springs[2].update_length(40)    # Mouse interaction
                        points[3].update_mass(10)
                        springs[38].update_length(40)    # Mouse interaction
                        points[15].update_mass(10)

                    if event.key == pygame.K_e:
                        springs[2].update_length(20)
                        points[3].update_mass(100)
                        springs[38].update_length(20)
                        points[15].update_mass(100)

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
        #if(spring.diagonal):
        #    spring.update_length(21)
        #else:
        #    spring.update_length(2*math.sqrt(2)
        spring.draw()


    for point in points:
        point.update()
        point.draw()
    points[15].draw_blue()

    laser.update()
    laser.draw()

    # Check for collision and destroy the soft body
    if laser.check_collision(points):
        points.clear()
        springs.clear()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()