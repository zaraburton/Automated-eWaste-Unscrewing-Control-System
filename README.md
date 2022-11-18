# Automated eWaste Unscrewing Control System

## Project Description

This repository is for the control system of the teachnology demonstrator for autonomous screw removal from waste phones developed as part of my masters in Engineering Design at the University of Bristol, partnered with the Advanced Manufacturing Research Centre. 

The project poster is shown below - see here for the full image

<embed src="https://drive.google.com/file/d/1hHOzlD-ifWzZcyybPflSExxP2BwYN0X_/view?usp=sharing" type="application/pdf">

Here is a video of the final system in action:

- video

- process flow

## System overview 
This is a list of the basic hardware elements used to follow the process flow shown above
- gantry with 3 stepper motors & limit switches
- compliant screw driver end effector with potentiometer to detect when in contact with phone 
- overhead camera 


Control features:
- spiralling 
- user input currently used to verify if end effector engaged with screw & the screw is removed
- 

Justification for software technologies used: 
- arduino & python on computer used for ease of development & easy interface with python based vision system 
- for serial communication between python on the PC and the arduinos, pyserial was used over pyfirmata for increased precision of stepper motor control 
- gcode was not used as only XXXXX


- python-arduino control of stepper motors (3d printer /gantry)





## How to Install and Run the Project
steps required to install your project and also the required dependencies if any.

Hardware diagrams
Wiring diagrams 

### Set Up Instructions
#### Hardware 
- hardware set up as shown in diagrams & upload code to arduinos 
- change com ports
#### Gantry system calibration
- calibrate steps/mm value (this should be calibrated with a dial guage, as shown in this video, this script can be used)
- calibrate datum position of Vs square using this code to count back from it 
- calibrate potentiometer value for touching phone 
- values for z heights may need to be adjusted based on hardware set up 
#### Vision system set up 
- download vision system code developed by Nathan Wooster from [this repo](https://github.com/NWooster/screw_vision_system)
- have in correct folder layout 
- set values to 1/0 for webcam / usb camera (laptop model dependant)

### To run
- position phone in 
- run rx.py in terminal 
- follow instructions printed in terminal 

## How it works 

Process flow of operations 
How it works descriptions 
- whole robot
- my code - serial coms, spiralling

### Further developments 

#### Hardware
- recentering of end effector 

#### Software
- calibration of image - real world coordinates in vision system
- bug fixing of vision system to repeatedly set datum from exact real world coordinate
- multimeter reading and integration to verify engagement and screw removal 
- optimisation of spiralling 


## Credits
- Group project partners Nathan Wooster, who worked on the vision system ([LinkedIn](https://www.linkedin.com/in/nathanwooster/), [GitHub](https://github.com/NWooster)) & Will Smy.
- Project supervisors Mervyn White at University of Bristol & Dr Alexi Winters at the AMRC 
- serial comms guy for arduino 
- gantry calibration stuff 

