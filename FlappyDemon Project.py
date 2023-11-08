# For generating random height of pillars
import random
import sys
import pygame
from pygame.locals import *

# Global Variables for the game
window_width = 600
window_height = 499

# Set height and width of window
window = pygame.display.set_mode((window_width, window_height))
elevation = window_height * 0.8
game_images = {}
framepersecond = 32
pillar = "pillar.png"
background_image = "space.png"
demon_image = "demon.png"
ground_level_image = "lava1.png"

def demonflap(): 
    your_score = 0
    horizontal = int(window_width/5) 
    vertical = int(window_width/2) 
    ground = 0
    temp_height = 100
  
    # Generating two pillars for blitting on window 
    first_pillar = createpillar() 
    second_pillar = createpillar() 
  
    # List containing lower pillars 
    down_pillars = [ 
        {'x': window_width+300-temp_height, 
         'y': first_pillar[1]['y']}, 
        {'x': window_width+300-temp_height+(window_width/2), 
         'y': second_pillar[1]['y']}, 
    ] 
  
    # List Containing upper pillars 
    up_pillars = [ 
        {'x': window_width+300-temp_height, 
         'y': first_pillar[0]['y']}, 
        {'x': window_width+200-temp_height+(window_width/2), 
         'y': second_pillar[0]['y']}, 
    ] 
  
    # pillar velocity along x 
    pillarVelX = -4
  
    # demon velocity 
    demon_velocity_y = -9
    demon_Max_Vel_Y = 10
    demon_Min_Vel_Y = -8
    demonAccY = 1
  
    demon_flap_velocity = -8
    demon_flapped = False
    while True: 
        for event in pygame.event.get(): 
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): 
                pygame.quit() 
                sys.exit() 
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP): 
                if vertical > 0: 
                    demon_velocity_y = demon_flap_velocity 
                    demon_flapped = True
  
        # This function will return true 
        # if the flappydemon is dead
        game_over = isGameOver(horizontal, 
                               vertical, 
                               up_pillars, 
                               down_pillars) 
        if game_over: 
            return
  
        # check for your_score 
        player_mid_position = horizontal + game_images["demon"].get_width()/2
        for pillar in up_pillars: 
            pillar_mid_position = pillar['x'] + game_images['pillar'][0].get_width()/2
            if pillar_mid_position <= player_mid_position < pillar_mid_position + 4: 
                your_score += 1
                print(f"Your your_score is {your_score}") 
  
        if demon_velocity_y < demon_Max_Vel_Y and not demon_flapped: 
            demon_velocity_y += demonAccY 
  
        if demon_flapped: 
            demon_flapped = False
        playerHeight = game_images['demon'].get_height() 
        vertical = vertical + min(demon_velocity_y, elevation - vertical - playerHeight) 
  
        # move pillars to the left 
        for upperpillar, lowerpillar in zip(up_pillars, down_pillars): 
            upperpillar['x'] += pillarVelX 
            lowerpillar['x'] += pillarVelX 
  
        # Add a new pillar when the first is 
        # about to cross the leftmost part of the screen 
        if 0 < up_pillars[0]['x'] < 5: 
            newpillar = createpillar() 
            up_pillars.append(newpillar[0]) 
            down_pillars.append(newpillar[1]) 
  
        # if the pillar is out of the screen, remove it 
        if up_pillars[0]['x'] < -game_images['pillar'][0].get_width(): 
            up_pillars.pop(0) 
            down_pillars.pop(0) 
  
        # Lets blit our game images now 
        window.blit(game_images['background'], (0, 0)) 
        for upperpillar, lowerpillar in zip(up_pillars, down_pillars): 
            window.blit(game_images['pillar'][0], 
                        (upperpillar['x'], upperpillar['y'])) 
            window.blit(game_images['pillar'][1], 
                        (lowerpillar['x'], lowerpillar['y'])) 
  
        window.blit(game_images['ground_level'], (ground, elevation)) 
        window.blit(game_images['demon'], (horizontal, vertical)) 
  
        # Fetching score art. 
        numbers = [int(x) for x in list(str(your_score))] 
        width = 0
  
        # finding the width of score images from numbers. 
        for num in numbers: 
            width += game_images['scoreimages'][num].get_width() 
        Xoffset = (window_width - width)/1.1
  
        # Blitting the images on the window. 
        for num in numbers: 
            window.blit(game_images['scoreimages'][num], 
                        (Xoffset, window_width*0.02)) 
            Xoffset += game_images['scoreimages'][num].get_width() 
  
        # Refreshing the game window and displaying the score. 
        pygame.display.update() 
        framepersecond_clock.tick(framepersecond) 
  
  
