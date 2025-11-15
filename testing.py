import pygame
from pygame.locals import *
import os

pygame.init()
output_screen=pygame.display.set_mode((1000,500))
clock=pygame.time.Clock()
running=True
font=pygame.font.Font('Fonts/OpenDyslexicMono-Regular.otf',48)
largest_char_y=0
for counter in range(33,127):
    if font.size(chr(counter))[1] > largest_char_y:
        largest_char_y=font.size(chr(counter))[1]
char_y=largest_char_y

def print_to_screen(text,colour,background,location,scroll_y,affected_by_scroll=None,background_overide=None):
    if background_overide == False:
        pass
    else:
        output_screen.fill(background)
    lines = text.split("\n")
    print(lines)
    base_x, base_y = location
    
    for row, line in enumerate(lines):
        y = base_y + row * font.get_linesize()
        if not affected_by_scroll:
            y -= scroll_y
        output_screen.blit(font.render(line,True,colour,background),(base_x,int(y)))

text='h\nb'
loc=0
while running:
    line=0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                loc+=1
            if event.key == pygame.K_LEFT:
                loc-=1
    for counter in range(loc):
        line+=font.size(text[counter])[0]
    print_to_screen(text,(255,255,255),(0,0,0),(0,0),0)
    pygame.draw.line(output_screen,(255,255,255),(line,(font.size(text[loc])[1])),(line+font.size(text[loc])[0],font.size(text[loc])[1]),10)
    pygame.display.flip()