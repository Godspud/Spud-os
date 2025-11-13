import pygame
from pygame.locals import *
import os

#TODO: copy paste
#TODO: selecting (highlighting)
#TODO: cursor
#TODO: find largest yvalue for chars for better font display

pygame.init()
display_info=pygame.display.Info()
output_screen=pygame.display.set_mode((display_info.current_w,display_info.current_h))
clock=pygame.time.Clock()
running=True

# functions
def print_to_screen(text,colour,background,location,scroll_y,affected_by_scroll=None,background_overide=None):
    if background_overide == False:
        pass
    else:
        output_screen.fill(background)
    lines = text.split("\n")
    base_x, base_y = location
    
    for row, line in enumerate(lines):
        y = base_y + row * font.get_linesize()
        if not affected_by_scroll:
            y -= scroll_y
        output_screen.blit(font.render(line,True,colour,background),(base_x,int(y)))

def text_add(text_to_add,text,cursor_pos,change_cursor_pos=None):
    text+=text_to_add
    if change_cursor_pos != False:
        width,height=font.size(text_to_add)
        cursor_pos=(cursor_pos[0]+width,cursor_pos[1])
    else:
        return text,cursor_pos
    return text,cursor_pos

def screen_input(prompt_text=None):
    output_screen.fill((0,0,0))
    text=""
    cursor_pos=(32,0)

    # Determine how many lines the prompt has
    prompt_lines=0
    if prompt_text:
        prompt_lines=prompt_text.count("\n")+1

    pygame.display.flip()

    entering=True
    while entering:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running=False
                return running

            elif event.type == pygame.KEYDOWN:
                # Backspace
                if event.key == pygame.K_BACKSPACE:
                    try:
                        cursor_pos=(cursor_pos[0]-font.size(text[-1])[0],cursor_pos[1])
                        text=text[:-1]
                    except IndexError:
                        pass

                # Enter: finish input
                elif event.key == pygame.K_RETURN:
                    entering=False
                    break

                # Normal keys (symbols,punctuation,space)
                elif pygame.K_SPACE <= event.key <= pygame.K_BACKQUOTE:
                    key=pygame.key.name(event.key)
                    char=chr(event.key)

                    if (event.mod & pygame.KMOD_SHIFT) or (event.mod & pygame.KMOD_CAPS):
                        for counter in range(len(normal_keys)):
                            if key == normal_keys[counter]:
                                char=shift_keys[counter]
                    text,cursor_pos=text_add(char,text,cursor_pos)

                # Letter keys
                elif pygame.K_a <= event.key <= pygame.K_z:
                    char=chr(event.key)
                    if (event.mod & pygame.KMOD_SHIFT) or (event.mod & pygame.KMOD_CAPS):
                        char=char.upper()
                    text,cursor_pos=text_add(char,text,cursor_pos)

        # Draw prompt text (may have multiple lines)
        if prompt_text:
            print_to_screen(prompt_text,colour,background,(0,0),0,False)

        # Draw input text *below* the prompt
        print_to_screen(text,colour,background,(0,prompt_lines*char_y),0,False,False)

        pygame.display.flip()
        clock.tick(30)

    return text

def wait_for_inpu(inpu_type):
    waiting_for_inpu=True
    while waiting_for_inpu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type in inpu_type:
                waiting_for_inpu=False

# assets
#font will be in the main settings loop as it is supposed to be interchangable
font_path=os.path.join("C:/Users/User/Downloads/coding/spud_os","Fonts/OpenDyslexicMono-Regular.otf")
font=pygame.font.Font(font_path,48)



