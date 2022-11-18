void new_point() {

  // set z direction to move BP down
  strcpy(zdir_py, "d");

  // move BP down
  move_z();

  // move to new X&Y point
  move_x();
  move_y();

  // set z direction to move BP up
  strcpy(zdir_py, "u");

  // move BP up to engage with new point
  engage_z();
}

void engage_z() {

  // set z direction to move up
  digitalWrite(ZdirPin, LOW); // up (in terms of BP)

  // reset variable indicating if theres been contact with end effector & bp steps
  contact = false;
  bpSteps = 0; 

  // loop over each step
  for (long long z = 0; z < zsteps_py; z++) {

    // check if the pentiometer says its pressing far enough
    readPentPin();

    // break out the stepping loop if the pentiometer says force is good
    if (ifcondtionismetbreak(contact)) {
      // return base plate steps to python
      Serial.println(bpSteps);
      break;
    }

    // make pulses to turn motor
    digitalWrite(ZstepPin, HIGH);
    delayMicroseconds(zpd);
    digitalWrite(ZstepPin, LOW);
    delayMicroseconds(zpd);

    // keep track of steps moved by base plate
    bpSteps++;
  }

}
