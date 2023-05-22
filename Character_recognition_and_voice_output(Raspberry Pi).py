import pytesseract
import cv2
import os
import time
from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO

camera = PiCamera()

button_pin = 15
sound_replay_pin = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sound_replay_pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

while 1:
       
        if GPIO.input(button_pin) == GPIO.HIGH:
                print("pushed")  
                sleep(0.2)
                camera.capture('/home/project/image/hangul.png')
                camera.stop_preview()
                pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
                result = open("/home/project/image/output.txt","w")
                path_dir = '/home/project/image'    
                file_list = os.listdir(path_dir)
               
                for file_name in file_list :
                        if file_name == "output.txt":
                                continue
               
                result.write(pytesseract.image_to_string('/home/project/image/hangul.png',lang="kor",config='--psm 4 -c preserve_interword_spaces=1')+'\n')
                result.close()
                print("check to output")
               
                def speak(option, msg) :
                        os.system("espeak {} '{}'".format(option,msg))
   
                option = '-s 130 -p 50 -a 200 -v ko+f7'
                msg = "-f/home/project/image/output.txt"
                msg2 = 'read txt file'
               
                print('espeak', option, msg2)
                speak(option,msg)
                time.sleep(0.1)
        if GPIO.input(sound_replay_pin) == GPIO.HIGH:
                print("sound replay")
                def speak(option, msg) :
                        os.system("espeak {} '{}'".format(option,msg))
   
                option = '-s 130 -p 50 -a 200 -v ko+f7'
                msg = "-f/home/project/image/output.txt"
                msg2 = 'read txt file'
               
                print('espeak', option, msg2)
                speak(option,msg)
                time.sleep(0.1)
               
GPIO.cleanup()
