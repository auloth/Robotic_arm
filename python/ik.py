from dataclasses import dataclass
import math

@dataclass
class Motors:
    shoulder: float = 90.0
    elbow: float = 90.0

def constrain(value: float, low: float, high: float) -> float:
    return max(low, min(value, high))

def ik(x: float, y: float) -> Motors:

    l1 = 130.0
    l2 = 115.0

    shoulder_offset = 83
    elbow_offset = 96

    # Distance to target
    d = math.sqrt(x*x + y*y)
    d = max(min(d, l1 + l2), abs(l1 - l2))

    # Law of cosines
    cos_elbow = (l1*l1 + l2*l2 - d*d) / (2.0 * l1 * l2)
    cos_elbow = constrain(cos_elbow, -1.0, 1.0)

    internal_angle = math.acos(cos_elbow)
    bend = math.pi - internal_angle

    # Choose elbow direction based on X
    if x < 0:
        elbow_rad = bend    # target on left side → elbow up
    else:
        elbow_rad = -bend   # target on right side → elbow down

    # Compute shoulder for chosen elbow
    k1 = l1 + l2 * math.cos(elbow_rad)
    k2 = l2 * math.sin(elbow_rad)
    shoulder_rad = math.atan2(y, x) - math.atan2(k2, k1)

    # Wrap shoulder to 0..pi to avoid flips
    while shoulder_rad < 0:
        shoulder_rad += math.pi
    while shoulder_rad > math.pi:
        shoulder_rad -= math.pi

    shoulder_deg = math.degrees(shoulder_rad)
    elbow_deg = math.degrees(elbow_rad)

    # Convert to servo values
    servo_shoulder = shoulder_offset - (shoulder_deg - 90.0)
    servo_elbow = elbow_offset - elbow_deg

    return Motors(
        constrain(servo_shoulder, 0.0, 180.0),
        constrain(servo_elbow, 0.0, 180.0),
    )

# Example usage
if __name__ == "__main__":
    test_positions = [(-50, 50), (50, 50), (-20, -10), (20, -10)]
    for x, y in test_positions:
        m = ik(x, y)
        print(f"x={x}, y={y} → Shoulder: {m.shoulder:.2f}, Elbow: {m.elbow:.2f}")