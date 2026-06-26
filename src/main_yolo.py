import Jetson.GPIO as GPIO
import requests
import time
import torch
from torch2trt import TRTModule
from robot.jetracer import JetRacer
from jetcam.csi_camera import CSICamera
from utils import preprocess
import numpy as np
import time
import serial
from ultralytics import YOLO

CENTER_CHANNEL = 19
STEERING_GAIN = -1.3
STEERING_BIAS = 0.00
TURN_DISTANCE = 270
THROTTLE = 0.04
TOTALTIME = 90

# prepare model
model_trt = TRTModule()
model_trt.load_state_dict(torch.load('/home/jetson/WRO/road_following_model_trt.pth'))
# prepare yolo
model_yolo = YOLO("/home/jetson/WRO/yolo11n.engine")

# prepare car
car = JetRacer(bus=7, signal_freq=50, servo_channel=0, motor_channel=1)
car.steering = 0.0
car.throttle = 0.0

# prepare camera
camera = CSICamera(width=640, height=480, capture_fps=60)
camera.running = True

# init GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(CENTER_CHANNEL, GPIO.IN)
GPIO.add_event_detect(CENTER_CHANNEL, GPIO.RISING, bouncetime=200)

# disable oled stats
link = "http://localhost:8000/stats/off"
f = requests.get(link)
print(f.text)

# display can_start text
link = "http://localhost:8000/text/can_start"
f = requests.get(link)
print(f.text)

# wait start signal
while True:
    if GPIO.event_detected(CENTER_CHANNEL):
        while GPIO.event_detected(CENTER_CHANNEL):
            pass
        break
    time.sleep(0.1)

# display running text
link = "http://localhost:8000/text/running"
f = requests.get(link)
print(f.text)

# store passed how many line
passed_line = 0
last_passed_time = 0
start_time = time.time()

def backward():
    car.throttle = 0
    car.steering = 0.0
    time.sleep(0.5)
    car.throttle = -0.05
    time.sleep(0.7)
    car.throttle = 0

# start running
throttle_cnt = 0
while True:
    st = time.time()
    image = camera.value#read()
    # YOLO
    yolo_results = model_yolo(image, verbose=False)
    # Resnet
    image = preprocess(image).half()
    output = model_trt(image).detach().cpu().numpy().flatten()
    x = float(output[0])
    skew = (x * STEERING_GAIN + STEERING_BIAS)
    car.steering = skew
    # print(skew)
    y = float(output[0])
    #print(y)
    if y < -0.05 and time.time()-last_passed_time > 1.5:
        last_passed_time = time.time()
        passed_line += 1
        print(passed_line)

    # if passed_line < 13:# and throttle_cnt % 1 == 0:
    if time.time()-start_time < 180:# and throttle_cnt % 7:
        car.throttle = THROTTLE
    else:
        car.throttle = 0
    throttle_cnt += 1
    # if passed_line == 12:
    if time.time()-start_time > TOTALTIME:
        break

    #YOLO
    boxes = yolo_results[0].boxes.xyxy.tolist()
    classes = yolo_results[0].boxes.cls.tolist()
    names = yolo_results[0].names
    confidences = yolo_results[0].boxes.conf.tolist()
    red_target = 120
    green_target = 500
    for box, cls, conf in zip(boxes, classes, confidences):
        x1, y1, x2, y2 = box
        confidence = conf
        detected_class = cls
        name = names[int(cls)]
        # xpos = (x1+x2)/2
        ypos = (y1+y2)/2
        # if name == "scissors" or name == "bottle":
        #     print(name, (y1+y2)/2)
        if y2 > TURN_DISTANCE:
        # if ypos > TURN_DISTANCE:
            # print(int(cls), ypos, xpos)
            # print(int(cls), y2)
            if int(cls) == 0:#name == "scissors":#red
                if x2 > red_target:
                    car.steering = (x2-red_target)/160
                    if y2 > 400:
                        backward()
                # if xpos > red_target:
                    # car.steering = (xpos-red_target)/160
                break
            elif int(cls) == 1:#name == "bottle":#green
                # print(y2, x1, -(green_target-x1)/160)
                if x1 < green_target:
                    car.steering = -(green_target-x1)/160
                    if y2 > 380:
                        backward()
                # if xpos < green_target:
                    # car.steering = -(green_target-xpos)/160
                break
    
    # check if there is end signal
    if GPIO.event_detected(CENTER_CHANNEL):
        while GPIO.event_detected(CENTER_CHANNEL):
            pass
        break
    # print(f"FPS: {int(1/(time.time()-st))}")

car.throttle = 0

# enable oled stats
link = "http://localhost:8000/stats/on"
f = requests.get(link)
print(f.text)