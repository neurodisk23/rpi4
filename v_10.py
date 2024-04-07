import telepot
import datetime
import pytz
import time
import telepot.namedtuple
import RPi.GPIO as GPIO
import os
import time
from time import sleep
import cv2
from subprocess import call
import board
import adafruit_dht

# The default pinmode is BCM

# Initialize the webcam
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)  # Set the mode

# Set the PIR sensor pin
PIR_PIN = 17

GPIO.setup(PIR_PIN, GPIO.IN)


class Bot:
    def __init__(self, token):
        self.bot = telepot.Bot(token)
        self.state = {}

    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type == 'text':
            text = msg['text']

            if text == '/det':
                self.pir(chat_id)
                pir_state = GPIO.input(PIR_PIN)
                if pir_state:
                    self.bot.sendMessage(chat_id, 'Activity recorded at ' + str(datetime.datetime.now(pytz.timezone('Asia/Kolkata'))) + " do you want a video")
                    while True:
                        response = self.bot.getUpdates()
                        if response:
                            response_text = response[-1]['message']['text']
                            print("response text", response_text)
                            if response_text == '/yes':
                                self.bot.sendMessage(chat_id, "Sending video")
                                break
                            elif response_text != '/yes':
                                break
                        time.sleep(1)

    def pir(self, chat_id):
        try:
            pir_state = GPIO.input(PIR_PIN)
            print("\n PIR state:", pir_state)
            # Read temperature and humidity from the sensor
            if pir_state:
                message = "Someone is there"
            else:
                message = "No-one is there"

            self.bot.sendMessage(chat_id, message)

        except RuntimeError as error:
            # Handle sensor reading errors
            print(error)
            self.bot.sendMessage(chat_id, "Error: Failed to read PIR data.")
            pass


TOKEN = '7067453611:AAETJIQTgUATD9c9eZgn5sY68of2Adw1G0Q'
bot = Bot(TOKEN)
bot.bot.message_loop(bot.handle)

print('Listening...')

# Keep the program running
while True:
    time.sleep(10)
