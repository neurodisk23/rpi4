import RPi.GPIO as GPIO
import time

# Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Set the PIR sensor pin
PIR_PIN = 11
GPIO.setup(PIR_PIN, GPIO.IN)

# Initialize variables
detection_threshold = 0
detection_start_time = 0

try:
    print("PIR sensor initialized. Waiting for detection...")

    while True:
        # Read the PIR sensor state
        pir_state = GPIO.input(PIR_PIN)

        if pir_state == GPIO.HIGH:
            detection_threshold += 1
            if detection_threshold == 1:
                detection_start_time = time.time()  # Start time of continuous detection

            if detection_threshold >= 3:
                print("Detected!")
                detection_threshold = 0  # Reset threshold after detection
        else:
            detection_threshold = 0  # Reset threshold if no detection

        # Check if continuous detection for 3 seconds
        if detection_start_time != 0 and time.time() - detection_start_time >= 3:
            print("Continuous detection for 3 seconds")
            detection_start_time = 0  # Reset start time after continuous detection

        time.sleep(1)  # Wait for 1 second

except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()  # Clean up GPIO

