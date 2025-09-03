import pygame
from random import randint as randomint
pygame.init()
display_info=pygame.display.Info()
output_screen=pygame.display.set_mode((display_info.current_w,display_info.current_h))
clock=pygame.time.Clock()
running=True

def pixel_colour(x,y,colour):
    output_screen.set_at((x,y),colour)
def show_lower_w(a,y,colour):
    for counter in range(64):
        for counter_1 in range(64):
            pixel_colour(counter,counter_1,'black')


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                output_screen.fill('green')
                show_lower_w(0,0,'black')
                pygame.display.flip()
            elif event.key == pygame.K_a:
                output_screen.blit(img_A,(0,0))
                pygame.display.flip()
    output_screen.fill('red')
    output_screen.fill('yellow')
    clock.tick(1)
    pygame.display.flip()
print('done')