# values (only on start up can be changed later)
background=(0,0,0) #can be changed later
colour=(255,255,255) #can be changed later
text=""
print(font.size('~'))
cursor_pos=(0,0)
normal_keys=["`","1","2","3","4","5","6","7","8","9","0","-","=","[","]","\\",";","'",",",".","/"," "]
shift_keys=["~","!","@","#","$","%","^","&","*","(",")","_","+","{","}","|",":","\"","<",">","?"," "]
scroll_y=0 #default
scroll_y_dampaning=10 #can be changed by user
Settings='Choese a setting to change:\n1: scroll dampaning \n2: Font selection \n3: font size \n4: background colour \n5: the text colour'
show_settings=False
Intro=['welcome to a very minimal text editor type \nto get started or press \nCtrl+s \nto access the settings(incomplete)',True]
current_file_path=''
largest_char_y=0
for counter in range(33,127):
    if font.size(chr(counter))[1] > largest_char_y:
        largest_char_y=font.size(chr(counter))[1]
char_y=largest_char_y

#files
BASE_FOLDER=os.path.join(os.getcwd(),"Spud_text_editor")
if not os.path.exists(BASE_FOLDER):
    os.mkdir(BASE_FOLDER)
    print('a folder has been created')

# startup
print('Assets and values initialised')


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

        elif event.type == pygame.KEYDOWN:
            if Intro[1]:
                Intro[1]=False
            
            #quit using ctrl+w
            if event.key == pygame.K_w and (event.mod & pygame.KMOD_CTRL):
                running=False

            #setting using ctrl+s
            elif event.key == pygame.K_s and (event.mod & pygame.KMOD_CTRL):
                inpu=screen_input(Settings)
                if inpu == '1':
                    scroll_y_dampaning=screen_input('Input a new value for your scroll dampaning')
                    scroll_y_dampaning=int(scroll_y_dampaning)
                elif inpu == '2':
                    largest_char_y=0
                    for counter in range(33,127):
                        if font.size(chr(counter))[1] > largest_char_y:
                             largest_char_y=font.size(chr(counter))[1]
                    char_y=largest_char_y
                    list_of_files=os.listdir('C:/Users/User/Downloads/coding/spud_os/Fonts')
                    list_of_files_2=[]
                    for counter in range(len(list_of_files)):
                        list_of_files_2.append((str(counter+1)+'. '+list_of_files[counter]))
                    inpu=screen_input('\n'.join(list_of_files_2))
                    try:
                        font_path=os.path.join('C:/Users/User/Downloads/coding/spud_os/Fonts',list_of_files[int(inpu)-1])
                        font=pygame.font.Font(font_path,48)
                    except (FileNotFoundError,FileExistsError,IndexError):
                        print_to_screen('Invalid file',(255,0,0),background,(0,0),0,False)
                        pygame.display.flip()
                        wait_for_inpu([pygame.KEYDOWN,pygame.MOUSEBUTTONDOWN])
                elif inpu == '3':
                    inpu=screen_input('input a new font size')
                    if int(inpu) > 0:
                        font=pygame.font.Font(font_path,int(inpu))
                    else:
                        print_to_screen('Invalid font size',(255,0,0),background,(0,0),0,False)
                        pygame.display.flip()
                        wait_for_inpu([pygame.MOUSEBUTTONDOWN,pygame.KEYDOWN])
                elif inpu == '4':
                    try:
                        background_=screen_input('Input 3 values from 0 to 255 in the\n RGB colour fromat')
                        if '-' in background_:
                            raise ValueError
                        else:
                            background_=background_.split(' ')
                            background=(int(background_[0]),int(background_[1]),int(background_[2]))
                    except (IndexError,ValueError):
                        print_to_screen('Invalid input',(255,0,0),background,(0,0),0,False)
                        pygame.display.flip()
                        wait_for_inpu([pygame.MOUSEBUTTONDOWN,pygame.KEYDOWN])
                elif inpu == '5':
                    try:
                        colour_=screen_input('Input 3 values from 0 to 255 in the\n RGB colour fromat')
                        if '-' in colour_:
                            raise ValueError
                        else:
                            colour_=colour_.split(' ')
                            colour=(int(colour_[0]),int(colour_[1]),int(colour_[2]))
                    except (IndexError,ValueError):
                        print_to_screen('Invalid input',(255,0,0),background,(0,0),0,False)
                        pygame.display.flip()
                        wait_for_inpu([pygame.MOUSEBUTTONDOWN,pygame.KEYDOWN])


                continue

            #Saving and loading files using ctrl+l
            elif event.key == pygame.K_l and (event.mod & pygame.KMOD_CTRL):
                inpu=screen_input('Would you like to \n1. open and load a file \n2. save a file?')
                if inpu == '1':
                    list_of_files=os.listdir(BASE_FOLDER)
                    list_of_files_2=[]
                    for counter in range(len(list_of_files)):
                        list_of_files_2.append((str(counter+1)+'. '+list_of_files[counter]))
                    inpu=screen_input('\n'.join(list_of_files_2))
                    cursor_pos=(0,0)
                    try:
                        list_of_files[(int(inpu)-1)]
                        current_file_path=os.path.join(BASE_FOLDER,list_of_files[(int(inpu)-1)])
                        with open(current_file_path,'r',encoding='utf-8') as current_file:
                            text=current_file.read()

                    except(IndexError,ValueError):
                        print_to_screen('Invalid file selected',(255,0,0),background,(0,0),scroll_y)
                        pygame.display.flip()
                        wait_for_inpu([pygame.KEYDOWN,pygame.MOUSEBUTTONDOWN])
                elif inpu == '2':
                    inpu=screen_input('would you like to \n1. save to the current file \n2. save to a file')
                    if inpu == '1':
                        try:
                            with open(current_file_path,'w',encoding='utf-8') as file:
                                file.write(text)
                            print_to_screen('File saved successfully',(0,255,0),background,(0,0),scroll_y)
                            pygame.display.flip()
                            wait_for_inpu([pygame.KEYDOWN,pygame.MOUSEBUTTONDOWN])
                        except (NameError,FileNotFoundError):
                            print_to_screen('No file currently loaded',(255,0,0),background,(0,0),scroll_y)
                            pygame.display.flip()
                            wait_for_inpu([pygame.KEYDOWN,pygame.MOUSEBUTTONDOWN])

                    elif inpu == '2':
                        new_file_name=screen_input('Enter new file name:')
                        new_file_path=os.path.join(BASE_FOLDER,new_file_name+'.txt')
                        if os.path.exists(new_file_path):
                            inpu=screen_input('File with that name already exists \nDo you want to override it [Y/n]')
                            pygame.display.flip()
                            if inpu.upper() == 'Y':        
                                with open(new_file_path,'w',encoding='utf-8') as file:
                                    file.write(text)
                                current_file_path=new_file_path
                                print_to_screen('File saved as new file',(0,255,0),background,(0,0),scroll_y)
                                pygame.display.flip()
                                wait_for_inpu([pygame.KEYDOWN,pygame.MOUSEBUTTONDOWN])

                            # wait for click before continuing
                            wait_for_inpu([pygame.MOUSEBUTTONDOWN,pygame.KEYDOWN])
                            continue
                        with open(new_file_path,'w',encoding='utf-8') as file:
                            file.write(text)
                        current_file_path=new_file_path
                        print_to_screen('File saved as new file',(0,255,0),background,(0,0),scroll_y)
                        pygame.display.flip()
                        wait_for_inpu([pygame.KEYDOWN,pygame.MOUSEBUTTONDOWN])

            # Backspace
            elif event.key == pygame.K_BACKSPACE:
                try:
                    cursor_pos=(cursor_pos[0]-font.size(text[-1])[0],cursor_pos[1])
                    text=text[:-1]
                except IndexError:
                    pass

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
            if Intro[1]:
                Intro[1]=False

    # Draw
    print_to_screen(text,colour,background,(0,0),scroll_y,False,True)

    if show_settings:
        print_to_screen(Settings,(255,255,0),background,(50,50),scroll_y,False)
    if Intro[1]:
        print_to_screen(Intro[0],colour,background,(0,0),False)
    pygame.display.flip()
    clock.tick(30)

print('done')
