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

class character:
    def __init__(self, x_start, y_start, height, width, name):
        self.x_start = x_start
        self.y_start = y_start
        self.height = height
        self.width = width
        self.x_change = 0
        self.y_change = 4
        self.boost_counter = 0
        self.x = x_start
        self.y = y_start
        self.old_x = self.x
        self.falling = False
        self.boost = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.name = name

xbox = character(100, 300, 50, 60, "xbox")
hatsune = character(1000, 300, 60, 60, "hatsune")

# set game window stats
game_display = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('PCSoc is best soc')
clock = pygame.time.Clock()

xbox.sprite = pygame.image.load('images/pcsoc_logo.png')
xbox.sprite = pygame.transform.scale(xbox.sprite, (xbox.width, xbox.height))

hatsune.sprite = pygame.image.load('images/gamedev_white.png')
hatsune.sprite = pygame.transform.scale(hatsune.sprite, (hatsune.width, hatsune.height))

boundary_right_rect = pygame.Rect(1250, 0, 30, 720)
boundary_left_rect = pygame.Rect(0, 0, 30, 720)
boundary_top_rect = pygame.Rect(0, 0, 1280, 30)
boundary_bottom_rect = pygame.Rect(30, 700, 1280, 720)

def check_boundary_collision(character):
    # boundary collisions
    if ((character.rect.colliderect(boundary_right_rect) and character.x_change > 0) or
    (character.rect.colliderect(boundary_left_rect) and character.x_change < 0)):
        charcter.x_change = 0

    if ((character.rect.colliderect(boundary_top_rect) and character.y_change < 0) or
        (character.rect.colliderect(boundary_bottom_rect) and character.y_change > 0)):
        character.y_change = 0

def check_character_collision(char_one, char_two):
    # character collisions
    if (char_one.rect.colliderect(char_two.rect)):
        if ((char_one.x_change > 0) and 
        (char_one.y in range(int(char_two.y - char_two.height / 2), int(char_two.y + char_two.height / 2)))):
            if char_one.x < char_two.x:
                char_one.x_change = 0
        if char_one.x_change < 0 and char_one.y in range(int(char_two.y - char_two.height / 2), int(char_two.y + char_two.height / 2)):
            if char_one.x > char_two.x:
                char_one.x_change = 0
        if (char_one.x in range(int(char_two.x - char_two.width / 2), int(char_two.x + char_two.width / 2)) and char_one.y < int(char_two.y + char_two.height / 2)):
            char_one.y_change = 0

    # check if one player on top of the other
    if (char_one.rect.colliderect(char_two.rect)):
        if ((char_one.y + char_one.height / 2) in range(int(char_two.y - char_two.height / 2), int(char_two.y)) and
            (char_one.x in range(int(char_two.x - char_two.width / 2), int(char_two.x + char_two.width / 2)))):
            char_two.rect = pygame.Rect(char_two.x_start, char_two.y_start, char_two.width, char_two.height)
            char_two.x = char_two.x_start
            char_two.y  = char_two.y_start
            char_one.y_change = 4
            char_two.y_change = 4

def level_one():
    global xbox
    global hatsune
    xbox.boost_counter += 1
    hatsune.boost_counter += 1
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
        #        xbox.y_change = -4

        #if event.type == pygame.JOYBUTTONUP:
        #    if not joystick.get_button(0):
        #        xbox.y_change = 0

        # key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                xbox.x_change = -4
            elif event.key == pygame.K_d:
                xbox.x_change = 4
            elif event.key == pygame.K_w:
                xbox.y_change = -5
            elif event.key == pygame.K_s:
                xbox.y_change = 9
                xbox.falling = True
            elif event.key == pygame.K_LSHIFT:
                if xbox.boost_counter > 300:
                    xbox.direction = xbox.x_change
                    xbox.old_x = xbox.x
                    xbox.boost = True
            elif event.key == pygame.K_RSHIFT:
                if hatsune.boost_counter > 300:
                    hatsune.direction = hatsune.x_change
                    hatsune.old_x = hatsune.x
                    hatsune.boost = True
            elif event.key == pygame.K_LEFT:
                hatsune.x_change = -4
            elif event.key == pygame.K_RIGHT:
                hatsune.x_change = 4
            elif event.key == pygame.K_UP:
                hatsune.y_change = -5
            elif event.key == pygame.K_DOWN:
                hatsune.y_change = 9
                hatsune.falling = True

        # key releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                xbox.x_change = 0
            if event.key == pygame.K_s or event.key == pygame.K_w:
                xbox.y_change = 4
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
               hatsune.x_change = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
               hatsune.y_change = 4

    if xbox.falling:
        if xbox.rect.colliderect(boundary_bottom_rect):
            xbox.y_change = 4
            xbox.falling = False
        else:
            xbox.y_change = 9

    if xbox.boost:
        if xbox.direction > 0:
            if xbox.x < xbox.old_x + 90:
                xbox.x_change = 10
            else:
                xbox.x_change = 4
                xbox.boost = False
                xbox.boost_counter = 0
        else:
            if xbox.x > xbox.old_x - 90:
                xbox.x_change = - 10
            else:
                xbox.x_change = -4
                xbox.boost = False
                xbox.boost_counter = 0

    if hatsune.falling:
        if hatsune.rect.colliderect(boundary_bottom_rect):
            hatsune.y_change = 4
            hatsune.falling = False
        else:
            hatsune.y_change = 9
            
    if hatsune.boost:
        if hatsune.direction > 0:
            if hatsune.x < hatsune.old_x + 90:
                hatsune.x_change = 10
            else:
                hatsune.x_change = 4
                hatsune.boost = False
                hatsune.boost_counter = 0
        else:
            if hatsune.x > hatsune.old_x - 90:
                hatsune.x_change = - 10
            else:
                hatsune.x_change = -4
                hatsune.boost = False
                hatsune.boost_counter = 0

    # boundary collisions
    check_boundary_collision(xbox)
    check_boundary_collision(hatsune)

    # character collisions
    check_character_collision(xbox, hatsune)
    check_character_collision(hatsune, xbox)

    xbox.rect.move_ip(xbox.x_change, xbox.y_change)
    hatsune.rect.move_ip(hatsune.x_change, hatsune.y_change)
    xbox.x += xbox.x_change
    xbox.y += xbox.y_change
    hatsune.x += hatsune.x_change
    hatsune.y += hatsune.y_change
  
    game_display.fill(bg_color)
    game_display.blit(xbox.sprite, xbox.rect)
    game_display.blit(hatsune.sprite, hatsune.rect)
    pygame.display.update() 
    clock.tick(60) # 60 FPS

while True:
    level_one()
