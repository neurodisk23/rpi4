import multiprocessing
import os
import telepot
import time
import cv2
from subprocess import call
import board
import adafruit_dht
import RPi.GPIO as GPIO
import datetime
import pytz

def run_bot():
    def handle(msg):
        global chat_id
        global telegramText

        chat_id = msg['chat']['id']
        telegramText = msg['text']

        print('Message received from ' + str(chat_id))

        pir_state = GPIO.input(PIR_PIN)

        if telegramText == '/start':
            bot.sendMessage(chat_id, 'Security camera is activated.')

        elif telegramText == '/video':
            send_video(chat_id)

        elif telegramText == '/temp':
            send_temperature_humidity(chat_id)

        elif telegramText == '/det':
            pir(chat_id)
            pir_state = GPIO.input(PIR_PIN)
            if pir_state:
                bot.sendMessage(chat_id, 'Activity recorded at ' + str(datetime.datetime.now(pytz.timezone('Asia/Kolkata'))) + " do you want a video")
                while True:
                    response = bot.getUpdates()
                    if response:
                        response_text = response[-1]['message']['text']
                        print("response text", response_text)
                        if response_text == '/yes':
                            send_video(chat_id)
                            break
                        elif response_text != '/yes':
                            break
                        time.sleep(1)

    def pir(chat_id):
        try:
            pir_state = GPIO.input(PIR_PIN)
            print("\n PIR state:", pir_state)
            if pir_state:
                message = "Someone is there"
            else:
                message = "No-one is there"

            bot.sendMessage(chat_id, message)

        except RuntimeError as error:
            print(error)
            bot.sendMessage(chat_id, "Error: Failed to read PIR data.")
            return

    def send_video(chat_id):
        filename = "./video_" + (time.strftime("%y%b%d_%H%M%S")) + ".avi"
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

        start_time = time.time()
        while (time.time() - start_time) < 10:
            ret, frame = camera.read()
            if ret:
                out.write(frame)
            else:
                print("Error: Couldn't capture frame")
                break

        out.release()

        if os.path.exists(filename):
            mp4_filename = filename.replace(".avi", ".mp4")
            command = f"ffmpeg -i {filename} -codec copy {mp4_filename}"
            call(command, shell=True)

            if os.path.exists(mp4_filename):
                bot.sendVideo(chat_id, video=open(mp4_filename, 'rb'))
                bot.sendMessage(chat_id, 'Here is the video you requested!')

                os.remove(filename)
                os.remove(mp4_filename)
            else:
                bot.sendMessage(chat_id, 'Failed to encode the video.')
        else:
            bot.sendMessage(chat_id, 'Failed to capture the video.')

    def send_temperature_humidity(chat_id):
        try:
            temperature_c = dhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = dhtDevice.humidity

            message = "Temperature: {:.1f} F / {:.1f} C\nHumidity: {}%".format(
                temperature_f, temperature_c, humidity)
            bot.sendMessage(chat_id, message)

        except RuntimeError as error:
            print(error)
            bot.sendMessage(chat_id, "Error: Failed to read temperature and humidity data.")
            return

    bot = telepot.Bot('7067453611:AAETJIQTgUATD9c9eZgn5sY68of2Adw1G0Q')
    bot.message_loop(handle)

    while True:
        time.sleep(10)

if __name__ == '__main__':
    # Set up GPIO and camera
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)
    PIR_PIN = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIR_PIN, GPIO.IN)

    # Number of instances you want to run
    num_instances = 2

    # Create a list to hold the processes
    processes = []

    # Create and start the processes
    for _ in range(num_instances):
        process = multiprocessing.Process(target=run_bot)
        process.start()
        processes.append(process)

    # Wait for all processes to finish
    for process in processes:
        process.join()
