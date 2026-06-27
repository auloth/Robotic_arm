#include <Servo.h>
#include <string.h>
#include <stdlib.h>
#include "ara.h"

Servo base;
Servo shoulder;
Servo elbow;
Servo wrist;
Servo wristrot;
Servo gripper;

int bCur = 90;
int sCur = 90;
int eCur = 90;
int wCur = 90;
int wrCur = 90;
int gCur = 90;

int stepDelay = 10;

void setup() {
  Serial.begin(9600);

  base.attach(7);
  shoulder.attach(8);
  elbow.attach(2);
  wrist.attach(4);
  wristrot.attach(3);
  gripper.attach(6);


  base.write(bCur);
  shoulder.write(sCur);
  elbow.write(eCur);
  wrist.write(wCur);
  wristrot.write(wrCur);
  gripper.write(gCur);

}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    int target[6];
    int index = 0;

    char buffer[64];
    input.toCharArray(buffer, sizeof(buffer));

    char *ptr = strtok(buffer, ",");
    while (ptr != NULL && index < 6) {
      target[index++] = constrain(atoi(ptr), 0, 180);
      ptr = strtok(NULL, ",");
    }

    if (index == 6) {
      moveTo(target);
      Serial.println("OK");
    } else {
      Serial.println("ERR");
    }
  }
}

void moveTo(int target[6]) {

  while (bCur != target[0] ||
         sCur != target[1] ||
         eCur != target[2] ||
         wCur != target[3] ||
         wrCur != target[4] ||
         gCur != target[5]) {

    if (bCur < target[0]) bCur++;
    else if (bCur > target[0]) bCur--;
    base.write(bCur);

    if (sCur < target[1]) sCur++;
    else if (sCur > target[1]) sCur--;
    shoulder.write(sCur);

    if (eCur < target[2]) eCur++;
    else if (eCur > target[2]) eCur--;
    elbow.write(eCur);

    if (wCur < target[3]) wCur++;
    else if (wCur > target[3]) wCur--;
    wrist.write(wCur);

    if (wrCur < target[4]) wrCur++;
    else if (wrCur > target[4]) wrCur--;
    wristrot.write(wrCur);

    if (gCur < target[5]) gCur++;
    else if (gCur > target[5]) gCur--;
    gripper.write(gCur);

    delay(stepDelay);
  }
}