import pygame
import random
import math
from pygame import mixer

pygame.init() # initialise the pygame

# create the screen
width=800
height=600
screen=pygame.display.set_mode((width,height)) 

# background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invaders")
icon=pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# player
playerImg=pygame.image.load("spaceship.png")
px=width/2-30
py=height-80
pxChange=0

# score
scoreVal=0
scoreFont=pygame.font.Font("freesansbold.ttf",24)
textX=10
textY=10
def showScore(x,y):
    score=scoreFont.render("Score: "+str(scoreVal),True,(200,200,200))
    screen.blit(score,(x,y))
    

# enemy
enemyImg=[]
ex=[]
ey=[]
exChange=[]
eyChange=[]
n=6
for i in range(0,n):
    enemyImg.append(pygame.image.load("enemy.png"))
    ex.append(random.randint(0,width))
    ey.append(random.randint(50,200))
    exChange.append(0.3)
    eyChange.append(40)

# bullet
bulletImg=pygame.image.load("bullet.png")
bx=0
by=height-80
bxChange=0
byChange=1
bState="ready" # bullet can't be seen on the screen

def player(x,y):
    screen.blit(playerImg,(x,y))
    
def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))
    
def fireBullet(x,y):
    global bState
    bState="fire"
    screen.blit(bulletImg,(x+16,y+10))

def isCollision(ex,ey,bx,by):
    distance=math.sqrt(math.pow(ex-bx,2)+math.pow(ey-by,2))    
    if distance< 27:
        return True
    return False

# game over
overFont=pygame.font.Font("freesansbold.ttf",54)
def gameOver():
    over=overFont.render("GAME OVER!",True,(220,0,0))
    screen.blit(over,(width/2-160,height/2-30))

# game loop
running=True
while running:
    screen.fill((0,0,60))
    for event in pygame.event.get():# iterate through all the events
        if event.type==pygame.KEYDOWN:# if a key is pressed
            if event.key==pygame.K_LEFT:
                # print("left arrow")
                # px-=0.1
                pxChange=-0.5
            if event.key==pygame.K_RIGHT:
                # print("right arrow")?
                # px+=0.1
                pxChange=0.5
        if event.type==pygame.KEYUP:# if a key is released
            if event.key==pygame.K_LEFT:
                # print("released")
                # px-=0
                pxChange=0
            if event.key==pygame.K_RIGHT:
                # print("released")
                # px+=0
                pxChange=0
            if event.key==pygame.K_SPACE:
                if bState=='ready':
                    bSound=mixer.Sound("laser.wav")
                    bSound.play()
                    fireBullet(px,by)
                    bx=px
            
        if event.type==pygame.QUIT:
            running=False
    
    # movement of space ship and enemy        
    px+=pxChange
    
    # checking for boundaries
    if px<=0:
        px=0
    elif px>=(width-64):
        px=(width-64)
    
    for i in range(0,n):
        if(ey[i]>height-150):
            for j in range(0,n):
                ey[j]=2000
            gameOver()
            break
        ex[i]+=exChange[i]
        if ex[i]<=0:
            exChange[i]=0.2
            ey[i]+=eyChange[i]
        elif ex[i]>=(width-64):
            exChange[i]=-0.2
            ey[i]+=eyChange[i]
        # collision
        col=isCollision(ex[i],ey[i],bx,by)
        if col:
            cSound=mixer.Sound("explosion.wav")
            cSound.play()
            by=width-80
            bState="ready"
            scoreVal+=2
            ex[i]=random.randint(0,width-64-1)
            ey[i]=random.randint(50,200)
        
        enemy(ex[i],ey[i],i)
    # bullet movement
    if by<=0:
        bState="ready"
        by=height-80
        
    if bState=="fire":
        fireBullet(bx,by)
        by-=byChange
        
    
        
    player(px,py)
    showScore(textX,textY)
    pygame.display.update() # after changing anything on the screen
    
    
    
    
    