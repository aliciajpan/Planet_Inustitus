#set up
#_________________________________________________________________________

import pygame
import sys
import random
import time
from pygame.locals import*
pygame.init()

#main game function
#_________________________________________________________________________
def main():
    
    screenx = 800 #screen
    screeny = 500

    screen = pygame.display.set_mode((screenx,screeny))
    pygame.display.set_caption(("Planet Inustitus")) #Inustitus means "odd" in Latin

#initialize
#_________________________________________________________________________

    clock = pygame.time.Clock()
    timer = 3600 #set for 60 seconds
    score = 0

    black = (0,0,0) #RBG colour codes
    white = (255,255,255)

    myfont = pygame.font.SysFont('callisto',60) #setting up text
    text = myfont.render(str(score),1,black)
    text2 = myfont.render(str("of 10"),1,black)

    r = random.randrange(0,6) #used to blit stars randomly
    if r == 0:
        rand_x = 100
    elif r == 1:
        rand_x = 200
    elif r == 2:
        rand_x = 400
    elif r == 3:
        rand_x = 500
    elif r == 4:
        rand_x = 600
    elif r == 5:
        rand_x = 700
    keys = pygame.key.get_pressed()

    x = 700 #dave's initial position
    y = 10

    speed = 0.3 #dave's jump vector
    gravity = -15

#load images
#_________________________________________________________________________
    
    win = pygame.image.load("Win Screen.png") #**no unecessarily .convert()
    lose = pygame.image.load("Lose Screen.png")
    
    respawn = pygame.image.load("Respawn Screen.png")

    bkgd = pygame.image.load("Background.png")
    ground = pygame.image.load("Ground.png")

    player = pygame.image.load("Dave.png")
    dave = player.get_rect()
    dave.left = x
    dave.top = y
    #dave is 80 pixels tall (top at 320)
    #74 pixels wide

    enemy1 = pygame.image.load("Kyle.png") #named kyle
    kyle = enemy1.get_rect()
    kyle.left = 730
    kyle.top = 285

    enemy2 = pygame.image.load("Mike.png") #named mike
    mike = enemy2.get_rect()
    mike.left = 0
    mike.top = 360

    starz = pygame.image.load("Star.png")
    point = starz.get_rect()
    point.left = rand_x
    point.top = 350

#boolean statements
#_________________________________________________________________________

    game = True
    keep_going = True
    game = True
    kyle_right = False
    mike_right = False
    collide = False
    jump = False
    respawning = False

#game
#_________________________________________________________________________
  
    while keep_going: #while actually playing occurs

        keys = pygame.key.get_pressed() #need to be in this loop to work

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                keep_going = False
                game = False #used to quit if player "X"s during gameplay

        if timer != 0: #countdown timer
            timer -= 1
            time_display = timer/60
        timing = myfont.render(str(time_display),1,black)

        if timer <= 0:
            keep_going = False

#blit to enable collision detection
#_________________________________________________________________________

        b = screen.blit(bkgd,(0,0))
        g = screen.blit(ground,(0,400))
        p = screen.blit(player,dave)
        e1 = screen.blit(enemy1,kyle)
        e2 = screen.blit(enemy2,mike)
        s = screen.blit(starz,point)

#player movement
#_________________________________________________________________________
            
        if keys[pygame.K_UP]:
            jump = True
        
        if keys[pygame.K_LEFT]:
            dave.left -= 8
            if dave.left < 0:
                dave.left = 0

        elif keys[pygame.K_RIGHT]:
            dave.left += 8
            if dave.left > 727:
                dave.left = 727

        if jump:
            detect = False
            dave.top += gravity
            gravity += speed
            if dave.top < 0:
                dave.top = 0                

