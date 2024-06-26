import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BOARD)

# Set the pin number
PIR_PIN = 11

# Setup the PIR pin as input
GPIO.setup(PIR_PIN, GPIO.IN)

try:
    print("PIR Module Test (CTRL+C to exit)")
    time.sleep(2)  # Allow sensor to settle
    print("Ready")

    while True:
        if GPIO.input(PIR_PIN):
            print("Motion Detected!")
        else:
            print("No motion")
        
        time.sleep(0.5)  # Delay to reduce CPU usage

except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()
