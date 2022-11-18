/* serial instructions to arduino sent in format:
      <N,N,N,0,0,0,n,n,n,0,0,0>
      <string,string,string,long long,long long,long long,string,string,string,int,int,int>

    where < and > are message start and end markers

    index 1-3: X/N/zero/S, Y/N/zero/S, Z/N/zero/S/E
      - X/Y/Z will allow respective motor movement
        - must be capitalised
        - N placement character for no movement
      - unless X/Y/Z is sent, non 0 or n values in following positions will not trigger movement
      - zero-ing
        - zero,zero,zero will move all axis to datum point at stopper buttons
        - zero,zero,N will move only X & Y axis to datum point
      - S = for when a new screw is to be moved to, or spiral search is initiated, from when already in contact with pphone/screw
      - E = when trying to engage with screw - already above screw and jsut want to move down in Z

    index 4-6: any  integer from 0-2147483647
      - steps to be taken by motor X, Y and Z respectively

    index 7-9: n/l/r, n/f/b, n/u/d/a
      - stepper direction
        - n = no movement
        - l = left, r = right [x motor]
        - f = forwards, b = backwards [y motor]
        - u = up, d = down, s = both directions (for when moving up then down for *S*piral search or next *S*crew) [z motor]

    index 10-12: any integer from 0-255
      - motor speed
      - value used as microsecond pulse delay

    Example:

        <X,Y,N,350,20,0,l,f,n,200,100,0>

        will move the end effector 350 steps left with a 200ms pulse delay in the x axis
        and move 20 steps forward, with a 100ms pulse delay in the y axis (this is 2x as fast as the x axis movement)

        no movement == <N,N,N,0,0,0,n,n,n,0,0,0>
        zero each axis == <zero,zero,zero,0,0,0,l,b,d,0,0,0>

*/


// serial communication variables
const byte numChars = 64;
char receivedChars[numChars];
char tempChars[numChars]; // temporary array for use when parsing

// to tell the arduino if new instructions have been sent
boolean newData = false;


// variables to hold the parsed python data on stepper instructions
// x motor
char xmotor_py[numChars] = {0}; // indicates x motor to move
char xsteps_char[numChars] = {0}; // temporary character array/string of steps to convert to long long
long long xsteps_py = 0; // steps to take in x axis
int xpd = 200; // x speed (pulse delay in microseconds)
char xdir_py[numChars] = {0}; // x direction (l=left, r=right)

// y motor
char ymotor_py[numChars] = {0};
char ysteps_char[numChars] = {0};
long long ysteps_py = 0;
long long ypd = 200;
char ydir_py[numChars] = {0}; // y direction (f=forwards, b=backwards)

// z motor
char zmotor_py[numChars] = {0};
char zsteps_char[numChars] = {0};
long long zsteps_py = 0;
long long zpd = 200;
char zdir_py[numChars] = {0}; // z direction (u=up, d=down)


// Pins of motors
// x stepper pins
const int XstepPin = 2;  //PUL X - Pulse
const int XdirPin = 3; //DIR X - Direction
const int enPin = 4;  //ENA(+) X  - to enable or disable motor, the ENA(-) on motor driver is grounded

// y pins
const int YstepPin = 5; // PUL Y
const int YdirPin = 6; // DIR Y
const int YenPin = 7; // ENA Y

// z pins
const int ZstepPin = 8; // PUL Z
const int ZdirPin = 9; // DIR Z
const int ZenPin = 10; // ENA Z

// datum button pins
const int xButtonPin = 11;
const int yButtonPin = 12;
const int zButtonPin = 13;

// button variables
boolean xButtonPressed = false;
boolean yButtonPressed = false;
boolean zButtonPressed = false;


// pentiometer pin
const int pentInPin = 44;  /// <--------


// pent variables
boolean contact = false;

//============

// position feedback variables
// u=unmoved, c=complete, z=zero position/buttons hit
int xFbPos = 0;
int yFbPos = 0;
int zFbPos = 0;

