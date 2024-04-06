import os
import telepot
import time
import cv2
from subprocess import call
import board
import adafruit_dht
import RPi.GPIO as GPIO  # Import the GPIO library

# Initialize the webcam
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

# Set up GPIO pin
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
PIN_11 = 11
GPIO.setup(PIN_11, GPIO.IN)

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

def check_pin_11():
    while True:
        if GPIO.input(PIN_11):  # If pin 11 is high
            bot.sendMessage(chat_id, "Pin 11 is high!")  # Send message to Telegram
            time.sleep(5)  # Wait for 5 seconds before checking again
        else:
            time.sleep(1)  # If pin 11 is not high, wait for 1 second before checking again

bot = telepot.Bot('your bot token here')
bot.message_loop(handle)

# Start a separate thread to continuously monitor pin 11
GPIO_thread = threading.Thread(target=check_pin_11)
GPIO_thread.daemon = True
GPIO_thread.start()

while True:
    time.sleep(10)
