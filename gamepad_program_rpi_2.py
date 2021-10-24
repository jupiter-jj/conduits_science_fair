#Science Fair Project 2021-2022
#Jeanelle Dao
#9 October 2021
#ONLY RUNNABLE ON WINDOWS PYTHON (3.9)

import pygame
import RPi.GPIO as GPIO
import time
#set GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
 
class TextPrint(object):
    """
    This is a simple class that will help us print to the screen
    It has nothing to do with the joysticks, just outputting the
    information.
    """
    def __init__(self):
        """ Constructor """
        self.reset()
        self.x_pos = 10
        self.y_pos = 10
        self.font = pygame.font.Font(None, 20)
 
    def print(self, my_screen, text_string):
        """ Draw text onto the screen. """
        text_bitmap = self.font.render(text_string, True, BLACK)
        my_screen.blit(text_bitmap, [self.x_pos, self.y_pos])
        self.y_pos += self.line_height
 
    def reset(self):
        """ Reset text to the top of the screen. """
        self.x_pos = 10
        self.y_pos = 10
        self.line_height = 15
 
    def indent(self):
        """ Indent the next line of text """
        self.x_pos += 10
 
    def unindent(self):
        """ Unindent the next line of text """
        self.x_pos -= 10
 
 
pygame.init()
 
# Set the width and height of the screen [width,height]
size = [500, 700]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Initialize the joysticks
pygame.joystick.init()
 
# Get ready to print
textPrint = TextPrint()


button_down = False
passwordEnterList = [10]
password = "023167"
passwordList = []

for digit in password:
  passwordList.append(int(digit))

dead_button_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
lock_timer_start = False
lock_clock_time = time.time()

# -------- Main Program Loop -----------
while not done:
    # EVENT PROCESSING STEP
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
        # Possible joystick actions: JOYAXISMOTION JOYB0ALLMOTION JOYBUTTONDOWN
        # JOYBUTTONUP JOYHATMOTION
        button_press_list = []
        button_press_value = 10


        #debugging
        if event.type == pygame.JOYBUTTONUP:
            for i in range(buttons):
                button = joystick.get_button(i)
                if button == 0:
                    dead_button_list[i]= 0
                    print("DEAD BUTTONS: ", dead_button_list)
            if lock_timer_start:
                if time.time() - lock_clock_time >= 1: #change number here to change lock delay
                    print(time.time() - lock_clock_time)
                    GPIO.output(21, True)
                    time.sleep(1)
                    GPIO.output(21, False)
                else:
                    print(time.time() - lock_clock_time)
                lock_timer_start = False
                    
                    
    
        #run is button is pressed
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
            for i in range(buttons):
                button = joystick.get_button(i)
                print("button: ", button)
                print("enter list: ", passwordEnterList[-1])
                print("dead buttons: ", dead_button_list[i])
                if dead_button_list[i] == 1: #if button was previously pressed
                    button_press_list.append(0) #ignore
                else:
                    button_press_list.append(button) #otherwise append button (0/1)
                
            #determine button press value
            print(button_press_list)
            button_press_value_str = ""
            for value in button_press_list:
                button_press_value_str += str(value)
            button_press_value = button_press_value_str.find("1") #first occuring "1"
            print(button_press_value)
            if button_press_value == 8 or button_press_value == 9:
                lock_timer_start = True
                lock_clock_time = time.time()
                

            else:
                if button_press_value != -1:
                    if len(passwordEnterList) <= 5:
                        #if there are not 6 digits in passwordEnterList
                        passwordEnterList.append(int(button_press_value))
                        print("\nPASSWORD ENTER LIST:", passwordEnterList)
                    else:
                        #if there are 6 digits, add new digit, remove earliest chosen digit
                        passwordEnterList.append(int(button_press_value))
                        passwordEnterList.pop(0)
                        print("\nPASSWORD ENTER LIST:", passwordEnterList)
                else:
                    print("\nothing added to password enter list")

                
                dead_button_list[button_press_value] = 1
                print(button_press_value)
                print(dead_button_list[button_press_value])
                print("DEAD BUTTONS: ", dead_button_list)

        #if password entered correctly --> open

        if passwordList == passwordEnterList:
            GPIO.output(20, True)
            time.sleep(1)
            GPIO.output(20, False)
            print("\n\nOPEN\n\n")
            passwordEnterList = [10]

#-------------------------------------------------------------------------------------------------------------------------#
 
    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()
 
    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()
 
    textPrint.print(screen, "Number of joysticks: {}".format(joystick_count))
    textPrint.indent()
 
    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
  
        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        textPrint.print(screen, "Joystick name: {}".format(name))

 
        buttons = joystick.get_numbuttons()
        textPrint.print(screen, "Number of buttons: {}".format(buttons))
        textPrint.indent()
 
        for i in range(buttons):
            button = joystick.get_button(i)
            textPrint.print(screen, "Button {} value: {}".format(i, button))
        textPrint.unindent()
 
        textPrint.unindent()
 
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
GPIO.output(21, False)
GPIO.output(20, False)
pygame.quit()