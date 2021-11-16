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
passwordStr = text_file.read()
 
#close file
text_file.close()

passwordList = passwordStr.split(", ")

#--------------#

        if abs(float(passwordList[i]) - passwordEnterList[i]) <= 0.5: #changes error margin
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
