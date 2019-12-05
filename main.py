#importing modules
import pygame
import random #to randomize the enemy position
import math
from pygame import mixer
#Initializing pygame
pygame.init()

#Create screen
screen = pygame.display.set_mode((800, 600))
#background
background = pygame.image.load("spacebg.jpg")
#background music
mixer.music.load("background.wav")
mixer.music.play(-1)
#title and Icon
pygame.display.set_caption("Space Fight")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

#player position now
playerimg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_move = 0
#number of enemies
enemyimg = []
enemyX = []
enemyY = []
enemyX_move = []
enemyY_move = []
num_of_enemies = 6
#enemy random position
for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(1, 130))
    enemyX_move.append(1)
    enemyY_move.append(80)

#Bullet position
# ready is when you can not see bullet on screen
# fire is when the bullet is moving
#taking bullet initial position at 480 at y because its where our spaceship is

bulletimg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_move = 0
bulletY_move =5
bullet_state = "Ready"

#score
score_val  = 0
font = pygame.font.Font("freesansbold.ttf", 25)
textX = 10
textY = 10

#game over text
gameover = pygame.font.Font("freesansbold.ttf", 100)

def show_score(x, y):
    score = font.render("Score:" + str(score_val), True, (255,255,255))
    screen.blit(score, (x,y))

#defining the player 
def player(x, y):
    screen.blit(playerimg, (x, y))

#for enemy
def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

#for bullet
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x+16, y+34))
    
#for collision
def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance <= 15:
        return True

#for game over
def game_over_text():
    GAME_OVER = gameover.render("GAME OVER", True, (255,255,255))
    screen.blit(GAME_OVER, (250, 300))

    
#Game Loop
    
running = True
while running:

# Screen backgroun RGB
    screen.fill((10, 50, 96))
#background
    screen.blit(background, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
# Cheking and giving keyboard input(direction of player)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
               playerX_move = -3
            if event.key == pygame.K_RIGHT:
                playerX_move = 3
            if event.key == pygame.K_UP:
               if bullet_state is "Ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_move = 0
#change player position

#making boundaries to player can't move beyond screen
#in actual we are making the value to orignal value by deleting any further increament or decrease in value 
#just by using if else loop

#also making x max to 736 just because our space ship size is 64 and we are deleting 64 from 800 so that 
#it will not go beyond the screen 

#this will happen so fast that human eye can not see the change and it will look like there is a restricted boundry
#changing player direction
    playerX = playerX + playerX_move
    if playerX <= 0:         #if spaceship go beyond 0 like -10, -100 etc
        playerX = 0         #we are making that again zero continously
    elif playerX >=736:        #if spaceship go beyong that 736 like 800, 100 etc
        playerX = 736       #it will again and again come to 736 position.

#changing enemy location
    for i in range(num_of_enemies):
        if enemyY[i] > 450:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_move[i]
        if enemyX[i] <= 0:         
            enemyX_move[i] = 1    
            enemyY[i] += enemyY_move[i] 
        elif enemyX[i] >= 736:        
            enemyX_move[i] = -1
            enemyY[i] += enemyY_move[i]
    #collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision is True:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "Ready"
            score_val += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(1, 130)
#calling enemy funtion
        enemy(enemyX[i], enemyY[i], i)
#bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "Ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_move
        
#score funtion
    show_score(textX, textY)
#calling player function
    player(playerX, playerY)
#updating display for the background color RGB
    pygame.display.update()
