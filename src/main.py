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
STEERING_GAIN = -0.8
STEERING_BIAS = 0.00
THROTTLE = 0.08
TOTALTIME = 60
print(THROTTLE)

# prepare model
model_trt = TRTModule()
model_trt.load_state_dict(torch.load('/home/jetson/WRO/road_following_model_trt.pth'))
# prepare yolo
model_yolo = YOLO("/home/jetson/WRO/yolo11n.engine")

# prepare car
car = JetRacer(bus=7, signal_freq=50, servo_channel=0, motor_channel=1)
car.steering = 0
car.throttle = 0

# prepare camera
camera = CSICamera(width=640, height=480, capture_fps=30)

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

# start running
throttle_cnt = 0
while True:
    st = time.time()
    image = camera.read()
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
        #print(THROTTLE)

    # if passed_line < 13:# and throttle_cnt % 1 == 0:
    if time.time()-start_time < 180:# and throttle_cnt % 7:
        car.throttle = THROTTLE

    else:
        car.throttle = 0
    throttle_cnt += 1
    # if passed_line == 12:
    if time.time()-start_time > TOTALTIME:
        break
    
    # check if there is end signal
    if GPIO.event_detected(CENTER_CHANNEL):
        while GPIO.event_detected(CENTER_CHANNEL):
            pass
        break
    # print(f"FPS: {int(1/(time.time()-st))}")

car.throttle = 0
car.steering = 0

# enable oled stats
link = "http://localhost:8000/stats/on"
f = requests.get(link)
print(f.text)