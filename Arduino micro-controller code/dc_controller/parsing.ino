
void parseData() {      // split the data into its parts

  char * strtokIndx; // this is used by strtok() as an index

  // variable to indicate whether the motor should start / stop
  strtokIndx = strtok(tempChars, ",");     // get the first part - the string
  strcpy(dcInstruction, strtokIndx);       // copy it to dcInstruction
  //Serial.print("copied");
  //Serial.print("DC INSTRUCTIONS: ");
  //Serial.print(dcInstruction);
  

}




//===============================================================
void recvWithStartEndMarkers() {
  /* Changes newData to true if a message is being sent over serial */
  static boolean recvInProgress = false;
  static byte ndx = 0;
  char startMarker = '<';
  char endMarker = '>';
  char rc;

  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read();
    //Serial.println(rc);

    if (recvInProgress == true) {
      if (rc != endMarker) {
        receivedChars[ndx] = rc;
        ndx++;
        if (ndx >= numChars) {
          ndx = numChars - 1;
        }
      }
      else {
        receivedChars[ndx] = '\0'; // terminate the string
        recvInProgress = false;
        ndx = 0;
        newData = true;
        //Serial.println("new data SHOULD BE true");
      }
    }

    else if (rc == startMarker) {
      recvInProgress = true;
    }
  }
}
