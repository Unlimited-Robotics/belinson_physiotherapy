from raya.enumerations import POSITION_UNIT, ANGLE_UNIT

GARY_FOOTPRINT = [
    [-0.25,  0.35],
    [ 0.25,  0.35],
    [ 0.25, -0.35],
    [-0.25, -0.35]
]

# Belinson, in the storage
NAV_POINT_HOME = {
        'x':        164.0,
        'y':        1680.0,
        'angle':    0.0,
        'pos_unit': POSITION_UNIT.PIXELS,
        'ang_unit': ANGLE_UNIT.DEGREES}

# Distance threshold for the robot to consider its in home location
HOME_THRESHOLD = 1.0

LOCALIZING_TIMEOUT = 30.0