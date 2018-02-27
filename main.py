import pygame
import sys

pygame.init()
#pygame.joystick.init()
#joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
#joystick = pygame.joystick.Joystick(0)
#joystick.init()

window_width = 1280
window_height = 720

bg_color = (169,169,169)

pcsoc_x_start = 100
pcsoc_y_start = 300
pcsoc_x_change = 0
pcsoc_y_change = 4
pcsoc_x = pcsoc_x_start
pcsoc_y = pcsoc_y_start
pcsoc_old_x = pcsoc_x
pcsoc_falling = False 
pcsoc_boost = False

gamedev_x_start = 1000
gamedev_y_start = 300
gamedev_x_change = 0
gamedev_y_change = 4
gamedev_x = gamedev_x_start
gamedev_y = gamedev_y_start
gamedev_falling = False
gamedev_boost = False

# set game window stats
game_display = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('PCSoc is best soc')
clock = pygame.time.Clock()

pcsoc_width = 50
pcsoc_height = 60
pcsoc_rect = pygame.Rect(pcsoc_x, pcsoc_y, pcsoc_width, pcsoc_height)
pcsoc_sprite = pygame.image.load('images/pcsoc_logo.png')
pcsoc_sprite = pygame.transform.scale(pcsoc_sprite, (pcsoc_width, pcsoc_height))

gamedev_width = 60
gamedev_height = 60
gamedev_rect = pygame.Rect(gamedev_x, gamedev_y, gamedev_width, gamedev_height)
gamedev_sprite = pygame.image.load('images/gamedev_white.png')
gamedev_sprite = pygame.transform.scale(gamedev_sprite, (gamedev_width, gamedev_height))

