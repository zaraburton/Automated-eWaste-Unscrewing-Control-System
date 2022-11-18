/*
    Testing arduino sending back big integers to

*/
// serial communication variables
const byte numChars = 64;
char receivedChars[numChars];
char tempChars[numChars]; // temporary array for use when parsing

// to tell the arduino if new instructions have been sent
boolean newData = false;

// feedback vars
int bpSteps = 0;

/*
    extra vars from other script

*/
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

/*
 *    setup & loop 
 * 
 */

void setup() {
  //begin serial communication
  Serial.begin(9600);
} // void setup

void loop() {
  // put your main code here, to run repeatedly:

  recvWithStartEndMarkers();

  if (newData == true) {

    strcpy(tempChars, receivedChars);
    parseData();
    delay(4);

    // attempt to engage phone with toolbit
    if (strcmp(zmotor_py, "E") == 0) {
      engage_z();
    } // if recieved E

    newData = false;

  } // if new data = true
} // void loop
