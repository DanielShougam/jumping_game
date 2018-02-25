import pygame
import sys

pygame.init()

game_display = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

rect = pygame.Rect(100, 100, 50, 60)
pcsoc_sprite = pygame.image.load('images/pcsoc_logo.png')
pcsoc_sprite = pygame.transform.scale(pcsoc_sprite, (50, 60))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    game_display.fill((169, 169, 169))
    game_display.blit(pcsoc_sprite, rect)

    pygame.display.update()
    clock.tick(60)
