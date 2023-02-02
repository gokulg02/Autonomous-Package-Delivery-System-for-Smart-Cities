import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
import time

# initializing the pin numbers where motors are connected
L_PWM_PIN1 = 38
L_PWM_PIN2 = 40
R_PWM_PIN2 = 32
R_PWM_PIN1 = 33
L_EN = 31
R_EN = 37
#encoder
enc_l = enc_r = 0
l = r = 0
#Encoder
l_enc = 24
r_enc = 26
motor_speed = 70
totalCount = 20
motor_offset = 30
circum = 230 #mm
distance = 400 #mm

#enc int
def l_int(channel):
    global enc_l,l
    enc_l += 1
    if enc_l%20 == 0:
        l += 1
    print("l:", enc_l)
    print("l_rev:", l)

def r_int(channel):
    global enc_r,r
    enc_r += 1
    if enc_r%20 == 0:
        r += 1
    print("r:", enc_r)
    print("r_rev:", r)
# declare motor pins as output pins
# motors get input from the PWM pins
def motor_pin_setup():
    global L_MOTOR1, L_MOTOR2, R_MOTOR1, R_MOTOR2
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(R_PWM_PIN1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(R_PWM_PIN2, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(L_PWM_PIN1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(L_PWM_PIN2, GPIO.OUT, initial=GPIO.LOW)

    # setting initial PWM frequency for all 4 pins
    L_MOTOR1 = GPIO.PWM(L_PWM_PIN1, 100) 
    R_MOTOR1 = GPIO.PWM(R_PWM_PIN1, 100)
    L_MOTOR2 = GPIO.PWM(L_PWM_PIN2, 100)
    R_MOTOR2 = GPIO.PWM(R_PWM_PIN2, 100) 
    GPIO.setup(L_EN, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(R_EN, GPIO.OUT, initial=GPIO.HIGH)
    #Encoder setup
    GPIO.setup(l_enc, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(r_enc, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(l_enc, GPIO.RISING, callback=l_int)
    GPIO.add_event_detect(r_enc, GPIO.RISING, callback=r_int)
    
    # setting initial speed (duty cycle) for each pin as 0
    L_MOTOR1.start(0)
    R_MOTOR1.start(0)
    L_MOTOR2.start(0)
    R_MOTOR2.start(0)
    
def forward(left, right):
    L_MOTOR1.ChangeDutyCycle(left)
    R_MOTOR1.ChangeDutyCycle(right)
    
def motor_stop():
    L_MOTOR1.stop()
    R_MOTOR1.stop()
    L_MOTOR2.stop()
    R_MOTOR2.stop()
    GPIO.cleanup()


def driveStraight():
    l_motor_speed = motor_speed
    r_motor_speed = motor_speed

    enc_l_prev = l
    enc_r_prev = r

    revol = distance/circum
    target_count = revol*totalCount
    print("target Count: ", target_count)
    while((l < target_count) and (r < target_count)):
        num_ticks_l = l;
        num_ticks_r = r;

        forward(l_motor_speed, r_motor_speed)

        diff_l = num_ticks_l - enc_l_prev
        diff_r = num_ticks_r - enc_r_prev

        enc_l_prev = num_ticks_l
        enc_r_prev = num_ticks_r

        if(diff_l > diff_r):
            l_motor_speed -= motor_offset
            r_motor_speed += motor_offset
        if(diff_l < diff_r):
            l_motor_speed += motor_offset
            r_motor_speed -= motor_offset

        time.sleep(0.0001)

       # motor_stop()

if __name__ == "__main__":
    motor_pin_setup()
    driveStraight()