import RPi.GPIO as GPIO
import time

# Control Pins
IN1, IN2 = 17, 27 # Left Motor
IN3, IN4 = 22, 23 # Right Motor

# Enable Pins for Speed
ENA, ENB = 12, 13

# Global variables for PWM objects
pwm_a = None
pwm_b = None

def setup():
    global pwm_a, pwm_b
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Setup all pins as outputs
    for pin in [IN1, IN2, IN3, IN4, ENA, ENB]:
        GPIO.setup(pin, GPIO.OUT)
    
    # Initialize PWM at 100Hz frequency
    pwm_a = GPIO.PWM(ENA, 100)
    pwm_b = GPIO.PWM(ENB, 100)
    
    # Start at 0 speed (off)
    pwm_a.start(0)
    pwm_b.start(0)  

def forward(speed=100):
    GPIO.output(IN1, GPIO.HIGH); GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH); GPIO.output(IN4, GPIO.LOW)
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(speed)

def backward(speed=100):
    GPIO.output(IN1, GPIO.LOW); GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW); GPIO.output(IN4, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(speed)

def stop():
    GPIO.output(IN1, GPIO.LOW); GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW); GPIO.output(IN4, GPIO.LOW)
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)

def spin_left(speed=60):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(speed)

def spin_right(speed=60):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)  
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH) 
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(speed)

def cleanup():
    global pwm_a, pwm_b
    stop()
    if pwm_a is not None:
        pwm_a.stop()
    if pwm_b is not None:
        pwm_b.stop()
    GPIO.cleanup()