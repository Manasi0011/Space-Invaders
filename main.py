import pygame as pg
import random
import math

# Initializing the pygame module
pg.init()

# create the screen -- set_mode(width, height)
# Y axis top to bottom +ve
# X axis left to right +ve
screen = pg.display.set_mode((900, 700))

# Title and Icon
pg.display.set_caption("Space Invaders")
icon = pg.image.load("asteroid.png")
background = pg.image.load("background1.jpg")
pg.display.set_icon(icon)

# Player
playerImg = pg.image.load("spaceship.png")
playerPosX = 450
playerPosY = 600
playerChangeX = 0
playerChangeY = 0

# Enemy
enemyImg = []
enemyPosX = []
enemyPosY = []
enemyChangeX = []
enemyChangeY = []
numOfEnemies = 10

for i in range(numOfEnemies):
    enemyImg.append(pg.image.load("ufo.png"))
    enemyPosX.append(random.randint(0, 800))
    enemyPosY.append(random.randint(50, 350))
    enemyChangeX.append(0.5)
    enemyChangeY.append(30)

# Bullet
bulletImg = pg.image.load("bullet.png")
bulletPosX = 0
bulletPosY = 0
bulletChangeX = 0
bulletChangeY = 0.5
# two states for the bullet
# Ready - you can't see the bullet on the screen
# Fire - moving bullet
bulletState = "ready"

# Keeping the score
score = 0
font = pg.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over Text
gameOverFont = pg.font.Font('freesansbold.ttf', 70)


def displayScore(x, y):
    # render text on the screen
    sc = font.render("SCORE :" + str(score), True, (255, 255, 255))
    # blit on screen
    screen.blit(sc, (x, y))


def gameOverText(x, y):
    # render text on the screen
    sc = gameOverFont.render("GAME OVER", True, (255, 255, 255))
    # blit on screen
    screen.blit(sc, (x, y))


def player(x, y):
    # drawing player on the screen
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    # drawing player on the screen
    screen.blit(enemyImg[i], (x, y))


def fireBullet(x, y):
    # fire the bullet from the ship
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x + 24, y + 1))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    # distance between two points
    distance = math.sqrt((math.pow((enemyX - bulletX), 2) + math.pow((enemyY - bulletY), 2)))
    if distance <= 27:
        return True
    else:
        return False


# Game Loop

running = True
playerKeys = [pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN]

while running:
    # Changing the background of the window
    # R G B values
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    # Every iteration is slow coz it has to load this heavy file

    for event in pg.event.get():  # checking through the event list that get() returns
        if event.type == pg.QUIT:  # event type is an int, when it takes the val of const QUIT we stop display
            running = False  # when X is pressed QUIT is triggered

        # If any keystroke is pressed check whether it is left or right
        if event.type == pg.KEYDOWN:
            # print("A keystroke is pressed")
            if event.key == pg.K_LEFT:
                playerChangeX = -0.7
            elif event.key == pg.K_RIGHT:
                playerChangeX = 0.7
            elif event.key == pg.K_SPACE:
                fireBullet(playerPosX, playerPosY)
                # get the current coordinates of the spaceship
                bulletPosX = playerPosX
                bulletPosY = playerPosY
            else:
                pass
        if event.type == pg.KEYUP:
            # print("key released")
            if event.key in playerKeys:
                playerChangeX = 0
                playerChangeY = 0

    playerPosX += playerChangeX
    playerPosY += playerChangeY
    player(playerPosX, playerPosY)

    # Checking for boundaries of ship
    if playerPosX <= 0 or playerPosX >= 836:
        playerPosX += -playerChangeX
    if playerPosY <= 0 or playerPosY >= 636:
        playerPosY += -playerChangeY

    # Enemy movement
    for i in range(numOfEnemies):

        # Game Over
        if enemyPosY[i] > 550:
            for j in range(numOfEnemies):
                enemyPosY[j] = 2000 # moving all the enemies out of the screen
            gameOverText(250, 320)
            break

        enemyPosX[i] += enemyChangeX[i]
        if enemyPosX[i] <= 3:
            enemyChangeX[i] = 0.3
            enemyPosY[i] += enemyChangeY[i]
        if enemyPosX[i] >= 800:
            enemyChangeX[i] = -0.3
            enemyPosY[i] += enemyChangeY[i]

        # Collisions
        collision = isCollision(enemyPosX[i], enemyPosY[i], bulletPosX, bulletPosY)
        if collision:
            bulletPosY = playerPosY
            bulletState = "ready"
            score += 10
            enemyPosX[i] = random.randint(0, 800)
            enemyPosY[i] = random.randint(50, 500)

        enemyPosX[i] += enemyChangeX[i]
        enemy(enemyPosX[i], enemyPosY[i], i)

    # Bullet movement
    if bulletPosY <= 0:
        bulletPosY = playerPosY
        bulletState = "ready"
    if bulletState == "fire":
        fireBullet(bulletPosX, bulletPosY)
        bulletPosY -= bulletChangeY

    displayScore(textX, textY)
    pg.display.update()
    # updating the window with the new information
