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
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
            for i in range(buttons):
                button = joystick.get_button(i)
                button_press_list.append(button)
            print(button_press_list)
            button_press_value = button_press_list.index(1)
            print(button_press_value)
            if len(passwordEnterList) <= 5:
                if passwordEnterList[-1] != button_press_value:
                    passwordEnterList.append(int(button_press_value))
                    print(passwordEnterList)
            else:
                if passwordEnterList[-1] != button_press_value:
                    passwordEnterList.append(int(button_press_value))
                    passwordEnterList.pop(0)
                    print(passwordEnterList) 

        if passwordList == passwordEnterList:
            print("\n\nOPEN\n\n")
            passwordEnterList = [10]
            
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
 
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
