import pygame

pygame.init()

pygame.display.set_caption('Day to Night')

fpsClock = pygame.time.Clock()

# Screen set up 
size=[700, 500]
screen = pygame.display.set_mode(size)

# Colours 
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0, 255, 0)
BLUE = (0, 191, 255) 
BROWN = (100,40,0)
BLACK=(0,0,0)
YELLOW = (255, 255, 0)
DARK_GREY = (82, 82, 82)
BOTTOM=(51, 252, 40)
TREE_BOTTOM=(153,89,49)
LEAFS=(57,138,30)
BASE=(189,203,240)

# Coordinates for the sun 
posX = 525
posY = 100
# Coordinates for the moon 
posX_M = 525
posY_M = 370

# Loop
while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
         pygame.quit()

    screen.fill(BLUE)
    # When the sun sets, turn the scene into night
    if posY >= 410: 
      screen.fill(BLACK)
      moon = pygame.draw.circle(screen, WHITE, (posX_M, posY_M), 30) # Draw the moon
      posY_M -= 5 # Make the moon rise up 
      if posY_M < 100:
        posY_M = 100 # Get the moon to stop at a certain point 
       

    # Draw the sun 
    sun = pygame.draw.circle(screen, YELLOW, (posX,posY), 30)
    posY += 5
  
    pygame.display.update()
    fpsClock.tick(10)