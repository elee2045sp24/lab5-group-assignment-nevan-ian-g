import pygame
import sys
from pygame import Vector2

# Constants for colors and screen size
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([10, 100])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = pygame.Vector2(0, 0)  # Velocity vector for movement

    def update(self):
        self.rect.move_ip(self.velocity)  # Move the paddle based on velocity
        self.check_boundary()  # Ensure paddle stays within screen bounds

    def check_boundary(self):
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([15, 15])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.velocity = pygame.Vector2(5, 5).normalize()  # Initial velocity vector

    def update(self):
        self.rect.x += self.velocity.x  
        self.rect.y += self.velocity.y  
        self.check_boundary()  # Ensure ball stays within screen bounds

    def reset_position(self):
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.velocity = pygame.Vector2(5, 5).normalize()  # Reset velocity

    def check_boundary(self):
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.velocity.y = -self.velocity.y  # Reverse y-velocity on hitting top or bottom
        elif self.rect.left <= 0:
            right_player_score.increase_score()
            self.reset_position()
        elif self.rect.right >= SCREEN_WIDTH:
            left_player_score.increase_score()
            self.reset_position()

class Score:
    def __init__(self, x, y):
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.text_surface = self.font.render(str(self.score), True, WHITE)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.topleft = (x, y)

    def increase_score(self):
        self.score += 1
        self.text_surface = self.font.render(str(self.score), True, WHITE)  # Update text surface
    


# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# Create paddles
left_paddle = Paddle(50, SCREEN_HEIGHT // 2)
right_paddle = Paddle(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2)

# Create ball
ball = Ball()

#score class instances  
left_player_score = Score(SCREEN_WIDTH // 2, 20)
right_player_score = Score(3 * SCREEN_WIDTH // 2, 20)

# Group for sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(left_paddle, right_paddle, ball)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        left_paddle.velocity.y = -5
    elif keys[pygame.K_s]:
        left_paddle.velocity.y = 5
    else:
        left_paddle.velocity.y = 0

    if keys[pygame.K_UP]:
        right_paddle.velocity.y = -5
    elif keys[pygame.K_DOWN]:
        right_paddle.velocity.y = 5
    else:
        right_paddle.velocity.y = 0

    #collide with paddles
    if pygame.sprite.spritecollide(ball, [left_paddle, right_paddle], False):
        ball.velocity.x = -ball.velocity.x
    
    # Update scores
    left_player_score.increase_score()
    right_player_score.increase_score()

     # Draw scores
    screen.blit(left_player_score.text_surface, left_player_score.text_rect)
    screen.blit(right_player_score.text_surface, right_player_score.text_rect)

    #Clear screen, update and draw objects
    all_sprites.update()
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()



