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

    motion_start_time = None

    while True:
        if GPIO.input(PIR_PIN):
            if motion_start_time is None:
                motion_start_time = time.time()
            else:
                if time.time() - motion_start_time >= 2:
                    print("Motion Detected!")
        else:
            motion_start_time = None
        
        time.sleep(0.1)  # Delay to reduce CPU usage

except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()
