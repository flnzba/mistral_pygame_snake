import pygame
import time
import random
import json
import os

pygame.init()

# Define colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Display dimensions
dis_width = 800
dis_height = 600

# Initialize display
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by Mistral')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

# File to store user data
user_data_file = 'user_data.json'

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color, y_displace=0):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3 + y_displace])

def show_leaderboard():
    if os.path.exists(user_data_file):
        with open(user_data_file, 'r') as file:
            users = json.load(file)
            sorted_users = sorted(users.items(), key=lambda x: x[1]['high_score'], reverse=True)
            dis.fill(blue)
            message("Leaderboard", red, -100)
            y_displace = 0
            for username, data in sorted_users:
                message(f"{username}: {data['high_score']}", black, y_displace)
                y_displace += 50
            pygame.display.update()
            time.sleep(5)

def login_or_register():
    dis.fill(blue)
    message("Enter your username:", red, -50)
    pygame.display.update()
    username = input_text()

    if os.path.exists(user_data_file):
        with open(user_data_file, 'r') as file:
            users = json.load(file)
    else:
        users = {}

    if username not in users:
        users[username] = {'high_score': 0}
        with open(user_data_file, 'w') as file:
            json.dump(users, file)

    return username, users[username]['high_score']

def input_text():
    input_active = True
    text = ''
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
        dis.fill(blue)
        message("Enter your username:", red, -50)
        message(text, black, 0)
        pygame.display.update()
    return text

def gameLoop(username, high_score):
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            dis.fill(blue)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            message(f"Your Score: {Length_of_snake - 1}", black, 50)
            message(f"High Score: {high_score}", black, 100)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop(username, high_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
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

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    if Length_of_snake - 1 > high_score:
        with open(user_data_file, 'r') as file:
            users = json.load(file)
        users[username]['high_score'] = Length_of_snake - 1
        with open(user_data_file, 'w') as file:
            json.dump(users, file)

    pygame.quit()
    quit()

def main():
    username, high_score = login_or_register()
    show_leaderboard()
    gameLoop(username, high_score)

if __name__ == "__main__":
    main()