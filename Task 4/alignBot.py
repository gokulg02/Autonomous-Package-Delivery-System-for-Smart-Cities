import math
import cv2
import numpy as np
import time
import warnings
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

warnings.filterwarnings("ignore")

# initializing the pin numbers where motors are connected
L_PWM_PIN1 = 38
L_PWM_PIN2 = 40
R_PWM_PIN2 = 32
R_PWM_PIN1 = 33
L_EN = 31
R_EN = 37
motor_speed = 50
motor_offset = 30
#encoder
enc_l = enc_r = 0
l_enc = 24
r_enc = 26
totalCount = 20
circum = 23 #cm
dia = 23/math.pi
width = 16 #cm
#enc int
def l_int(channel):
    global enc_l
    enc_l += 1

def r_int(channel):
    global enc_r,r
    enc_r += 1
    
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

def driveStraight(distance):
    l_motor_speed = motor_speed
    r_motor_speed = motor_speed

    enc_l_prev = enc_l
    enc_r_prev = enc_r

    revol = distance/circum
    target_count = revol*totalCount
    print("target Count: ", target_count)
    while((enc_l < target_count) and (enc_r < target_count)):
        num_ticks_l = enc_l;
        num_ticks_r = enc_r;

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

        time.sleep(0.001)

    stop()

def stop():
    L_MOTOR1.ChangeDutyCycle(0)
    R_MOTOR1.ChangeDutyCycle(0)
    L_MOTOR2.ChangeDutyCycle(0)
    R_MOTOR2.ChangeDutyCycle(0)

def turnLeft(angle):
    print(steering_angle1,"- Turn Left")
    L_MOTOR1.ChangeDutyCycle(0)
    R_MOTOR2.ChangeDutyCycle(0)
    L_MOTOR2.ChangeDutyCycle(motor_speed)
    R_MOTOR1.ChangeDutyCycle(motor_speed)
    time.sleep(0.03)
    stop()
    # time.sleep(0.05)

def turnRight(angle):
    print(angle,"-Turn Right")
    L_MOTOR1.ChangeDutyCycle(motor_speed)
    R_MOTOR2.ChangeDutyCycle(motor_speed)
    L_MOTOR2.ChangeDutyCycle(0)
    R_MOTOR1.ChangeDutyCycle(0)
    time.sleep(0.03)
    stop()
    # time.sleep(0.05)
    
def canny(image):
    gray=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    blur=cv2.GaussianBlur(gray,(5,5),0)
    #lower_bound = np.array([0, 0, 0])
    #upper_bound = np.array([0,0,0])
    #imagemask = cv2.inRange(blur, 75, 255)
    ret, imagemask = cv2.threshold(blur, 100, 255, 1) #prev 80
    canny=cv2.Canny(imagemask,50,150)
    return [canny,imagemask]

def make_points(frame, line):
    height, width, _ = frame.shape
    slope, intercept = line
    y1 = height  # bottom of the frame
    y2 = int(y1 * 1 / 2)  # make points from middle of the frame down

    # bound the coordinates within the frame
    x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
    x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
    return [[x1, y1, x2, y2]]

def average_slope_intercept(frame, line_segments): 
    lane_lines = []
    if line_segments is None:
        return lane_lines

    height, width, _ = frame.shape
    left_fit = []
    right_fit = []

    #boundary = 1/3
    #left_region_boundary = width * (1 - boundary)  # left lane line segment should be on left 2/3 of the screen
    #right_region_boundary = width * boundary # right lane line segment should be on left 2/3 of the screen

    for line_segment in line_segments:
        for x1, y1, x2, y2 in line_segment:
            #if x1 == x2:
                #continue
            if(abs(y1 - y2)<50 and abs(x1 - x2)>20):
                continue    
            fit = np.polyfit((x1, x2+1), (y1, y2), 1)
            slope = fit[0]
            intercept = fit[1]
            if slope < 0:
                #if x1 < left_region_boundary and x2 < left_region_boundary:
                    left_fit.append((slope, intercept))
            else:
                #if x1 > right_region_boundary and x2 > right_region_boundary:
                    right_fit.append((slope, intercept))
    
    left_fit_average = np.average(left_fit, axis=0)
    if len(left_fit) > 0:
        lane_lines.append(make_points(frame, left_fit_average))

    right_fit_average = np.average(right_fit, axis=0)
    if len(right_fit) > 0:
        lane_lines.append(make_points(frame, right_fit_average))

    return lane_lines

