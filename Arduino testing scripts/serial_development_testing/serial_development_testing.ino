//#include <string>
//#include <StackString.hpp>
//using namespace Stack; // Important!

/* serial instructions to arduino sent over 32 bytes, indexed 0-31

    index: 0  (message start marker)

    index: 1 -- 11 -- 21
            direction (1)
            l,r,u,d,f,b,n
            n = no movement

    index: 2,3,4,5 -- 12,13,14,15 -- 22,23,24,25
            speed (4)
            1-1000

    index: 6,7,8,9,10 -- 16,17,18,19,20 -- 26,27,28,29,30
            steps (5) 
            1-89000

    index: 31 (message end marker)

    example --- <x0z0047860n00000000d002000095>
            --- x motor 
                  - left
                  - pulse delay = 500 ms
                  - steps = 47860
            --- y motor doesnt move
            --- z motor
                  - down
                  - pulse delay = 20 ms
                  - steps = 95
*/


//defines pins //for X stepper motor
const int XstepPin = 6;  //PUL -Pulse
const int XdirPin = 7; //DIR -Direction
const int enPin = 8;  //ENA(+)  - to enable or disable motor ??, the ENA(-) on motor driver is to ground

// for Y stepper motor
const int YstepPin;
const int YdirPin; 
//for Z stepper motor
const int ZstepPin;  
const int ZdirPin; 

// define variables

# define todo 1 // value for an action to do
# define done 0 // value for action when it's done

const byte numChars = 32;
char receivedChars[numChars]; //message to be recieved
String receievedString;
boolean newData = false; //indicates when a message has been recieved

int action = 0; // variable of whether an action needs to be done 
int incomingByte; // a variable to read the incoming serial data 

//x,y,z move/not move variables
char mx;
char my;
char mz;


// recieve message
void recvWithStartEndMarkers() {
    static boolean recvInProgress = false; //if receiving is in progress
    static byte ndx = 0;  // recieved byte index starts at 0
    char startMarker = '<'; // character indicating start of message
    char endMarker = '>'; // character indicating start of message
    char rc;  // recieved character
 
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) { //when you're recieving a message
            if (rc != endMarker) { // and its not the end marker
                receivedChars[ndx] = rc; //add the character recieved to the recieved characters list
                ndx++;  //plus 1 to the index 

                Serial.print(receivedChars[ndx]);
                if (ndx >= numChars) {  //if index > 32, 
                    ndx = numChars - 1;  // index = 32
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true; // says you have new data avaliable to process onces everythings been recieved
            }
        }

        else if (rc == startMarker) {  //if you recieve the start marker
            recvInProgress = true; // change status to recieving message
        }
    }
}
    



void setup(){
  // initialize serial communication:
  Serial.begin(9600);

  //Sets the pins as Outputs
  pinMode(XstepPin,OUTPUT); 
  pinMode(XdirPin,OUTPUT);

  pinMode(YstepPin,OUTPUT); 
  pinMode(YdirPin,OUTPUT);

  pinMode(ZstepPin,OUTPUT); 
  pinMode(ZdirPin,OUTPUT);

  pinMode(enPin,OUTPUT);
  digitalWrite(enPin,LOW);
}


void loop(){
  //recieve any incoming messages
  recvWithStartEndMarkers(); 
  // complete instructions recieved
  if (newData == true) {
    Serial.print("action:todo");
    newData==false;
    
  }
}
