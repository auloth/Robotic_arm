motors ik(double x, double y)
{
  motors m = {90, 90, 90, 90};

  const double l1 = 130.0;
  const double l2 = 115.0;

  const int SHOULDER_OFFSET = 83;
  const int ELBOW_OFFSET    = 96;

  double d = sqrt(x*x + y*y);

  if (d > (l1 + l2)) d = l1 + l2;
  if (d < fabs(l1 - l2)) d = fabs(l1 - l2);

  double cosElbow = (l1*l1 + l2*l2 - d*d) / (2*l1*l2);
  cosElbow = constrain(cosElbow, -1.0, 1.0);

  double internalAngle = acos(cosElbow);
  double elbowRad = PI - internalAngle;

  double k1 = l1 + l2 * cos(elbowRad);
  double k2 = l2 * sin(elbowRad);

  double shoulderRad = atan2(y, x) - atan2(k2, k1);

  double shoulderDeg = shoulderRad * 180.0 / M_PI;
  double elbowDeg    = elbowRad * 180.0 / M_PI;

  m.shoulder = constrain(SHOULDER_OFFSET - (shoulderDeg - 90.0), 0, 180);
  m.elbow    = constrain(ELBOW_OFFSET - elbowDeg, 0, 180);

  return m;
}