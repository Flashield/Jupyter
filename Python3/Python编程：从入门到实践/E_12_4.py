import pygame

pygame.init()
screen = pygame.display.set_mode((500,500))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            print(event.key)