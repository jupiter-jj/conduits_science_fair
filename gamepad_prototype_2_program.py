#Science Fair Prototype v2 2021-2022
#Jeanelle Dao
#14 November 2021

import RPi.GPIO as GPIO
import time

#set GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
 
#set variables
passwordEnterList = []
unlockList = [False, False, False, False, False, False]

#--------------#

#open text file in read mode
text_file = open("password.txt", "r")
 
#read whole file to a string
passwordList = text_file.read()
 
#close file
text_file.close()

#--------------#

button = 3
last_button = 3

lock_timer_start = False
lock_clock_time = time.time()


#NOTE: FALSE MEANS BUTTON DOWN AND TRUE MEANS BUTTON UP
#TRUE/FALSE DEPENDS ON VOLTAGE

def GPIOBUTTONDETECT():
    global button
    global last_button
   
    if GPIO.input(26) == GPIO.HIGH:
        button = 1
       
    if GPIO.input(26) == GPIO.LOW:
        button = 0
       
    if button == 0 and last_button == 1:
        print("JOYBUTTONDOWN")
        last_button = button
        return ("down")
   
    if button == 1 and last_button == 0:
        print("JOYBUTTONUP\n")
        last_button = button
        return ("up")

    last_button = button
   
# -------- Main Program Loop -----------
while True:
   
    button_state = GPIOBUTTONDETECT()

    #debugging
    if button_state == "up":
        if lock_timer_start:
            button_press_value = time.time() - lock_clock_time
            print("\n----------------------\nTIME:",  button_press_value)
           
            if button_press_value >= 5:
                GPIO.output(21, True)
                time.sleep(1)
                GPIO.output(21, False)
                print("\n\nCLOSE\n\n")
                passwordEnterList = []
       
            elif len(passwordEnterList) <= 5: #lock time
                #if there are not 6 digits in passwordEnterList
                passwordEnterList.append(button_press_value)
                print("PASSWORD ENTER LIST:", passwordEnterList)
            else:
                #if there are 6 digits, add new digit, remove earliest chosen digit
                passwordEnterList.append(button_press_value)
                passwordEnterList.pop(0)
                print("PASSWORD ENTER LIST:", passwordEnterList)

            lock_timer_start = False
                   
    #run is button is pressed
    if button_state == "down":
        lock_timer_start = True
        lock_clock_time = time.time()

    #if password entered correctly --> open

    for i in range(len(passwordEnterList)):
        if abs(passwordList[i] - passwordEnterList[i]) <= 1: #changes error margin
            unlockList[i] = True

    if unlockList == [True, True, True, True, True, True]:
        GPIO.output(20, True)
        time.sleep(1)
        GPIO.output(20, False)
        print("\n\nOPEN\n\n")
        passwordEnterList = []
   


    #reset unlock list to be updated later
    unlockList = [False, False, False, False, False, False]
    time.sleep(0.1)
           

#-------------------------------------------------------------------#

GPIO.output(21, False)
GPIO.output(20, False)
pygame.quit()