#enemy movement
#_________________________________________________________________________

        #kyle paces back and forth (faster when going left)
        if kyle.left == 730:
            kyle_right = False
            
        if kyle.left == 0:
            kyle_right = True
            
        if not kyle_right: #moving left
            kyle.left -= 5
            if kyle.left <= 0:
                kyle_right = True
                
        if kyle_right:
            kyle.left += 2

        #mike follows the player
        if mike.left >= dave.left:
            mike_right = False
            
        if mike.left <= dave.left:
            mike_right = True
            
        if not mike_right: #moving left
            mike.left -= 1
            if mike.left <= 0:
                mike_right = True
                
        if mike_right:
            mike.left += 1

        #enemies move at different rates to stagger spacing
        #(easier for player to jump over)

#collisions
#_________________________________________________________________________

        if p.colliderect(g): #player touches ground
            collide = True
        else:
            collide = False

        if collide:
            jump = False
            gravity = -15

        if not collide:
            dave.top += 5
            if dave.top >= 320:
                dave.top = 320

        if p.colliderect(e1) or p.colliderect(e2): #player touches enemies
            x = 700
            y = 10
            dave.left = x
            dave.top = y
            p = screen.blit(player,dave)
            timer -= 300
            respawning = True

        if p.colliderect(s): #player collects star
            score += 1
            if r == 0:
                r = random.randrange(2,6)
            elif r == 1:
                r = random.randrange(3,6)
            elif r == 2:
                r = random.randrange(4,6)
            elif r == 3:
                r = random.randrange(5,6)
            elif r == 4:
                r = random.randrange(0,2)
            elif r == 5:
                r = random.randrange(0,3)
            
            if r == 0: #randomize star position again
                rand_x = 100
            elif r == 1:
                rand_x = 200
            elif r == 2:
                rand_x = 400
            elif r == 3:
                rand_x = 500
            elif r == 4:
                rand_x = 600
            elif r == 5:
                rand_x = 700
                
            point.left = rand_x
            point.top = 350
            
            text = myfont.render(str(score),1,black) #change score
            text2 = myfont.render(str("of 10"),1,black)

#screen blits
#_________________________________________________________________________

        screen.blit(bkgd,(0,0))
        screen.blit(ground,(0,400))
        screen.blit(enemy1,kyle)
        screen.blit(enemy2,mike)
        screen.blit(starz,point)
        screen.blit(player,dave)
        screen.blit(text,(50,25))
        screen.blit(text2,(125,25))
        screen.blit(timing,(695,25))

#respawn
#_________________________________________________________________________

        if respawning:
            kyle.left = 730 #set enemies back to starting position
            mike.left = 0   #so player does not immediately die after respawning
            kyle_right = False
            screen.blit(respawn,(0,0))
            pygame.display.update()
            time.sleep(2) #let player read screen
            respawning = False #reset
            gravity = -15 #reset 

#if win before timer runs out
#_________________________________________________________________________
            
        if score == 10: #when 10 points reached (even if timer still running)
            keep_going = False

#end of loop
#_________________________________________________________________________

        pygame.display.update() 
        clock.tick(60) #fps

#after timer runs out
#_________________________________________________________________________
        
    if not keep_going:

        if not game: #total quit
            pygame.display.quit()

        if score == 10:

            screen.blit(win,(0,0))
            pygame.display.update()
            time.sleep(6) #let player read screen
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                         main() #play from main screen 

        if score < 10: #when timer stops running but score too low

            if game:
                screen.blit(lose,(0,0))
                pygame.display.update()
                time.sleep(6) #let player read screen
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                         main() #play from main screen 

        #pygame.display.update() need again (separate loop)

#start screen
#_________________________________________________________________________

#outside of loops; first screen
start = pygame.image.load("Start Screen.png")

screen = pygame.display.set_mode((800,500))
pygame.display.set_caption(("Planet Inustitus"))

keep_running = True

while keep_running: #own loop
    
    screen.blit(start,(0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_running = False
            pygame.quit();sys.exit();
            quit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                main() #play game
         
    pygame.display.update() #need again (separate loop)

pygame.display.quit() #exit game
