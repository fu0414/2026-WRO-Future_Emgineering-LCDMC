# 2026-WRO-Future_Emgineers-LCDMC

## contents

- [Preface](#Preface)

- [Design plan](#Design-plan)

  - [Vehicle Chassis Selection](#Vehicle-Chassis-Selection)

  - [What upgrades were make to WPL D12?](#What-upgrades-were-made-to-WPL-D12?)

      - [Rear Suspension](#Rear-Suspension)
   
      - [Front Steering Servo](#Front-Steering-Servo)
   
      - [Brushless Motor](#Brushless-Motor)
   
      - [Mechanical Differential Rear Axle](#Mechanical-Differential-Rear-Axle)

  - [Visual Solutions](#Visual-Solutions)

  - [Obstacle Avoidance System Design](#Obsatacle-Avoidance-System-Design)
 
  - [Velosity Controling System Design](#Velosity-Controling-System_Design)
 
  - [Turning System Design](#Turning-System-Design)
 
 - [Materials List](#Materials-List)

 - [Vehicle Photo](#Vehicle-Photo)

 - [Team Photo](#Team-Photo)

 - [Videos](#Videos)

   - [Counter-clockwise obstacle avoidance(complete process)](#Counter-clockwise-obstacle-avoidance(complete-process))
  
   - [Clockwise,without obstruction](#Clockwise,without-obstruction)
  
   - [Counterclockwise,without obstruction](#Counterclockwise,without-obstruction)
  
   - [Clockwise,have obstacles](#Clockwise,have-obstacles)
  
   - [Counterclockwise,have obstacles](#Counterclockwise,have-obstacles)
  
- [Reference link](#Reference-link)


## Preface

We are students from the Tung Wah Group of Hospitals Lee Ching Tak Memorial College. This is our technical document. Our team consists of students passionate about technology and robotics. We hope to explore how robots can solve problems through innovative design, technology, and diverse ideas. In the upcoming World Robot Competition (WRO), we will showcase our creativity and technical strength, striving for excellent results.

Therefore, our main goal in the WRO is to demonstrate our problem-solving abilities and teamwork. We aim to design and develop robots capable of solving real-world problems. We believe that only by constantly challenging ourselves can we achieve greater success. Every competition is a learning opportunity, and we will fully utilize these experiences to continuously improve and pursue excellence.

These are our previous Github repositories for WRO Future Engineers

2024:
- https://github.com/fuqup571/WRO-Future-Engineering-LCDMC

2025:
- https://github.com/fu0414/2025-WRO-Future-Engineering-LCDMC

## Design plan

### Vehicle Chassis Selection

We used the WPL D12 as the chassis for this vehicle because there are more aftermarket parts available for the WPL D12 compared to other toy cars,thus offering greater modification potential.We also used the WPL D12 in 2024,and itsexcellent handling and extremely small turning radius led us to decide to use it again.

### What upgrades were make to WPL D12?

We made upgrades,including the rear suspension,front steering servo,and brushless motor,but most importantly,we upgraded the mechanical differential rear axle.

#### Rear Suspension

We adopted a stiffer rear suspension to withstand greater loads,allowing us to install more sensors or other tools.

#### Front Steering Servo

This increases torque,resulting in faster cornering speeds and reducing the risk of hitting obstacles or walls due to slow cornering speeds.

#### Brushless Motor

This can increase torque.

#### Mechanical Differential Rear Axle

In 2024 and 2025, our vehicles lacked a mechanical differential rear axle. This caused a jamming effect when the front steering angle was too large, as both rear wheels were steering in the same direction. This year, however, we've installed a mechanical differential rear axle, allowing the two wheels to travel at different speeds, eliminating the jamming caused by excessive front steering angles.(You can find the sample video in the [other] file)

### Visual Solutions

For this vehicle,we adopted a purely vision-based solution,so we chose to use the IMX219 camera for road and obstacle recognition because it works out of the box and supports jetson orin nano.

### Obstacle Avoidance System Design

Use a ResNet18 to input camera image and generate steering angle. The ResNet18 AI model is trained with pictures that took with on board IMX219 camera and labelled manually to teach the model to turn correctly in different situation
<img width="1919" height="1020" alt="image" src="https://github.com/user-attachments/assets/23140565-9eb8-437e-823f-192dfa11003c" />
After that we build a model of yolo to tell Orin Nneo what the object is and it can give action

A YOLO11n model is used to get the boundary box and label of the red/green obstacle. Once the yolo model recognized the obstacle and the obstacle is in range, the program will override ResNet18 model steering output, control car's steering base on obstacle's color and position.

In code,we make use of yolo model to identify object with different colour and follow the flow show in figure1.1
<img width="1728" height="1079" alt="image" src="https://github.com/user-attachments/assets/9bee869b-9a18-42a4-988b-1bf90bd7021d" />

### Velosity Controling System Design
At first,we set a throttle value at Orin Neno.We use a separate circuit board to run the PID programme to control and stablize the speed of car to allow us to stop the car at sutible palce on the track through counting the starting time

Here is the graphic shown of how each part of PID avoid the stablize of speed of car

![PID_Compensation_Animated](https://github.com/user-attachments/assets/0fff1022-56bb-44ba-ae9f-740df99037f7)

### Turning System Design
We make use of road following model building method of jetson neno.

At first,we taking some image(around200) and use the different X coordinates repercent the turning (small x-coordinate mean turn left and large x-coordinate mean turn right)
![WhatsApp 图像2025-07-02于16 13 12_3bd753ba](https://github.com/user-attachments/assets/b7b7f950-68ac-4f28-852c-f695385f53c6)

## Power Architecture


## Materials List

- custom built car(WPL D12)
- rear wheel drive wheel base
- metal gear servo
- 10A mosfet motor driver
- 7.4V 5200mah 25C Bettery
- 3D printed mounting board(you can find their STL files in the [models] section)
- orin nano 8GB

## Vehicle Photo

top
![image](https://github.com/fu0414/2026-WRO-Future_Emgineering-LCDMC/blob/main/v-photo/WhatsApp%20Image%202026-07-08%20at%2012.26.43%20AM.jpeg)
bottom
![image](https://github.com/fu0414/2026-WRO-Future_Emgineering-LCDMC/blob/main/v-photo/WhatsApp%20Image%202026-07-08%20at%2012.26.44%20AM.jpeg)
forward
![image](https://github.com/fu0414/2026-WRO-Future_Emgineering-LCDMC/blob/main/v-photo/WhatsApp%20Image%202026-07-08%20at%2012.26.44%20AM%20(2).jpeg)
back
![image](https://github.com/fu0414/2026-WRO-Future_Emgineering-LCDMC/blob/main/v-photo/WhatsApp%20Image%202026-07-08%20at%2012.26.44%20AM%20(1).jpeg)
left
![image](https://github.com/fu0414/2026-WRO-Future_Emgineering-LCDMC/blob/main/v-photo/WhatsApp%20Image%202026-07-08%20at%2012.26.46%20AM.jpeg)
right
![image](https://github.com/fu0414/2026-WRO-Future_Emgineering-LCDMC/blob/main/v-photo/WhatsApp%20Image%202026-07-08%20at%2012.26.45%20AM.jpeg)

## Team Photo

![image](https://github.com/fu0414/2026-WRO-Future_Emgineering-LCDMC/blob/main/t-photo/WhatsApp%20Image%202026-07-08%20at%206.42.17%20PM.jpeg)

## Videos

### Counter-clockwise obstacle avoidance(complete process)
- https://www.youtube.com/watch?v=52Vih6Od3e4

### Clockwise,without obstruction
- https://www.youtube.com/watch?v=cz_oedEK1D4

### Counterclockwise,without obstruction
- https://www.youtube.com/watch?v=CtjAY1_Tr7o

### Clockwise,have obstacles
- https://www.youtube.com/watch?v=bco2o4wXkVQ

### Counterclockwise,have obstacles
- https://www.youtube.com/watch?v=CQ-CMoyexY8

## Reference link
