import paho.mqtt.client as mqtt
import cv2
import mediapipe as mp
import pygame
import sys, time
import random
from pygame import Vector2

#initialize MQTT
powUp1_topic = "ugaelee2045sp24/ikg61117/powUp1"
powUp2_topic = "ugaelee2045sp24/ikg61117/powUp2"
def on_message(client_obj, userdata, message):
    print(f"Message received: {message.payload.decode('utf8')}")
    if message.topic == powUp1_topic:
        left_paddle.power_up = True
    if message.topic == powUp2_topic:
        right_paddle.power_up = True

client_id = "123"                                                                                   #MQTT setup
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id)
client.username_pw_set("class_user", "class_password")
client.connect("mqtt.ugavel.com")
client.on_message = on_message
client.subscribe(powUp1_topic)
client.subscribe(powUp2_topic)
client.loop_start()

#initialize hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands =2)
mp_draw = mp.solutions.drawing_utils

# Initialize Pygame
pygame.init()

cap = cv2.VideoCapture(0)  #initalize camera

# Constants for colors and screen size
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
#Font
game_font = pygame.font.Font("game_font.ttf", 15)


class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([10, 100])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = pygame.Vector2(0, 0)  # Velocity vector for movement
        self.power_up = False
        self.number_power_ups = 2

    def update(self):
        self.rect.move_ip(self.velocity)  # Move the paddle based on velocity
        self.check_boundary()  # keeps paddle within screen bounds

    def check_boundary(self):
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
    
    def powers_up(self):
            print(self.rect.height)
            self.rect.inflate(5,5)
class Score:
    def __init__(self, x, y):
        self.score = 0
        self.font = pygame.font.Font("game_font.ttf", 36)
        self.text_surface = self.font.render(str(self.score), True, WHITE)
        self.text_rect = self.text_surface.get_rect(topleft=(x, y))
        
    def increase_score(self):
        self.score += 1
        self.text_surface = self.font.render(f"Score: {str(self.score)}", True, WHITE)
        self.text_rect = self.text_surface.get_rect(topleft=self.text_rect.topleft)
        

# initialize score
right_player_score = Score(3 * SCREEN_WIDTH // 2, 20)
left_player_score = Score(SCREEN_WIDTH // 2, 20)


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([15, 15])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.velocity_choices = [1, -1]
        self.velocity_magnitude_x = 3
        self.velocity_magnitude_y = 3
        self.velocity = pygame.Vector2(random.choice(self.velocity_choices)*(self.velocity_magnitude_x), random.choice(self.velocity_choices)*(self.velocity_magnitude_y)) #.normalize()  #Generate sudo-random direction each start

    def update(self):
        self.rect.move_ip(self.velocity.x, self.velocity.y)
        self.check_boundary()  # keeps ball stays within screen bounds


    def reset_position(self):
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.velocity = pygame.Vector2(random.choice(self.velocity_choices)*(self.velocity_magnitude_x), random.choice(self.velocity_choices)*(self.velocity_magnitude_y)) #.normalize()

    def check_boundary(self):
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.velocity.y = -self.velocity.y  # Reverse y-velocity on hitting top or bottom
        elif self.rect.left <= 0:
            right_player_score.increase_score()
            self.reset_position()
        elif self.rect.right >= SCREEN_WIDTH:
            left_player_score.increase_score()
            self.reset_position()

# Create ball
ball = Ball()

# Define Power-up Class
class PowerUp:
    def __init__(self, name):
        self.name = name

    def apply_effect(self, game):
        pass  # Implement this method in subclasses

# Define specific power-up classes
#class IncreasePaddleSize(PowerUp):
#    def apply_effect(self, game):
 #       game.left_paddle.size += 1

class SpeedUpBall(PowerUp):
    def apply_effect(self, game):
        game.velocity_magnitude_x *= 50  # Increase ball speed
        game.velocity_magnitude_y *= 50

#power up function
def powerUpCheck(Paddle):
    if Paddle.power_up == True:
        Paddle.image = pygame.transform.scale_by(Paddle.image, 1.8)
        print(Paddle.power_up)
        Paddle.power_up = False
        

#draw text on screen
def draw_text(text, font, text_col, x, y):            
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))   
 
# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED | pygame.RESIZABLE, vsync =1)
pygame.display.set_caption("Magic Pong")

# Create paddles
left_paddle = Paddle(50, SCREEN_HEIGHT // 2)
right_paddle = Paddle(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2)



# Group for sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(left_paddle, right_paddle, ball)

# Main loop
running = True
while running:
    # Capture frame from webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(cv2.flip(frame,1), cv2.COLOR_BGR2RGB)    #flip shows mirror image on cv window

    # Process the frame with MediaPipe
    results = hands.process(frame_rgb)

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
    
    #For loop used to find hands, draw them, and control paddles
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame_rgb, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Determine which hand (left or right) based on wrist position (x-coordinate)
            hand_x = hand_landmarks.landmark[17].x  # X-coordinate of middle of backside of hand (landmark 17 via mediapipe documentation)
            hand_y = hand_landmarks.landmark[17].y  # Y-coordinate of middle of backside of hand (landmark 17 via mediapipe documentation)

            # Convert the wrist y-coordinate to screen height
            wrist_y_screen = int(hand_y * SCREEN_HEIGHT)

            if hand_x < 0.5:
                # Control left paddle if hand is on the left side
                left_paddle.velocity.y += (wrist_y_screen - SCREEN_HEIGHT // 2)*.3          #multiply by 0.3 to reduced sensitivity
            else:
                # Control right paddle if hand is on the right side
                right_paddle.velocity.y += (wrist_y_screen - SCREEN_HEIGHT // 2)*.3

    #collide with paddles
    if pygame.sprite.spritecollide(ball, [left_paddle, right_paddle], False):
        ball.velocity.x = -ball.velocity.x

    #Power Ups
    powerUpCheck(left_paddle)
    
    # Create an array of power-ups
    power_ups = [SpeedUpBall("Speed Up Ball")]

    # Randomly select a power-up and apply its effect
    # Randomly select a power-up and apply its effect
    # selected_power_up = random.choice(power_ups)
    # selected_power_up.apply_effect(ball)  # Apply power-up effect

    #Clear screen, update and draw objects
    screen.fill(BLACK)
    
    #Draw Text
    draw_text(f"Player 1 Score: {left_player_score.score}", game_font, WHITE, 10,10)
    draw_text(f"Player 2 Score: {right_player_score.score}", game_font, WHITE, 520, 10)

    all_sprites.update()
    all_sprites.draw(screen)
    

    # Convert RGB frame back to BGR for display
    frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

    # Display the frame in OpenCV window (for reference)
    cv2.imshow("Hand Tracking", frame_bgr)

    pygame.time.Clock().tick(60)
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()



