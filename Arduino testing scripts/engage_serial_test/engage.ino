void engage_z() {

  // set z direction to move up
  //digitalWrite(ZdirPin, LOW); // up (in terms of BP)

  // reset variable indicating if theres been contact with end effector
  //contact = false;

  // loop over each step
  for (long long z = 0; z < zsteps_py; z++) {

    // keep track of steps moved by base plate
    bpSteps++;     
  } // stepping loop

  Serial.println(bpSteps);

} // engage z
