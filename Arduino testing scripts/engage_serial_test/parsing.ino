long long char_to_LL(char *str){
  /* converts character array to long long int */
  long long result = 0; // Initialize result
  // Iterate through all characters of input string and update result
  for (int i = 0; str[i] != '\0'; ++i)
    result = result*10 + str[i] - '0';
  return result;
}

void LL_to_Serial(long long ll){
  /* prints long long int variable over serial */
  uint64_t xx = ll/1000000000ULL;
  if (xx >0) Serial.print((long)xx);
  Serial.print((long)(ll-xx*1000000000));
}

//===============================================================

void parseData() {      // split the data into its parts

  char * strtokIndx; // this is used by strtok() as an index

  // variables to indicate whether a motor is needed
  strtokIndx = strtok(tempChars, ",");     // get the first part - the string
  strcpy(xmotor_py, strtokIndx); // copy it to xmotor_py
  strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
  strcpy(ymotor_py, strtokIndx); // ymotor_py
  strtokIndx = strtok(NULL, ",");
  strcpy(zmotor_py, strtokIndx); // zmotor_py


  // motor steps inputs
  // x steps
  strtokIndx = strtok(NULL, ",");
  strcpy(xsteps_char, strtokIndx); // create string of step value
  xsteps_py = char_to_LL(xsteps_char); // steps as long long varaible
  // y steps
  strtokIndx = strtok(NULL, ",");
  strcpy(ysteps_char, strtokIndx);
  ysteps_py = char_to_LL(ysteps_char);
  // z steps
  strtokIndx = strtok(NULL, ",");
  strcpy(zsteps_char, strtokIndx);
  zsteps_py = char_to_LL(zsteps_char);

  // motor direction inputs
  strtokIndx = strtok(NULL, ",");
  strcpy(xdir_py, strtokIndx); // x direction
  strtokIndx = strtok(NULL, ",");
  strcpy(ydir_py, strtokIndx); // y direction
  strtokIndx = strtok(NULL, ",");
  strcpy(zdir_py, strtokIndx); // z direction

  // motor speed (pulse delay in microseconds) inputs (200 good for 8 step setting)
  strtokIndx = strtok(NULL, ",");
  xpd = atoi(strtokIndx); // x pulse delay
  strtokIndx = strtok(NULL, ",");
  ypd = atoi(strtokIndx); // y pulse delay
  strtokIndx = strtok(NULL, ",");
  zpd = atoi(strtokIndx); // z pulse delay
}

//===============================================================

void showParsedData() {
  Serial.print("motors told to move: ");
  delay(4);
  Serial.println(xmotor_py);
  delay(4);
  Serial.println(ymotor_py);
  delay(4);
  Serial.println(zmotor_py);
  delay(4);
  Serial.print("X Steps ");
  delay(4);
  LL_to_Serial(xsteps_py);
  Serial.println();
  Serial.println();

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
      }
    }

    else if (rc == startMarker) {
      recvInProgress = true;
    }
  }
}

//===============================================================
