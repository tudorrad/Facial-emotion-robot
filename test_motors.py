import motors
import time

print("--- STARTING HARDWARE TEST ---")
motors.setup() 

print("Moving Forward at 60% speed...")
motors.forward(speed=60)
time.sleep(2)

print("Stopping...")
motors.stop()
motors.cleanup()
print("--- TEST COMPLETE ---")