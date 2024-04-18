import pygame
import sys


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
        self.speed = 0  # Initial speed

    def update(self):
        # Update the position based on the speed
        self.rect.y += self.speed

        # Keep the paddle within the screen bounds
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, color, x_speed, y_speed):
        super().__init__()
        self.image = pygame.Surface([radius * 2, radius * 2])
        self.image.fill(BLACK)  # Ball is initially black
        self.image.set_colorkey(BLACK)  # Make black transparent
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        # Collision with top and bottom walls
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.y_speed = -self.y_speed

        # Collision with paddles
        if pygame.sprite.spritecollide(self, all_sprites, False):
            self.x_speed = -self.x_speed  # Reverse direction

        # Collision with left and right walls (score)
        if self.rect.left <= 0:
            # Right player scores
            # Reset ball position and direction
            self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.x_speed = abs(self.x_speed)  # Reset speed
        elif self.rect.right >= SCREEN_WIDTH:
            # Left player scores
            # Reset ball position and direction
            self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.x_speed = -abs(self.x_speed)  # Reset speed



# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# Create paddles
left_paddle = Paddle(50, SCREEN_HEIGHT // 2)
right_paddle = Paddle(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2)

# Create ball
ball = Ball(10, WHITE, 5, 5)  # Radius, color, x_speed, y_speed

# Group for sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(left_paddle, right_paddle, ball)

# Main loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                left_paddle.speed = -5
            elif event.key == pygame.K_s:
                left_paddle.speed = 5
            elif event.key == pygame.K_UP:
                right_paddle.speed = -5
            elif event.key == pygame.K_DOWN:
                right_paddle.speed = 5
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                left_paddle.speed = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                right_paddle.speed = 0

    # Update all objects
    all_sprites.update()

    # Clear the screen
    screen.fill(BLACK)

    # Draw the paddles
    all_sprites.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()



