# Automated eWaste Unscrewing Control System

## Project Description

This repository is for the control system of the technology demonstrator for autonomous screw removal from waste phones developed as part of our Engineering Design masters group design project at the University of Bristol. This led on from our bachelors research projects on automated phone disassembly. 

### Project Partners:
- Will Smy 
- Nathan Wooster ([LinkedIn](https://www.linkedin.com/in/nathanwooster/), [GitHub](https://github.com/NWooster))
- Smruthi Radhakrishnan ([LinkedIn](https://www.linkedin.com/in/smruthi-radhakrishnan/), [GitHub](https://github.com/smruthi-radhakrishnan))
- Alex Straw ([LinkedIn](https://www.linkedin.com/in/alex-straw/), [GitHub](https://github.com/alex-straw/alex-straw))
### Supervisors
- Mervyn White at the University of Bristol
- Dr Alexi Winters at the Advanced Manufacturing Research Centre
- Jeremy Hadall with the Manufacturing Technology Centre 


| <img src="https://github.com/zaraburton/Automated-eWaste-Unscrewing-Control-System/blob/main/readme_pictures/Automated_Phone_Unscrewing_Poster.png" width="1000"> |
| :--: |
| Project Poster |


| [<img src="https://github.com/zaraburton/Automated-eWaste-Unscrewing-Control-System/blob/main/readme_pictures/vibes.JPG" width="700">](https://drive.google.com/file/d/17BihyDyC95Abv2gOByDlfVvxRjB9EVz_/view?usp=sharing) |
| :--: |
| Video of operations |

## System Overview 

| <img src="https://user-images.githubusercontent.com/79492615/231604244-7f5eaf6e-5e4f-4834-a04e-da4357fa4380.jpg" width="1000">  |
| :--: |
| System diagrams (MC = microcontroller/Arduino) |

Python packages used: sys, keyboard, time, serial, math, numpy, argparse

Justification for software technologies used: 
- Arduino & python on computer used for ease of development & easy interface with python based vision system 
- For serial communication between python on the PC and the Arduinos, pyserial was used over pyfirmata for increased precision of stepper motor control 

Hardware elements used
- Gantry with three NEMA23 stepper motors, TB6600 stepper motor drivers set to 1/32 microstepping & limit switches
- Compliant screwdriver end effector driven by a DC motor with a potentiometer to detect when in contact with phone 
- Overhead camera 
- 3x Arduino microcontrollers for (1) the gantry,  (2) DC motor in the end effector- including a motor shield, and (3) the potentiometer in the end effector
- PC/laptop used as central contoller running python control scripts
- The camera, gantry Arduino & DC motor Arduino are connected via USB to laptop/PC 
- The potentiometer Arduino is directed wireded via digital IOs to the gantry Arduino
- Gantry with three NEMA23 stepper motors, TB6600 stepper motor drivers set to 1/32 microstepping & limit switches
- Compliant screwdriver end effector driven by a DC motor with a potentiometer to detect when in contact with phone 
- Overhead camera 
- 3x Arduino microcontrollers for (1) the gantry,  (2) DC motor in the end effector- including a motor shield, and (3) the potentiometer in the end effector
- PC/laptop used as central contoller running python control scripts
- The camera, gantry Arduino & DC motor Arduino are connected via USB to laptop/PC 
- The potentiometer Arduino is directed wireded via digital IOs to the gantry Arduino


## How it works

| <img src="https://user-images.githubusercontent.com/79492615/231604542-66e96f34-62b1-462b-ab2f-c10b8ae96e50.jpg" width="700"> |<img src="https://user-images.githubusercontent.com/79492615/231605217-e94b2d2b-b52e-46d8-b41c-2e2a9e5c9821.png" width="300">
| :--: | :--: |
| Control software implementation | What's involved in each action |

<details><summary>Set Up Instructions</summary>
<br>
Hardware:
  
- Set up hardware as described above & upload code to Arduino 
- Set com ports for the gantry and dc motor Arduinos in main() of robot_control.py

Gantry system calibration:

- Calibrate steps/mm value - use a dial guage method like with 3D printer calibration (alright for bigger screws), or use the gantry_step_count_test arduino script on the gantry arduino to count the number of steps from multiple known points to the limit switches. Set this in main() func of robot_control.py, line 63 
- Assuming the vision system datum is in a different place to the gantry limit switches, count the number of steps from the vision system datum to the X and Y limit switches and enter in gantry_cntrol.py on line 261 in the start_sequence_for_vsa() (this function runs the initial start sequence to take a photograph and return coordinates of the phone screws, fiddle with this if your screw coordinates are way off.) 
- Values for z heights for the end effector moving over the baseplate and for taking photos may need to be adjusted based on hardware set-up - gantry_control.py lines 220-226
<!--- - Calibrate potentiometer value for touching phone (detailed instructions TBA) -->

Vision system set up:

- Download vision system code developed by Nathan Wooster from [this repo](https://github.com/NWooster/screw_vision_system)
- Copy all files from the Run_vision_system folder into the Python control code folder of this repo
- Create 2 folders called images_taken and images_processed
- When running, if the images_taken folder contains laptop webcam mugshots, change the "1" in the last line of take_picture.py to "0" or vice versa (this 1/0 value for webcam/USB camera is laptop model dependent).

To run:

- Position phone in baseplate
- Run robot_control.py in terminal 
- Follow instructions printed in the terminal 
</details>

| <img src="https://github.com/zaraburton/Automated-eWaste-Unscrewing-Control-System/blob/main/readme_pictures/1screw_mm_output.jpg" width="500">  | <img src="https://user-images.githubusercontent.com/79492615/231605884-f8048477-d865-4600-818d-abd03ba17fe9.png" width="300"> |
| :--: | :--: | 
| Example of vision system output | Screw searching path |



## Future work

- Digital multimeter reading integration to verify engagement and screw removal
- Optimisation of spiralling to maximise success rate & minimise operation time
- Testing at increased speeds and on larger sample of phones

