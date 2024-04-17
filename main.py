import pygame
from pygame import Vector2,rect
import sys

#colors
BLACK = (0, 0, 0)

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaga")

class Paddle:
    def __init__(self, pos:Vector2):
        self.pos = pos
        self.vel = Vector2(0,0)
        #self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
    def draw(self, screen):
        pygame.draw.rect(screen, "#0000FF", self.rect)

paddle = Paddle()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(BLACK)
    pygame.display.flip()


pygame.quit()
sys.exit()



