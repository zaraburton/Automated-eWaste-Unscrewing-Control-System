void readButtonY() {
  yButtonPressed = false;

  if (digitalRead(yButtonPin) == HIGH) {
    yButtonPressed = true;
    yFbPos = 'z'; ;
  }
}

void readButtonX() {
  xButtonPressed = false;

  if (digitalRead(xButtonPin) == HIGH) {
    xButtonPressed = true;
  }
}

bool ifcondtionismetbreak(bool p) {
  if (p == true)
    return true;
  return false;
}
void readButtonZ() {
  zButtonPressed = false;

  if (digitalRead(zButtonPin) == HIGH) {
    zButtonPressed = true;
    zFbPos = 'z';
  }
}

void readPentPin() {

  if (digitalRead(pentInPin) == HIGH) {
    contact = true;
  }
}
