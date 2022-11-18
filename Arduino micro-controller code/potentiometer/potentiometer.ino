//---------------------------------- Script to run potentiometer ---------------------------------

// outputs 1 or 0 if force value is achieved, doesn't take any inputs

//-------------------------------------- Define input pins ---------------------------------------

// Define the analogue potentiometer sensor input pin
const int sensorPin = A0;

// Define the digital safety input pin
const int safetyinPin = 1; // Change 1 to pin used

//-------------------------------------- Define output pins --------------------------------------

// Define the digital potentiometer result output pin
const int sensorResult = 10;

// Define the digital safety output pin
const int safetyoutPin = 2; // Change 1 to pin used

//--------------------------------------- Define variables ---------------------------------------

// Define variable to store sensor value
int sensorValue = 0;

// Define variable to output sensor value
int outputValue = 0;

//------------------------------------- Define sensor states -------------------------------------

// Define sensor state for flag output
int sensorState = 0;

//------------------------------------------ Void setup ------------------------------------------

void setup() {
  Serial.begin(9600);
  pinMode(sensorResult, OUTPUT);
  digitalWrite(sensorResult, LOW);
  pinMode(safetyinPin, INPUT);
}

//------------------------------------------ Void loop -------------------------------------------

void loop() {

  // Read sensor value and store in variable
  sensorValue = analogRead(sensorPin);
  //analogWrite(sensorPin, outputValue);

  //Serial.println(sensorValue);




  if (sensorValue >= 740) {

    digitalWrite(sensorResult, HIGH);
    //Serial.println("HIT 6");
  }
  delay(1000);
  digitalWrite(sensorResult, LOW);

}//End of void loop
