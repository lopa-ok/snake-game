import pygame
import time
import random


pygame.init()


white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
wall_color = (255, 0, 0)


dis_width = 800
dis_height = 600


dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')


clock = pygame.time.Clock()

snake_block = 10
initial_snake_speed = 5
max_snake_speed = 30 


font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

def our_snake(snake_block, snake_List):
    for x in snake_List:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def draw_wall():
    margin = 20  
    pygame.draw.rect(dis, wall_color, [margin, margin, dis_width - 2 * margin, 10])  
    pygame.draw.rect(dis, wall_color, [margin, margin, 10, dis_height - 2 * margin]) 
    pygame.draw.rect(dis, wall_color, [margin, dis_height - margin - 10, dis_width - 2 * margin, 10])  
    pygame.draw.rect(dis, wall_color, [dis_width - margin - 10, margin, 10, dis_height - 2 * margin])

def show_score(score):
    value = score_font.render("Score: " + str(score), True, white)
    dis.blit(value, [dis_width / 2 - 50, 0])

def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    margin = 30  

    foodx = round(random.randrange(margin, dis_width - margin - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(margin, dis_height - margin - snake_block) / 10.0) * 10.0

    direction = None
    snake_speed = initial_snake_speed

    while not game_over:

        while game_close == True:
            dis.fill(blue)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            show_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

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

        if x1 >= dis_width - margin - 10 or x1 < margin or y1 >= dis_height - margin - 10 or y1 < margin:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)

        draw_wall() 

        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        show_score(Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(margin, dis_width - margin - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(margin, dis_height - margin - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            snake_speed = min(snake_speed + 1, max_snake_speed)  # Increase speed but cap it

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