boundary_right_rect = pygame.Rect(1250, 0, 30, 720)
boundary_left_rect = pygame.Rect(0, 0, 30, 720)
boundary_top_rect = pygame.Rect(0, 0, 1280, 30)
boundary_bottom_rect = pygame.Rect(30, 700, 1280, 720)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
        # Controller stuff, do this later
        #if event.type == pygame.JOYBUTTONDOWN:
        #    print("Pressed joystick button")
        #    print("Joystick button: " + str(joystick.get_button(0)))

        #if event.type == pygame.JOYBUTTONDOWN:
        #    if joystick.get_button(0):
        #        pcsoc_y_change = -4

        #if event.type == pygame.JOYBUTTONUP:
        #    if not joystick.get_button(0):
        #        pcsoc_y_change = 0

        # key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                pcsoc_x_change = -4
            elif event.key == pygame.K_d:
                pcsoc_x_change = 4
            elif event.key == pygame.K_w:
                pcsoc_y_change = -5
            elif event.key == pygame.K_s:
                pcsoc_y_change = 9
                pcsoc_falling = True
            elif event.key == pygame.K_LSHIFT:
                pcsoc_direction = pcsoc_x_change
                pcsoc_old_x = pcsoc_x
                pcsoc_boost = True
            elif event.key == pygame.K_LEFT:
                gamedev_x_change = -4
            elif event.key == pygame.K_RIGHT:
                gamedev_x_change = 4
            elif event.key == pygame.K_UP:
                gamedev_y_change = -5
            elif event.key == pygame.K_DOWN:
                gamedev_y_change = 9
                gamedev_falling = True

        # key releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                pcsoc_x_change = 0
            if event.key == pygame.K_s or event.key == pygame.K_w:
                pcsoc_y_change = 4
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
               gamedev_x_change = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
               gamedev_y_change = 4

    if pcsoc_falling:
        if pcsoc_rect.colliderect(boundary_bottom_rect):
            pcsoc_y_change = 4
            pcsoc_falling = False
        else:
            pcsoc_y_change = 9

    if pcsoc_boost:
        if pcsoc_direction > 0:
            if pcsoc_x < pcsoc_old_x + 50:
                pcsoc_x_change = 10
            else:
                pcsoc_x_change = 4
                pcsoc_boost = False
        else:
            if pcsoc_x > pcsoc_old_x - 50:
                pcsoc_x_change = - 10
            else:
                pcsoc_x_change = -4
                pcsoc_boost = False

    if gamedev_falling:
        if gamedev_rect.colliderect(boundary_bottom_rect):
            gamedev_y_change = 4
            gamedev_falling = False
        else:
            gamedev_y_change = 9

    # boundary collisions
    if ((pcsoc_rect.colliderect(boundary_right_rect) and pcsoc_x_change > 0) or
    (pcsoc_rect.colliderect(boundary_left_rect) and pcsoc_x_change < 0)):
        pcsoc_x_change = 0

    if ((pcsoc_rect.colliderect(boundary_top_rect) and pcsoc_y_change < 0) or
        (pcsoc_rect.colliderect(boundary_bottom_rect) and pcsoc_y_change > 0)):
        pcsoc_y_change = 0

    if ((gamedev_rect.colliderect(boundary_right_rect) and gamedev_x_change > 0) or
        (gamedev_rect.colliderect(boundary_left_rect) and gamedev_x_change < 0)):
        gamedev_x_change = 0

    if ((gamedev_rect.colliderect(boundary_top_rect) and gamedev_y_change < 0) or
        (gamedev_rect.colliderect(boundary_bottom_rect) and gamedev_y_change > 0)):
        gamedev_y_change = 0

    # character collisions
    if (pcsoc_rect.colliderect(gamedev_rect)):
        if pcsoc_x_change > 0 and pcsoc_y in range(int(gamedev_y - gamedev_height / 2), int(gamedev_y + gamedev_height / 2)):
            if pcsoc_x < gamedev_x:
                pcsoc_x_change = 0
        if pcsoc_x_change < 0 and pcsoc_y in range(int(gamedev_y - gamedev_height / 2), int(gamedev_y + gamedev_height / 2)):
            if pcsoc_x > gamedev_x:
                pcsoc_x_change = 0
        if (pcsoc_x in range(int(gamedev_x - gamedev_width / 2), int(gamedev_x + gamedev_width / 2)) and pcsoc_y < int(gamedev_y + gamedev_height / 2)):
            pcsoc_y_change = 0
            
        if gamedev_x_change > 0 and gamedev_y in range(int(pcsoc_y - pcsoc_height / 2), int(pcsoc_y + pcsoc_height / 2)):
            if gamedev_x < pcsoc_x:
                gamedev_x_change = 0
        if gamedev_x_change < 0 and gamedev_y in range(int(pcsoc_y - pcsoc_height / 2), int(pcsoc_y + pcsoc_height / 2)):
            if gamedev_x > pcsoc_x:
                gamedev_x_change = 0
        if (gamedev_x in range(int(pcsoc_x - pcsoc_width / 2), int(pcsoc_x + pcsoc_width / 2)) and gamedev_y < int(pcsoc_y + pcsoc_height / 2)):
            gamedev_y_change = 0

    # check if one player on top of the other
    if (pcsoc_rect.colliderect(gamedev_rect)):
        if ((pcsoc_y + pcsoc_height / 2) in range(int(gamedev_y - gamedev_height / 2), int(gamedev_y)) and
            (pcsoc_x in range(int(gamedev_x - gamedev_width / 2), int(gamedev_x + gamedev_width / 2)))):
            gamedev_rect = pygame.Rect(gamedev_x_start, gamedev_y_start, gamedev_width, gamedev_height)
            gamedev_x = gamedev_x_start
            gamedev_y  = gamedev_y_start
            pcsoc_y_change = 4
            gamedev_y_change = 4

    if (gamedev_rect.colliderect(pcsoc_rect)):
        if ((gamedev_y + gamedev_height / 2) in range(int(pcsoc_y - pcsoc_height / 2), int(pcsoc_y)) and
            (gamedev_x in range(int(pcsoc_x - pcsoc_width / 2), int(pcsoc_x + pcsoc_width / 2)))):
            pcsoc_rect = pygame.Rect(pcsoc_x_start, pcsoc_y_start, pcsoc_width, pcsoc_height)
            pcsoc_x = pcsoc_x_start
            pcsoc_y  = pcsoc_y_start
            gamedev_y_change = 4
            pcsoc_y_change = 4 

    pcsoc_rect.move_ip(pcsoc_x_change, pcsoc_y_change)
    gamedev_rect.move_ip(gamedev_x_change, gamedev_y_change)
    pcsoc_x += pcsoc_x_change
    pcsoc_y += pcsoc_y_change
    gamedev_x += gamedev_x_change
    gamedev_y += gamedev_y_change
  
    game_display.fill(bg_color)
    game_display.blit(pcsoc_sprite, pcsoc_rect)
    game_display.blit(gamedev_sprite, gamedev_rect)
    pygame.display.update() 
    clock.tick(60) # 60 FPS
