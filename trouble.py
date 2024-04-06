import os
import telepot
import time
from time import sleep
import cv2
from subprocess import call
import board
import adafruit_dht
import RPi.GPIO as GPIO
import datetime
import pytz
# The default pinmode is BCM

# Initialize the webcam
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)
# GPIO.setmode(GPIO.BOARD)

# Set the PIR sensor pin
PIR_PIN = 17

GPIO.setup(PIR_PIN, GPIO.IN)


# Initialize variables
detection_threshold = 0
detection_start_time = 0



def handle(msg):
    global chat_id
    global telegramText
  
    chat_id = msg['chat']['id']
    telegramText = msg['text']
  
    print('Message received from ' + str(chat_id))
    
    pir_state = GPIO.input(PIR_PIN)
  
    if telegramText == '/start':
        bot.sendMessage(chat_id, 'Security camera is activated.')#Put your welcome note here

    elif telegramText == '/video':
        send_video(chat_id)

    elif telegramText == '/temp':
        send_temperature_humidity(chat_id)
    
    elif telegramText == '/det':
        pir(chat_id)
        pir_state = GPIO.input(PIR_PIN)
        if pir_state :
            bot.sendMessage(chat_id, 'Activity recorded at '+ str(datetime.datetime.now(pytz.timezone('Asia/Kolkata')))+" do you want a video")
            if telegramText == '/yes':
                send_video(chat_id)
                
    elif pir_state :
        bot.sendMessage(chat_id, 'hello')
     
            
        
