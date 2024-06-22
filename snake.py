import pygame
import time
import random

# Initialize the Pygame
pygame.init()

# Define colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
wall_color = (255, 0, 0)
boost_color = (0, 255, 255)
slow_color = (255, 165, 0)

# Set the dimensions of the window
dis_width = 800
dis_height = 600

# Initialize the display
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game with Wall, Score, and Power-ups')

# Set the clock for controlling the frame rate
clock = pygame.time.Clock()

snake_block = 10
initial_snake_speed = 5
max_snake_speed = 30  # Maximum speed limit for the snake

# Set the font style and size
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

# Initialize high score
high_score = 0

def our_snake(snake_block, snake_List):
    for x in snake_List:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def draw_wall():
    margin = 20  # Margin from the edges of the window
    pygame.draw.rect(dis, wall_color, [margin, margin, dis_width - 2 * margin, 10])  # Top wall
    pygame.draw.rect(dis, wall_color, [margin, margin, 10, dis_height - 2 * margin])  # Left wall
    pygame.draw.rect(dis, wall_color, [margin, dis_height - margin - 10, dis_width - 2 * margin, 10])  # Bottom wall
    pygame.draw.rect(dis, wall_color, [dis_width - margin - 10, margin, 10, dis_height - 2 * margin])  # Right wall

def show_score(score):
    value = score_font.render("Score: " + str(score), True, white)
    dis.blit(value, [dis_width / 2 - 50, 0])

def show_power_up_timer(active_power_up, power_up_effect_timer):
    if active_power_up:
        msg = f"{active_power_up.replace('_', ' ').title()}: {power_up_effect_timer // 10}"
        value = score_font.render(msg, True, white)
        dis.blit(value, [dis_width - 200, 0])

def show_high_score():
    global high_score
    value = score_font.render("High Score: " + str(high_score), True, white)
    dis.blit(value, [10, 0])

class PowerUp:
    def __init__(self, x, y, power_type, color):
        self.x = x
        self.y = y
        self.type = power_type
        self.color = color
        self.size = snake_block

    def draw(self):
        pygame.draw.rect(dis, self.color, [self.x, self.y, self.size, self.size])

def gameLoop():
    global high_score
    game_over = False
    game_close = False
    game_paused = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    margin = 30  # Margin from the edges of the window for the snake and food

    foodx = round(random.randrange(margin, dis_width - margin - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(margin, dis_height - margin - snake_block) / 10.0) * 10.0

    direction = None
    snake_speed = initial_snake_speed

    power_up_timer = 0
    power_ups = []

    active_power_up = None
    power_up_effect_timer = 0

    while not game_over:

        while game_close:
            dis.fill(blue)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            show_score(Length_of_snake - 1)
            show_high_score()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        while game_paused:
            dis.fill(blue)
            message("Game Paused! Press P to Resume", yellow)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        game_paused = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != 'RIGHT':
                    x1_change = -snake_block
                    y1_change = 0
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    x1_change = snake_block
                    y1_change = 0
                    direction = 'RIGHT'
                elif event.key == pygame.K_UP and direction != 'DOWN':
                    y1_change = -snake_block
                    x1_change = 0
                    direction = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    y1_change = snake_block
                    x1_change = 0
                    direction = 'DOWN'
                elif event.key == pygame.K_p:
                    game_paused = True

        if x1 >= dis_width - margin - 10 or x1 < margin or y1 >= dis_height - margin - 10 or y1 < margin:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)

        draw_wall()  # Draw the wall around the edges

        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        show_score(Length_of_snake - 1)
        show_high_score()
        show_power_up_timer(active_power_up, power_up_effect_timer)

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(margin, dis_width - margin - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(margin, dis_height - margin - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            snake_speed = min(snake_speed + 1, max_snake_speed)  # Increase speed but cap it

        # Power-up logic
        if power_up_timer <= 0:
            power_up_type = random.choice(['speed_boost', 'slow_down'])
            power_up_color = boost_color if power_up_type == 'speed_boost' else slow_color
            power_up_x = round(random.randrange(margin, dis_width - margin - snake_block) / 10.0) * 10.0
            power_up_y = round(random.randrange(margin, dis_height - margin - snake_block) / 10.0) * 10.0
            power_ups.append(PowerUp(power_up_x, power_up_y, power_up_type, power_up_color))
            power_up_timer = random.randint(100, 300)
        else:
            power_up_timer -= 1

        for power_up in power_ups:
            power_up.draw()
            if x1 == power_up.x and y1 == power_up.y:
                active_power_up = power_up.type
                power_up_effect_timer = 100  # Duration the power-up effect lasts (in frames)
                power_ups.remove(power_up)

        # Apply power-up effects
        if power_up_effect_timer > 0:
            power_up_effect_timer -= 1
            if active_power_up == 'speed_boost':
                snake_speed = min(snake_speed + 5, max_snake_speed)
            elif active_power_up == 'slow_down':
                snake_speed = max(snake_speed - 5, 1)
        else:
            active_power_up = None
            snake_speed = initial_snake_speed + Length_of_snake - 1  # Reset to the normal speed based on length

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Start the game loop
gameLoop()
