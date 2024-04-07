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
    global detection_threshold
    global detection_start_time

    chat_id = msg['chat']['id']
    telegramText = msg['text']

    print('Message received from ' + str(chat_id))

    pir_state = GPIO.input(PIR_PIN)

    if telegramText == '/start':
        bot.sendMessage(chat_id, 'Security camera is activated.')  # Put your welcome note here

    elif telegramText == '/video':
        send_video(chat_id)

    elif telegramText == '/temp':
        send_temperature_humidity(chat_id)

    elif telegramText == '/det':
        pir(chat_id)
        pir_state = GPIO.input(PIR_PIN)
        if pir_state:
            detection_threshold += 1
            if detection_threshold >= 2:  # Check if threshold reached
                detection_threshold = 0
                response = bot.sendMessage(chat_id, 'Activity recorded at ' + str(
                    datetime.datetime.now(pytz.timezone('Asia/Kolkata'))) + ". Do you want to get the video?")
                # We don't handle the response here, as telepot doesn't provide callback_query_handler method.
                # Instead, the response is handled by the user when they send '/video yes' or '/video no' in a separate message.

    elif '/video' in telegramText:  # Handling response to the video request
        if telegramText == '/video yes':
            send_video(chat_id)
        elif telegramText == '/video no':
            bot.sendMessage(chat_id, 'Video request declined.')

    elif '/det' in telegramText:  # Handling response to the motion detection notification
        if telegramText == '/det yes':
            send_video(chat_id)
        elif telegramText == '/det no':
            bot.sendMessage(chat_id, 'Motion detection notification declined.')


# Existing code continues below...





# Existing code continues below...
     
        
        
def pir(chat_id):
    try:
        pir_state = GPIO.input(PIR_PIN)
        print("\n PIR state:", pir_state)
        # Read temperature and humidity from the sensor
        if pir_state :
            message = "Someone is there"
            
        else :
            message = "No-one is there"
            
        bot.sendMessage(chat_id, message)

    except RuntimeError as error:
        # Handle sensor reading errors
        print(error)
        bot.sendMessage(chat_id, "Error: Failed to read PIR data.")
        return
    

def send_video(chat_id):
    # Generate filename
    filename = "./video_" + (time.strftime("%y%b%d_%H%M%S")) + ".avi"
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

    # Record video for 5 seconds
    start_time = time.time()
    while (time.time() - start_time) < 10:
        ret, frame = camera.read()
        if ret:
            out.write(frame)
        else:
            print("Error: Couldn't capture frame")
            break  # Break the loop if there's an error

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
            bot.sendMessage(chat_id, 'Here is the video you requested!')

            # Remove the video files
            os.remove(filename)
            os.remove(mp4_filename)
        else:
            bot.sendMessage(chat_id, 'Failed to encode the video.')
    else:
        bot.sendMessage(chat_id, 'Failed to capture the video.')
        
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

bot = telepot.Bot('7067453611:AAETJIQTgUATD9c9eZgn5sY68of2Adw1G0Q')
bot.message_loop(handle)        

while True:
    time.sleep(10)


