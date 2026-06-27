#ifndef ARA_H
#define ARA_H

struct motors {
  int base;
  int shoulder;
  int elbow;
  int wrist;
  int wristrot;
  int gripper;
};

motors ik(double x, double y, double z, double toolAngleDeg);

#endif