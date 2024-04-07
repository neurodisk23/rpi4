import RPi.GPIO as GPIO
import time

# Set up GPIO using Board numbering
GPIO.setmode(GPIO.BOARD)

# Set the PIR sensor pin
PIR_PIN = 11
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setmode(GPIO.BOARD)
# Initialize variables
detection_threshold = 0
detection_start_time = 0

try:
    print("PIR sensor initialized. Waiting for detection...")

    while True:
        # Read the PIR sensor state
        pir_state = GPIO.input(PIR_PIN)
        print("\n PIR Status: ", pir_state)
        time.sleep(0.25)



except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()  # Clean up GPIO
