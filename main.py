import pygame
import sys

pygame.init()
#pygame.joystick.init()
#joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
#joystick = pygame.joystick.Joystick(0)
#joystick.init()

window_width = 1920
window_height = 1080

bg_color = (169,169,169)

class character:
    def __init__(self, x_start, y_start, height, width, name):
        self.x_start = x_start
        self.y_start = y_start
        self.height = height 
        self.width = width 
        self.x_change = 0
        self.y_change = 5
        self.boost_counter = 0
        self.x = x_start
        self.y = y_start
        self.old_x = self.x
        self.falling = False
        self.boost = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.name = name

class block:
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

xbox = character(100, 300, 60, 50, "xbox")
hatsune = character(1000, 300, 60, 60, "hatsune")

block_one = block(400, 630, 50, 100)

# set game window stats
game_display = pygame.display.set_mode((window_width, window_height), pygame.FULLSCREEN)
pygame.display.set_caption('PCSoc is best soc')
clock = pygame.time.Clock()

xbox.sprite = pygame.image.load('images/Xbox-360-Console_direction.png')
xbox.sprite = pygame.transform.scale(xbox.sprite, (xbox.width, xbox.height))

hatsune.sprite = pygame.image.load('images/hatsune_left.png')
hatsune.sprite = pygame.transform.scale(hatsune.sprite, (hatsune.width, hatsune.height))

bg = pygame.image.load('images/background.PNG')

block_sprite = pygame.image.load('images/block.jpg')

boundary_right_rect = pygame.Rect(1250, 0, 30, 720)
boundary_left_rect = pygame.Rect(0, 0, 30, 720)
boundary_top_rect = pygame.Rect(0, 0, 1280, 30)
boundary_bottom_rect = pygame.Rect(30, 700, 1280, 720)

def check_boundary_collision(character):
    # boundary collisions
    if ((character.rect.colliderect(boundary_right_rect) and character.x_change > 0) or
    (character.rect.colliderect(boundary_left_rect) and character.x_change < 0)):
        character.x_change = 0

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
            char_one.y_change = 5
            char_two.y_change = 5

def check_block_collision(char, block):
    # check if top of character hits bottom of block
    if char.rect.colliderect(block.rect) and char.y - char.height / 2 in range(int(block.y), int(block.y + block.height / 2)):
        char.y_change = 15
        char.falling = True
    # check if bottom of character hits top of block
    elif char.rect.colliderect(block.rect) and char.y + char.height / 2 in range(int(block.y - block.height / 2), int(block.y)):
        if char.y_change > 0:
            char.y_change = 0
    # check if right side of character hits left side of block
    elif char.rect.colliderect(block.rect) and char.x + char.width / 2 in range(int(block.x - block.width / 2), int(block.x)):
        if char.x_change > 0:
            char.x_change = 0
    # check if the left side of the character hits the left side of the block
    elif char.rect.colliderect(block.rect) and char.x - char.width / 2 in range(int(block.x), int(block.x + block.width / 2)):
        if char.x_change < 0:
            char.x_change = 0


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
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_a:
                xbox.x_change = -5
            elif event.key == pygame.K_d:
                xbox.x_change = 5
            elif event.key == pygame.K_w:
                xbox.y_change = -12
            elif event.key == pygame.K_s:
                xbox.y_change = 15
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
                hatsune.x_change = -5
            elif event.key == pygame.K_RIGHT:
                hatsune.x_change = 5
            elif event.key == pygame.K_UP:
                hatsune.y_change = -12
            elif event.key == pygame.K_DOWN:
                hatsune.y_change = 15
                hatsune.falling = True

        # key releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                xbox.x_change = 0
            if event.key == pygame.K_s or event.key == pygame.K_w:
                xbox.y_change = 5
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
               hatsune.x_change = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
               hatsune.y_change = 5

    if xbox.falling:
        if xbox.rect.colliderect(boundary_bottom_rect):
            xbox.y_change = 5
            xbox.falling = False
        else:
            xbox.y_change = 15

    if xbox.boost:
        if xbox.direction > 0:
            if xbox.x < xbox.old_x + 90:
                xbox.x_change = 15
            else:
                xbox.x_change = 5
                xbox.boost = False
                xbox.boost_counter = 0
        else:
            if xbox.x > xbox.old_x - 90:
                xbox.x_change = -15
            else:
                xbox.x_change = -5
                xbox.boost = False
                xbox.boost_counter = 0

    if hatsune.falling:
        if hatsune.rect.colliderect(boundary_bottom_rect):
            hatsune.y_change = 5
            hatsune.falling = False
        else:
            hatsune.y_change = 15
            
    if hatsune.boost:
        if hatsune.direction > 0:
            if hatsune.x < hatsune.old_x + 90:
                hatsune.x_change = 15
            else:
                hatsune.x_change = 5
                hatsune.boost = False
                hatsune.boost_counter = 0
        else:
            if hatsune.x > hatsune.old_x - 90:
                hatsune.x_change = -15
            else:
                hatsune.x_change = -5
                hatsune.boost = False
                hatsune.boost_counter = 0

    # make sure the character isn't stuck in the air
    if (xbox.y_change == 0):
        if not xbox.rect.colliderect(block_one.rect):
            xbox.y_change = 5

    # boundary collisions
    check_boundary_collision(xbox)
    check_boundary_collision(hatsune)

    check_block_collision(xbox, block_one)

    # character collisions
    check_character_collision(xbox, hatsune)
    check_character_collision(hatsune, xbox)


    xbox.rect.move_ip(xbox.x_change, xbox.y_change)
    hatsune.rect.move_ip(hatsune.x_change, hatsune.y_change)
    xbox.x += xbox.x_change
    xbox.y += xbox.y_change
    hatsune.x += hatsune.x_change
    hatsune.y += hatsune.y_change

    game_display.blit(bg, (0, 0))
  
    game_display.blit(block_sprite, block_one.rect)
    game_display.blit(xbox.sprite, xbox.rect)
    game_display.blit(hatsune.sprite, hatsune.rect)
    pygame.display.update() 
    clock.tick(60) # 60 FPS

while True:
    level_one()
