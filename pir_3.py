import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BOARD)

# Set the pin number
PIR_PIN = 11

# Setup the PIR pin as input
GPIO.setup(PIR_PIN, GPIO.IN)

def detect_motion():
    motion_detected = False
    motion_start_time = None

    while True:
        if GPIO.input(PIR_PIN):
            if not motion_detected:
                motion_start_time = time.time()
                motion_detected = True
            elif time.time() - motion_start_time >= 2:
                print("Motion Detected!")
                motion_detected = False
        else:
            motion_detected = False
        
        time.sleep(0.1)  # Delay to reduce CPU usage

try:
    print("PIR Module Test (CTRL+C to exit)")
    time.sleep(2)  # Allow sensor to settle
    print("Ready")

    detect_motion()

except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()
