import pygame
import time
import random

# Initialize sound system and high score from a file
pygame.mixer.init()  # This initializes the sound system
pygame.mixer_music.load("-mp3cut_ZbWjDks.mp3")
pygame.mixer_music.set_volume(0.2)
pygame.mixer_music.play(-1)
def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0  # Return 0 if the file doesn't exist
game_over_music = pygame.mixer.Sound("tmpv9rdyy9z.mp3")
# Save the high score to a file
def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

# Game initialization and constants
pygame.init()
window_x = 720
window_y = 480
snake_speed = 15
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Game window and FPS controller
game_window = pygame.display.set_mode((window_x, window_y))
pygame.display.set_caption("Snake CIC")
fps = pygame.time.Clock()

# Load sound effects
eat_sound = pygame.mixer.Sound("2024-04-21 19-24-50 (1).mp3")  # Add your sound file name here

# Initial positions
snake_position = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
fruit_position = [random.randrange(1, (window_x//10)) * 10, random.randrange(1, (window_y//10)) * 10]
fruit_spawn = True
direction = 'RIGHT'
change_to = direction

# Scores
score = 0
highest_score = load_high_score()  # Load the high score at the beginning

# Displaying the score
def show_score(color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render(f"Score: {score}  High Score: {highest_score}", True, color)
    game_window.blit(score_surface, (10, 10))

# Game over function with high score logic
def game_over():
    global score, highest_score
    game_over_music.play()
    # Update high score if the current score is higher
    if score > highest_score:
        highest_score = score
        save_high_score(highest_score)  # Save the new high score

    my_font = pygame.font.SysFont("times new roman", 50)
    game_over_surface = my_font.render(f"Your Score: {score}", True, red)
    high_score_surface = my_font.render(f"High Score: {highest_score}", True, blue)

    game_over_rect = game_over_surface.get_rect(center=(window_x / 2, window_y / 4))
    high_score_rect = high_score_surface.get_rect(center=(window_x / 2, window_y / 2))

    game_window.blit(game_over_surface, game_over_rect)
    game_window.blit(high_score_surface, high_score_rect)

    pygame.display.flip()  # Refresh the screen

    time.sleep(2)  # Pause before quitting
    pygame.quit()
    quit()

# Main game loop
while True:
   
    # handling key events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
 
    # If two keys pressed simultaneously, we don't want snake to move into two directions
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'
 
    # Moving the snake
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    # Continue with the rest of the game logic...


    # Snake movement logic
    snake_body.insert(0, list(snake_position))
    if snake_position == fruit_position:
        score += 10
        eat_sound.play()  # Play the sound effect when the snake eats
        fruit_spawn = False
    else:
        snake_body.pop()

    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x//10)) * 10, random.randrange(1, (window_y//10)) * 10]

    fruit_spawn = True

    game_window.fill(black)

    # Draw the snake and fruit
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    
    pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

    # Game over conditions
    if snake_position[0] < 0 or snake_position[1] > window_x - 10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y - 10:
        game_over()

    for block in snake_body[1:]:
        if snake_position == block:
            game_over()

    # Display the score and high score
    show_score(white, "times new roman", 20)

    pygame.display.update()
    fps.tick(snake_speed)
