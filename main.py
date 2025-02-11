import pygame
import math
import random
import numpy as np
from box import Box


#BOX
TRAIT_COUNT = 80
LENGTH_STATE = 60
# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0
SPRING_CONSTANT = 0.3
DAMPING = 0.9
POINT_MASS = 20
MOUSE_RADIUS = 50
MOUSE_STRENGTH = 0.1
SPACING = 20

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

def createNewCreature():
    dna = np.clip(np.random.normal(0.0, 5.0, TRAIT_COUNT),-20,20)
    return Box(dna)
#MAIN START


points, springs = create_softbody_grid(300, 100, 4, 4, SPACING)
laser = Laser()
running = True


tempcreature = createNewCreature()
print(tempcreature.dna)



frames = 0
state = False
while running:
    frames += 1
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                springs[2].update_length(40)
                points[3].update_mass(10)
                springs[38].update_length(-10)
                points[15].update_mass(10)
            if event.key == pygame.K_e:
                springs[2].update_length(20)
                points[3].update_mass(100)
                springs[38].update_length(20)
                points[15].update_mass(100)


#update the spring values to creature
    spring_count = 0
    bumper_val = 0
    if(state):
        bumper_val = 0
    else:
        bumper_val = 24

    for spring in springs:
        if (not spring.diagonal):
            spring.update_length(SPACING + tempcreature.dna[bumper_val+spring_count])
            spring_count += 1 

    if(state):
        bumper_val = 48
    else:
        bumper_val = 64
    for i, point in enumerate(points):
        point.update_mass(POINT_MASS + tempcreature.dna[bumper_val+i])

    mouse_x, mouse_y = pygame.mouse.get_pos()
    left, _, _ = pygame.mouse.get_pressed()
    
    if(frames % LENGTH_STATE == 0):
        state = not state
    


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

    for spring in springs:
        spring.update()
        spring.draw()

    for point in points:
        point.update()

    # Prevent points from overlapping
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            p1 = points[i]
            p2 = points[j]
            dx = p2.x - p1.x
            dy = p2.y - p1.y
            distance = math.hypot(dx, dy)
            min_distance = 10  # Minimum distance between points
            if 0 < distance < min_distance:
                # Calculate separation vector
                overlap = (min_distance - distance) / 2
                angle = math.atan2(dy, dx)
                nx = math.cos(angle)
                ny = math.sin(angle)
                
                # Move points apart
                if not p1.fixed:
                    p1.x -= overlap * nx
                    p1.y -= overlap * ny
                if not p2.fixed:
                    p2.x += overlap * nx
                    p2.y += overlap * ny

    for point in points:
        point.draw()
    points[15].draw_blue()

    laser.update()
    laser.draw()

    if laser.check_collision(points):
        points.clear()
        springs.clear()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()