# Automated eWaste Unscrewing Control System

## Project Description

This repository is for the control system of the technology demonstrator for autonomous screw removal from waste phones developed as part of my master's in Engineering Design at the University of Bristol, partnered with the Advanced Manufacturing Research Centre. 

## System Overview 

![System Overview](https://github.com/zaraburton/Automated-eWaste-Unscrewing-Control-System/blob/main/readme_pictures/ddintro2.png)

Hardware elements used 
- gantry with three stepper motors & limit switches
- compliant screwdriver end effector with a potentiometer to detect when in contact with phone 
- overhead camera 

Justification for software technologies used: 
- Arduino & python on computer used for ease of development & easy interface with python based vision system 
- For serial communication between python on the PC and the Arduinos, pyserial was used over pyfirmata for increased precision of stepper motor control 


## How to Install and Run the Project

Hardware diagrams TBA

Wiring diagrams TBA

### Set Up Instructions
#### Hardware 
- Hardware set up as shown in diagrams & upload code to Arduino 
- Set com ports
#### Gantry system calibration
- Calibrate steps/mm value (this should be calibrated with a dial gauge, as shown in this video, details TBA)
- Calibrate datum position of vision system checkered square (detailed instructions TBA)
- Calibrate potentiometer value for touching phone (detailed instructions TBA)
- Values for z heights may need to be adjusted based on hardware set-up 
#### Vision system set up 
- Download vision system code developed by Nathan Wooster from [this repo](https://github.com/NWooster/screw_vision_system)
- Ensure folder layout correct (details TBA)
- Set values to 1/0 for webcam / USB camera (laptop model dependent)

### To run
- Position phone 
- Run rx.py in terminal 
- Follow instructions printed in the terminal 

## How it works 

Process flow of operations TBA

Description TBA

### Further developments 

#### Hardware
- Recentering of end effector 

#### Software
- Calibration of image - real world coordinates in vision system
- Bug fixing of vision system to repeatedly set datum from exact real world coordinate
- Multimeter reading and integration to verify engagement and screw removal 
- Further optimisation of spiralling to maximise success rate & minimise operation time


## Credits
- Group project partners Nathan Wooster, who worked on the vision system ([LinkedIn](https://www.linkedin.com/in/nathanwooster/), [GitHub](https://github.com/NWooster)) & Will Smy.
- Project supervisors Mervyn White at the University of Bristol & Dr Alexi Winters at the AMRC 