def isGameOver(horizontal, vertical, up_pillars, down_pillars): 
    if vertical > elevation - 25 or vertical < 0: 
        return True
  
    for pillar in up_pillars: 
        pillarHeight = game_images['pillar'][0].get_height() 
        if(vertical < pillarHeight + pillar['y'] and abs(horizontal - pillar['x']) < game_images['pillar'][0].get_width()): 
            return True
  
    for pillar in down_pillars: 
        if (vertical + game_images['demon'].get_height() > pillar['y']) and abs(horizontal - pillar['x']) < game_images['pillar'][0].get_width():
            return True
    return False
  
def createpillar(): 
    offset = window_height/3
    pillarHeight = game_images['pillar'][0].get_height() 
    y2 = offset + random.randrange( 
            0, int(window_height - game_images['ground_level'].get_height() - 1.2 * offset))   
    pillarX = window_width + 10
    y1 = pillarHeight - y2 + offset 
    pillar = [ 
        # upper pillar 
        {'x': pillarX, 'y': -y1}, 
  
        # lower pillar 
        {'x': pillarX, 'y': y2} 
    ] 
    return pillar 

# program where the game starts
if __name__ == "__main__":
    
    # For initializing modules of pygame library
    pygame.init()
    framepersecond_clock = pygame.time.Clock()
    
    # Sets the title on top of game window
    pygame.display.set_caption("Flappy Demon Game")
    
    # Load all the images which we will use in the game
    # images for displaying score
    game_images["scoreimages"] = (
        pygame.image.load("new0.png").convert_alpha(),
        pygame.image.load("new1.png").convert_alpha(),
        pygame.image.load("new2.png").convert_alpha(),
        pygame.image.load("new3.png").convert_alpha(),
        pygame.image.load("new4.png").convert_alpha(),
        pygame.image.load("new5.png").convert_alpha(),
        pygame.image.load("new6.png").convert_alpha(),
        pygame.image.load("new7.png").convert_alpha(),
        pygame.image.load("new8.png").convert_alpha(),
        pygame.image.load("new9.png").convert_alpha(),
    )
    game_images["demon"] = pygame.image.load(demon_image).convert_alpha()
    game_images["ground_level"] = pygame.image.load(ground_level_image).convert_alpha()
    game_images["background"] = pygame.image.load(background_image).convert_alpha()
    game_images["pillar"] = (pygame.transform.rotate(pygame.image.load(pillar).convert_alpha(),180),
                                pygame.image.load(pillar).convert_alpha())
    
    print("WELCOME TO THE FLAPPY DEMON GAME")
    print("Press space or enter to start the game")
    
    # Creating the loop
    while True:
        
        # sets the coordinates of flappy demon
        horizontal = int(window_width/5)
        vertical = int((window_height - game_images["demon"].get_height())/2)
        
        # For ground_level
        ground = 0
        while True:
            for event in pygame.event.get():
                
                # if user clicks on cross button, close the game
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    
                    # Exit Program
                    sys.exit()
                    
                #If user presses space or up key, starts game.
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    demonflap()
                    
                # if user doesnt press anything nothing happens
                else:
                    window.blit(game_images["background"], (0, 0))
                    window.blit(game_images["demon"], (horizontal, vertical))
                    window.blit(game_images["ground_level"], (ground, elevation))
                    
                    # Refresh the screen
                    pygame.display.update()
                    
                    # Set the rate of frame per second
                    framepersecond_clock.tick(framepersecond)
           