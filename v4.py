import os
import telepot
import time
from time import sleep
import cv2
from subprocess import call
import board
import adafruit_dht

# Initialize the webcam
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Initialize the DHT sensor
dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

def handle(msg):
    global chat_id
    global telegramText
  
    chat_id = msg['chat']['id']
    telegramText = msg['text']
  
    print('Message received from ' + str(chat_id))
  
    if telegramText == '/start':
        bot.sendMessage(chat_id, 'Security camera is activated.')#Put your welcome note here

    elif telegramText == '/video':
        send_video(chat_id)

    elif telegramText == '/temp':
        send_temperature_humidity(chat_id)

def send_video(chat_id):
    # Video recording code here...

def send_temperature_humidity(chat_id):
    try:
        # Read temperature and humidity from the sensor
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity

        # Send temperature and humidity data to Telegram
        message = "Temperature: {:.1f} F / {:.1f} C\nHumidity: {}%".format(
            temperature_f, temperature_c, humidity)
        bot.sendMessage(chat_id, message)

    except RuntimeError as error:
        # Handle sensor reading errors
        print(error)
        bot.sendMessage(chat_id, "Error: Failed to read temperature and humidity data.")
        return

# Telegram bot initialization and message loop...

