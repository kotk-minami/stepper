import RPi.GPIO as GPIO
import board
import neopixel
from time import sleep

GPIO.setmode(GPIO.BCM)

left_motor = 10
right_motor = 11

left_switch = 5
right_switch = 6

#Output
GPIO.setup(left_motor, GPIO.OUT)
GPIO.setup(right_motor, GPIO.OUT)

#Input
GPIO.setup(left_switch, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(right_switch, GPIO.IN, pull_up_down = GPIO.PUD_UP)

led_count = 14
total_led = neopixel.NeoPixel(board.D18, led_count)

off_light = [(0, 0, 0)] * led_count/2
turn_light = [(0, 100, 0)] * led_count/2
usual_light = [(0, 0, 100)] * led_count/2

current_state = 0
last_state = 0
large_counter = 0

vibe_time = 300
total_vibe = 400

while True:
    try:
        if GPIO.input(left_switch) == GPIO.LOW:
            current_state = 1
        elif GPIO.input(right_switch) == GPIO.LOW:
            current_state = 2
        else:
            current_state = 0

        if current_state != last_state:
            large_counter = 0
        
        if current_state == 1:
            #left_turn
            if large_counter <= vibe_time:
                GPIO.output(left_motor, GPIO.HIGH)
                GPIO.output(right_motor, GPIO.LOW)

                total_led[0:led_count/2] = turn_light #left_hundle
                total_led[led_count/2:led_count] = off_light #right_hundle
            else:
                GPIO.output(left_motor, GPIO.LOW)
                GPIO.output(right_motor, GPIO.LOW)

                total_led[0:led_count/2] = off_light #left_hundle
                total_led[led_count/2:led_count] = off_light #right_hundle
        elif current_state == 2:
            #right_turn
            if large_counter <= vibe_time:
                GPIO.output(left_motor, GPIO.LOW)
                GPIO.output(right_motor, GPIO.HIGH)
            else:
                GPIO.output(left_motor, GPIO.LOW)
                GPIO.output(right_motor, GPIO.LOW)
        else:
            GPIO.output(left_motor, GPIO.LOW)
            GPIO.output(right_motor, GPIO.LOW)

        sleep(0.001)
        large_counter += 1
        if large_counter > total_vibe:
            large_counter = 0

        last_state = current_state
        
    except KeyboardInterrupt:
        GPIO.output(left_motor, GPIO.LOW)
        GPIO.output(right_motor, GPIO.LOW)
        GPIO.cleanup()

        total_led.fill((0, 0, 0))
        sleep(0.001)