int bpSteps = 0;
long xSteps = 0;
long ySteps = 0;

void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);

  // set the stepper pins as Outputs
  pinMode(XstepPin, OUTPUT);
  pinMode(XdirPin, OUTPUT);
  pinMode(YstepPin, OUTPUT);
  pinMode(YdirPin, OUTPUT);
  pinMode(ZstepPin, OUTPUT);
  pinMode(ZdirPin, OUTPUT);

  pinMode(enPin, OUTPUT);
  digitalWrite(enPin, LOW);

  // button pins
  pinMode(xButtonPin, INPUT_PULLUP);
  pinMode(yButtonPin, INPUT_PULLUP);
  pinMode(zButtonPin, INPUT_PULLUP);

  // pent pin
  pinMode(pentInPin, INPUT);

  //begin serial communication
  Serial.begin(9600);


}

//===============================================================

void loop() {

  recvWithStartEndMarkers();
  if (newData == true) {
    strcpy(tempChars, receivedChars);
    // this temporary copy is necessary to protect the original data
    //   because strtok() used in parseData() replaces the commas with \0
    parseData();

    delay(4);

    // set position feedback as "unmoved"
    xFbPos = 0;
    yFbPos = 0;
    zFbPos = 0;

    // MOVE MOTORS
    // move z
    if (strcmp(zmotor_py, "Z") == 0) {
      move_z();
      //send_fb();
    }

    // move x
    if (strcmp(xmotor_py, "X") == 0) {  // checks X was sent
      move_x();
      //send_fb();
    }

    // move y
    if (strcmp(ymotor_py, "Y") == 0) {
      move_y();
      //send_fb();
    }

    // move to datum (0,0,0)
    if (strcmp(xmotor_py, "zero") == 0 && strcmp(ymotor_py, "zero") == 0 && strcmp(zmotor_py, "zero") == 0) {
      zero_xy(); //CHANGE THIS BACK TO XYZ 
      send_fb();
    }

    //move x&y to datum (0,0)
    //if (strcmp(xmotor_py, "zero") == 0 && strcmp(ymotor_py, "zero") == 0) {
      //zero_xy();
      //send_fb();
    //}

    //move z to datum (x,x,0)
    //if (strcmp(zmotor_py, "zero") == 0) {
      //zero_z();
      //send_fb();
    //}

    // move to new point (for new screw, or when sprial searching)
    if (strcmp(xmotor_py, "S") == 0 && strcmp(ymotor_py, "S") == 0 && strcmp(zmotor_py, "S") == 0) {
      new_point();
    }

    // attempt to engage phone with toolbit
    if (strcmp(zmotor_py, "E") == 0) {
      engage_z();
    }

    // set motor directions back to HIGH (left, forwards, up) after running to keep them happy
    digitalWrite(XdirPin, HIGH);
    digitalWrite(YdirPin, HIGH);
    digitalWrite(ZdirPin, HIGH);
    
    newData = false;

    if (strcmp(zmotor_py, "E") != 0) {
      send_fb();
    }
  }
}

void send_fb() {
  // send feedback on action/position in each axis
  //int fb = 1;
  //Serial.println(fb);


  Serial.print("X STEPS: ");
  Serial.println(xSteps);
  Serial.print("Y STEPS: ");
  Serial.println(ySteps);
  

} // void send fb()


