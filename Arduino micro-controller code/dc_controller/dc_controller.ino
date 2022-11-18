// send instructions as <S> = turn slow, <F> turn fast, <P> pause turning


//#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

// define motor
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *Motor = AFMS.getMotor(2);

// pins
const int dcPin = 50;


// serial communication variables
const byte numChars = 16;
char receivedChars[numChars];
char tempChars[numChars]; // temporary array for use when parsing

boolean newData = false; // to tell the arduino if new instructions have been sent

// variable to hold the parsed python data on DC motor instructions
char dcInstruction[numChars] = {0}; // indicates motor to turn/stop

void setup() {
  // put your setup code here, to run once:

  //digitalWrite(dcPin, LOW);
  AFMS.begin();
  Serial.begin(9600);
  delay(200);

}

void loop() {
  // put your main code here, to run repeatedly:

  // read serial input from python
  recvWithStartEndMarkers();
  delay(4);
  //Serial.println(newData);
  //if it's sent an instruction
  if (newData == true) {
    //Serial.println("new data true");

    // make temporary copy of recieved data
    strcpy(tempChars, receivedChars);

    // parse data
    parseData();

    delay(4);


    // check what instruction was sent & act on it

    // "S" = start unscrewing slowly
    if (strcmp(dcInstruction, "S") == 0) {  // checks G was sent

      // set DC motor pin to HIGH
      //Serial.println("should run SLOW");
      //digitalWrite(dcPin, HIGH);
      Motor -> setSpeed(20);
      Motor -> run(FORWARD);

    }

    // "F" = FAST unscrewing
    if (strcmp(dcInstruction, "F") == 0) {  // checks G was sent

      // set DC motor pin to HIGH
      //Serial.println("should run FAST");
      //digitalWrite(dcPin, HIGH);
      Motor -> setSpeed(100);
      Motor -> run(FORWARD);

    }

    // "P"ause = stop unscrewing
    if (strcmp(dcInstruction, "P") == 0) {  // checks P was sent

      // set DC motor pin to LOW
      //Serial.println("motor should stop");
      //digitalWrite(dcPin, LOW);

      Motor -> setSpeed(0);
    }

    newData = false;

  }

} // void loop
