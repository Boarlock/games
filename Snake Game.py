import pygame 
import random
import pygame.mixer
import os
import sys

pygame.init() #Initialize pygame
pygame.mixer.init() #Initialize pygame mixer

script_dir = os.path.dirname(os.path.abspath(__file__)) #Get directory of where file is ran from
os.chdir(script_dir) #Change working directory to where file is ran from

SCREEN_WIDTH = 800 #Creating screen width
SCREEN_HEIGHT = 600 #Creating screen height

food_sound = pygame.mixer.Sound("eat_food.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")
background_music = pygame.mixer.Sound("background_music.mp3")

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #Making game window as set width and height

clock = pygame.time.Clock() #Creating game clock

font_style = pygame.font.SysFont(None, 50) #Defining font style

pink = (255, 105, 180) #Food color
black = (0, 0, 0) #Background color
orange = (255, 165, 0) #Enemies Color
green = (57, 255, 20) #Snake color
red = (255, 0, 0) #Game Over text color

block_size = 15 #How big snake, enemies, and food pieces are
snake_speed = 25 #How fast the snake moves
enemy_list = []

def spawnFood(): #Defining spawn food function
    food_x = random.randint(25, 775) #Defining foods x coordinate
    food_y = random.randint(25, 575) #Defining foods y coordinate
    food_Rect = pygame.Rect(food_x, food_y, block_size, block_size) #Making food rectangle
    food_sound.play() #Playing food sound
    return food_Rect #Returning rectangle for game loop

class EnemyClass:
    def __init__(self):
        self.x = random.randint(25, 775)
        self.y = random.randint(25, 575)

def spawnEnemy():
        enemy = EnemyClass()
        enemy_list.append(enemy)

def message(msg, color, pos): #Define message function
    msg = font_style.render(msg, True, color) #When function is called the message and color is passed to function
    screen.blit(msg, pos) #Displaying message center of screen

def runGame(): #Creating the game loop
    background_music.play(-1) #Playing background music

    pygame.display.set_caption("Snake Re-Imagined") #Setting game title

    snake_body = [(395, 295)] #Initialize list with x and y of snake head

    food_rect = None #Initializing food rectangle

    food_count = 0 #Number of food collected

    prev_direction = None

    x1 = 395 #Players starting x-value
    y1 = 295 #Players starting y-value

    x_change = 0 #Store updating x-value
    y_change = 0 #Store updating y-value

    close_game = False #Exit game condition
    while close_game == False: #Keeps gameloop running until close_game is true
     
        if food_count % 10 == 0 and food_count != 0:
            if len(enemy_list) * 10 != food_count:
                spawnEnemy()

        if food_rect is None: 
            food_rect = spawnFood() #Calling spawn food and returning value of rectangle

        for event in pygame.event.get(): #Creating loop event handler
            if event.type == pygame.QUIT: #Hitting the X button
                pygame.quit() #Quits pygame and ends program
                quit()
            if event.type == pygame.KEYDOWN: #Checking if player is pressing a key
                if event.key == pygame.K_a and prev_direction != "right": #When a is pressed
                    prev_direction = "left"
                    x_change = -block_size #Move left
                    y_change = 0
                elif event.key == pygame.K_d and prev_direction != "left": #When d is pressed
                    prev_direction = "right"
                    x_change = block_size #Move right
                    y_change = 0
                elif event.key == pygame.K_w and prev_direction != "down": #When w is pressed
                    prev_direction = "up"
                    x_change = 0
                    y_change = -block_size #Move up
                elif event.key == pygame.K_s and prev_direction != "up": #When s is pressed
                    prev_direction = "down"
                    x_change = 0
                    y_change = block_size #Move down
            
        x1 += x_change
        y1 += y_change

        if x1 < -5 or x1 > 790 or y1 < -5 or y1 > 590:
            gameOver()

        snake_body[0] = (x1, y1) #Update first element in list(snake head) with updated x and y values
        for i in range(len(snake_body) - 1, 0, -1): #Iterate through snake body backwards not including the head 
            snake_body[i] = snake_body[i - 1] #Assign every value the old value of the last element (piece 2 get the x and y of piece 1)

        head_rect = pygame.Rect(snake_body[0][0], snake_body[0][1], block_size, block_size) #Defining the head rectangle for collisions

        screen.fill(black) #Fills screen with black

        if head_rect.colliderect(food_rect): #Check for collision
            snake_body.append(snake_body[-1]) #Add to snake body
            food_rect = spawnFood() #Spawn in new food
            food_count += 1
            if food_count % 10 == 0:
                enemy_spawn_flag = True
        
        for i in range(len(enemy_list)):
            enemy = enemy_list[i]
            enemy_rect = pygame.Rect(enemy.x, enemy.y, block_size, block_size)
            if head_rect.colliderect(enemy_rect):
                gameOver()

        for i in range(3, len(snake_body)): #Iterate through snake body (excluding head and first 2 segments) for collisions
            x, y = snake_body[i] #Unpacking tuple (i) into x and y
            if head_rect.colliderect(x, y, block_size, block_size): #Checking to see if head collided with body
                gameOver() #Calling gameover function

        for x, y in snake_body: #Iterate through snake body again for drawing
            pygame.draw.rect(screen, green, [x, y, block_size, block_size]) #Draw each element in snake body to the screen

        for i in range(len(enemy_list)): #Iterate through enemy list for drawings
            enemy = enemy_list[i]
            enemy_draw = pygame.Rect(enemy.x, enemy.y, block_size, block_size)
            pygame.draw.rect(screen, orange, enemy_draw) #Draw each enemy in list to the screen
        
        pygame.draw.rect(screen, pink, food_rect) #Draw food to screen

        message("Score: " + str(food_count * 1000), red, [10, 10]) #Displaying score

        pygame.display.update( ) #Updates the screen constantly at the end of each loop

        clock.tick(snake_speed) #Snake speed is defined as a global variable

def gameOver():
    game_over_sound.play()
    while True: #If gameover is true
        screen.fill(black) #Fills screen with black
        message("Game Over! Press Q to quit or R to restart", red, [80, 300]) #Display gameover text
        pygame.display.update( ) #Updates the screen
        for event in pygame.event.get(): #Creating loop event handler
            if event.type == pygame.QUIT: #Hitting the X button
                pygame.quit() #Quits pygame and ends program
                quit()
            if event.type == pygame.KEYDOWN: #Checking if player is pressing a key
                if event.key == pygame.K_q: #When q is pressed
                    pygame.quit() #Quits pygame and ends program
                    quit()
                if event.key == pygame.K_r: #When r is pressed
                    enemy_list.clear() #Clearing enemy list
                    runGame() #Restarting the game loop

runGame() #Run the game loop