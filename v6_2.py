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

# Initialize the webcam
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

# Set the PIR sensor pin
PIR_PIN = 17

GPIO.setup(PIR_PIN, GPIO.IN)

# Initialize variables
detection_threshold = 0

def handle(msg):
    global chat_id
    global telegramText
    global detection_threshold

    chat_id = msg['chat']['id']
    telegramText = msg['text']

    print('Message received from ' + str(chat_id))

    if telegramText == '/start':
        bot.sendMessage(chat_id, 'Security camera is activated.')  # Put your welcome note here

    elif telegramText == '/video':
        send_video(chat_id)

    elif telegramText == '/temp':
        send_temperature_humidity(chat_id)


def pir(chat_id):
    global detection_threshold

    try:
        pir_state = GPIO.input(PIR_PIN)
        print("\n PIR state:", pir_state)
        
        # Read temperature and humidity from the sensor
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        
        if pir_state:
            message = "Motion detected!\nTemperature: {:.1f} F / {:.1f} C\nHumidity: {}%".format(
                temperature_f, temperature_c, humidity)
            bot.sendMessage(chat_id, message)
            
            # Generate filename
            filename = "./video_" + (time.strftime("%y%b%d_%H%M%S")) + ".avi"
            
            # Define the codec and create VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

            # Record video for 10 seconds
            start_time = time.time()
            while (time.time() - start_time) < 10:
                ret, frame = camera.read()
                if ret:
                    out.write(frame)
                else:
                    print("Error: Couldn't capture frame")
                    break

            # Release the video writer
            out.release()

            # Check if the video file exists
            if os.path.exists(filename):
                # Convert AVI to MP4
                mp4_filename = filename.replace(".avi", ".mp4")
                command = f"ffmpeg -i {filename} -codec copy {mp4_filename}"
                call(command, shell=True)

                # Check if the MP4 file exists
                if os.path.exists(mp4_filename):
                    # Send the video
                    bot.sendVideo(chat_id, video=open(mp4_filename, 'rb'))
                    bot.sendMessage(chat_id, 'Here is the video of the detected motion!')

                    # Remove the video files
                    os.remove(filename)
                    os.remove(mp4_filename)
                else:
                    bot.sendMessage(chat_id, 'Failed to encode the video.')
            else:
                bot.sendMessage(chat_id, 'Failed to capture the video.')

        else:
            bot.sendMessage(chat_id, "No motion detected.")

    except RuntimeError as error:
        # Handle sensor reading errors
        print(error)
        bot.sendMessage(chat_id, "Error: Failed to read PIR data.")


def send_video(chat_id):
    # Function to send the recorded video
    pass


def send_temperature_humidity(chat_id):
    # Function to send temperature and humidity data
    pass


bot = telepot.Bot('YOUR_BOT_TOKEN')
bot.message_loop(handle)

while True:
    pir(-123456789)  # Provide a dummy chat ID as it's not relevant here
    time.sleep(10)
