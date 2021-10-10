#Science Fair Project 2021-2022
#Jeanelle Dao
#9 October 2021
#ONLY RUNNABLE ON WINDOWS PYTHON (3.9)

"""

Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/
 
Show everything we can pull off the joystick
"""
import pygame
 
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
                    dead_button_list[i] = 0
                    print("DEAD BUTTONS: ", dead_button_list)
    
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
 
        textPrint.print(screen, "Joystick {}".format(i))
        textPrint.indent()
 
        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        textPrint.print(screen, "Joystick name: {}".format(name))
 
        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        textPrint.print(screen, "Number of axes: {}".format(axes))
        textPrint.indent()
 
        for i in range(axes):
            axis = joystick.get_axis(i)
            textPrint.print(screen, "Axis {} value: {:>6.3f}".format(i, axis))
        textPrint.unindent()
 
        buttons = joystick.get_numbuttons()
        textPrint.print(screen, "Number of buttons: {}".format(buttons))
        textPrint.indent()
 
        for i in range(buttons):
            button = joystick.get_button(i)
            textPrint.print(screen, "Button {} value: {}".format(i, button))
        textPrint.unindent()
 
        # Hat switch. All or nothing for direction, not like joysticks.
        # Value comes back in an array.
        hats = joystick.get_numhats()
        textPrint.print(screen, "Number of hats: {}".format(hats))
        textPrint.indent()
 
        for i in range(hats):
            hat = joystick.get_hat(i)
            textPrint.print(screen, "Hat {} value: {}".format(i, str(hat)))
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
pygame.quit()