def display_lines(image,lines):
    line_image=np.zeros_like(image)
    if lines is not None:
         for line in lines:
            for x1, y1, x2, y2 in line:
               cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),5)
    return line_image



if __name__ == "__main__":
    motor_pin_setup()
    print("Motor Setup Done.")
    cap = cv2.VideoCapture(0)
    

    while cap.isOpened():

        ret, frame = cap.read()
        try:
            img=np.copy(frame)
            img=cv2.resize(img,(320,240))
            cannyimg = canny(img)
            lines=cv2.HoughLinesP(cannyimg[0],2,np.pi/180,30,np.array([]),minLineLength=160,maxLineGap=50)
            #lines=cv2.HoughLinesP(cannyimg[0],1,np.pi/180,10,np.array([]),minLineLength=70,maxLineGap=4)
            lane_lines=average_slope_intercept(img,lines)
            houghlines = display_lines(img,lines)
            avglines = display_lines(img,lane_lines)
            combo_image=cv2.addWeighted(img,0.8,avglines,1,1)

            height, width, _ = img.shape
            #print(lane_lines)
            if len(lane_lines)==1:
                x1, _, x2, _ = lane_lines[0][0]
                x_offset = x2 - x1
            else:     
                left_x1, _, left_x2, _ = lane_lines[0][0]
                right_x1, _, right_x2, _ = lane_lines[1][0]
                #mid = int(width / 2)
                mid= int((right_x1+left_x1)/2)
                x_offset = (left_x2 + right_x2) / 2 - mid  
            y_offset = int(height / 2)
            angle_to_mid_radian = math.atan(x_offset / y_offset)  # angle (in radian) to center vertical line
            angle_to_mid_deg = int(angle_to_mid_radian * 180.0 / math.pi)  # angle (in degrees) to center vertical line
            steering_angle = angle_to_mid_deg + 90  # this is the steering angle needed by picar front wheel
            steering_angle1=180-steering_angle
            print(steering_angle1)
            if 89 <= steering_angle1 <= 91:
                print("Go Straight.")
                break
            elif steering_angle1 <= 88 :
                #print("Turn Right.")
                turnRight(steering_angle1)
            elif steering_angle1 > 91:
                #print("Turn Left.")
                turnLeft(steering_angle1)
            else:
                print("Wait.")
            def display_heading_line(frame, steering_angle,mid=width/2,line_color=(0, 0, 255), line_width=5 ):
                heading_image = np.zeros_like(frame)
                height, width, _ = frame.shape

                steering_angle_radian = steering_angle / 180.0 * math.pi
                #x1 = int(width / 2)
                x1=int(mid)
                y1 = height
                x2 = int(x1 - height / 2 / math.tan(steering_angle_radian))
                y2 = int(height / 2)

                cv2.line(heading_image, (x1, y1), (x2, y2), line_color, line_width)
                heading_image = cv2.addWeighted(frame, 0.8, heading_image, 1, 1)
                return heading_image

            if(len(lane_lines)==1):
                heading_image=display_heading_line(combo_image,steering_angle)
            else:    
                heading_image=display_heading_line(combo_image,steering_angle,mid)
            
            #cv2.imshow("imagemask",cannyimg[1])
            cv2.imshow("canny",cannyimg[0])
            #cv2.imshow("houghlines",houghlines)
            #cv2.imshow("avglines",avglines)
            cv2.imshow("headingimg",heading_image)

        except Exception as e:
            print(e)
            pass
        time.sleep(0.2)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows
            break    