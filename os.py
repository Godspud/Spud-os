import pygame
from pygame.locals import *

#TODO: add scroll for when the text goes off screen (down)
#TODO: copy paste
#TODO: selecting (highlighting)

pygame.init()
display_info=pygame.display.Info()
output_screen=pygame.display.set_mode((display_info.current_w,display_info.current_h))
clock=pygame.time.Clock()
running=True

# functions
def print_to_screen(text,colour,background,location,scroll_y,affected_by_scroll=None):
    lines=text.split("\n")
    for counter in range(len(lines)):
        for counter_1 in range(len(lines[counter])):
            if affected_by_scroll == False:
                output_screen.blit(font.render(lines[counter][counter_1],True,colour,background),(counter_1*char_y,counter*char_x))
            else:
                output_screen.blit(font.render(lines[counter][counter_1],True,colour,background),(counter_1*char_y,counter*char_x-scroll_y))

def text_add(text_to_add,text,cursor_pos,change_cursor_pos=None):
    text+=text_to_add
    if change_cursor_pos != False:
        cursor_pos=(cursor_pos[0]+char_y,cursor_pos[1])
    else:
        return text,cursor_pos
    return text,cursor_pos

def change_setting(setting_to_be_changed,changed_value,how_to_be_changed=None):
    if how_to_be_changed == '+':
        setting_to_be_changed+=changed_value
    elif how_to_be_changed == '-':
        setting_to_be_changed-=changed_value
    else:
        setting_to_be_changed=changed_value
    return setting_to_be_changed

def screen_input(text_to_be_displayed):
    print_to_screen(text_to_be_displayed)


# assets
font=pygame.font.Font('OpenDyslexicMono-Regular.otf',48)

# values (only on start up can be changed later)
background=(0,0,0)
text=""
cursor_pos=(0,0)
char_y=32
char_x=61
normal_keys=["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0","-", "=", "[", "]", "\\", ";", "'", ",", ".", "/", " "]
shift_keys=["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")","_", "+", "{", "}", "|", ":", "\"", "<", ">", "?", " "]
scroll_y=0 #default
scroll_y_dampaning=10 #can be changed by user
Settings='Choese a setting to change:\n1: scroll dampaning'
show_settings=False
Intro=['welcome to a very minimal text editor type \nto get started or press \nCtrl + s \nto access the settings(incomplete)',True]

# startup
print('Assets and values initialised')


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

        elif event.type == pygame.KEYDOWN:
            if show_settings:
                show_settings=False
            if Intro[1]:
                Intro[1]=False
            
            #setting using ctrl + s
            if event.key == pygame.K_s and (event.mod & pygame.KMOD_CTRL):
                show_settings = True
                continue

            # Backspace
            elif event.key == pygame.K_BACKSPACE:
                cursor_pos=(cursor_pos[0]-char_y,cursor_pos[1])
                text=text[:-1]

            # Enter
            elif event.key == pygame.K_RETURN:
                text,cursor_pos=text_add('\n',text,cursor_pos,False)

            # Tab
            elif event.key == pygame.K_TAB:
                text,cursor_pos=text_add("    ",text,cursor_pos)

            # Letters from (https://www.pygame.org/docs/ref/key.html?highlight=key#module-pygame.key)
            #First half for all non letter keys (char.upper dosent work to get the caps version)
            elif pygame.K_SPACE <= event.key <= pygame.K_BACKQUOTE:
                key=pygame.key.name(event.key)

                char=chr(event.key)

                # shift
                if (event.mod & pygame.KMOD_SHIFT) or (event.mod & pygame.KMOD_CAPS):
                    for counter in range(len(normal_keys)):
                        if key == normal_keys[counter]:
                            char=shift_keys[counter]
                
                text,cursor_pos=text_add(char,text,cursor_pos)

            #Second half
            elif pygame.K_a <= event.key <= pygame.K_z:
                char=chr(event.key)
                if (event.mod & pygame.KMOD_SHIFT) or (event.mod & pygame.KMOD_CAPS):
                    char=char.upper()
                text,cursor_pos=text_add(char,text,cursor_pos)

        elif event.type == MOUSEWHEEL:
            scroll_y+=event.y*scroll_y_dampaning

        elif event.type == MOUSEBUTTONDOWN:
            # Hide settings on any click
            if show_settings:
                show_settings = False
            if Intro[1]:
                Intro[1]=False

    # Draw
    output_screen.fill(background)
    print_to_screen(text,(255,255,255),background,(0,0),scroll_y)

    if show_settings:
        print_to_screen(Settings,(255,255,0),background,(50,50),scroll_y,False)
    if Intro[1]:
        print_to_screen(Intro[0],(255,255,255),background,(0,0),False)
    pygame.display.flip()
    clock.tick(30)

print('done')