void move_x() {
  // x speed set by xpd already
  // set x direction
  if (strcmp(xdir_py, "l") == 0) {
    digitalWrite(XdirPin, HIGH); // left
    //Serial.println("x:l");
  }
  else if (strcmp(xdir_py, "r") == 0) {
    digitalWrite(XdirPin, LOW); // right
    //Serial.println("x:r");
  }
  xButtonPressed = false;
  xSteps = 0;
  // loop over each step
  for (long long x = 0; x < xsteps_py; x++) {
    // check if the button has been pressed if moving left
    if (strcmp(xdir_py, "l") == 0) {
      readButtonX();
    }
    // break out the stepping loop if the button is pressed
    if (ifcondtionismetbreak(xButtonPressed)) {
      break;
    }
    // make pulses to turn motor
    digitalWrite(XstepPin, HIGH);
    delayMicroseconds(xpd);
    digitalWrite(XstepPin, LOW);
    delayMicroseconds(xpd);

    xSteps++;
  }
  // send feedback that all steps were completed if the button was not pressed
  if (xButtonPressed == false) {
    xFbPos = 1;
  }
  if (xButtonPressed == true) {
    xFbPos = 2;
  }
}


void move_y() {
  // set y direction
  if (strcmp(ydir_py, "f") == 0) {
    digitalWrite(YdirPin, HIGH); // forwards
  }
  if (strcmp(ydir_py, "b") == 0) {
    digitalWrite(YdirPin, LOW); // backwards
  }
  yButtonPressed = false;
  ySteps = 0;
  // loop over each step
  for (long long y = 0; y < ysteps_py; y++) {

    // check if the button has been pressed if moving backwards
    if (strcmp(ydir_py, "b") == 0) {
      readButtonY();
    }
    // break out the stepping loop if the button is pressed
    if (ifcondtionismetbreak(yButtonPressed)) {
      break;
    }
    // make pulses to turn motor
    digitalWrite(YstepPin, HIGH);
    delayMicroseconds(ypd);
    digitalWrite(YstepPin, LOW);
    delayMicroseconds(ypd);
    ySteps++;
  }
  // send feedback that all steps were completed if the button was not pressed
  if (yButtonPressed == false) {
    yFbPos = 1;
  }
  if (yButtonPressed == true) {
    yFbPos = 2;
  }
}

void move_z() {
  // set z direction
  if (strcmp(zdir_py, "u") == 0) {
    digitalWrite(ZdirPin, LOW); // up (in terms of end effector)
  }
  if (strcmp(zdir_py, "d") == 0) {
    digitalWrite(ZdirPin, HIGH); // down (in terms of end effector)
  }
  zButtonPressed = false;
  // loop over each step
  for (long long z = 0; z < zsteps_py; z++) {

    // check if the limit switch has been pressed if moving down
    if (strcmp(zdir_py, "d") == 0) {
      readButtonZ();
    }
    // break out the stepping loop if the limit switch is pressed
    if (ifcondtionismetbreak(zButtonPressed)) {
      break;
    }

    // make pulses to turn motor
    digitalWrite(ZstepPin, HIGH);
    delayMicroseconds(zpd);
    digitalWrite(ZstepPin, LOW);
    delayMicroseconds(zpd);
  }
  // send feedback that all steps were completed if the button was not pressed
  if (zButtonPressed == false) {
    zFbPos = 1;
  }
  if (zButtonPressed == true) {
    zFbPos = 2;
  }
}

void zero_xyz() {
  // set directions
  strcpy(xdir_py, "l");
  strcpy(ydir_py, "b");
  strcpy(zdir_py, "d");

  // set speeds
  xpd = 1000;
  ypd = 1000;
  zpd = 500;

  // set high steps to ensure buttons are hit
  xsteps_py = 90000;
  ysteps_py = 90000;
  zsteps_py = 90000;

  // move motors
  //move_z();
  move_x();
  move_y();
  
}

void zero_xy() {
  // set directions
  strcpy(xdir_py, "l");
  strcpy(ydir_py, "b");

  // set speeds
  xpd = 1000;
  ypd = 1000;

  // set high steps to ensure buttons are hit
  xsteps_py = 90000;
  ysteps_py = 90000;

  // move motors
  move_x();
  move_y();
}

void zero_z() {
  // set direction
  strcpy(zdir_py, "d");

  // set speeds
  zpd = 700;

  // set high steps to ensure buttons are hit
  zsteps_py = 900000;

  // move motor
  move_z();

}
