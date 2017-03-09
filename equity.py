from models import Wings
from scipy.interpolate import interp1d
def equate(wing1, wing2):
    if len(wing1) > len(wing2):
        longer_wing = wing1
        shorter_wing = wing2
    else:
        longer_wing = wing2
        shorter_wing = wing1
    shorter_wing_copy = Wings(description = shorter_wing.description[:], x_points = shorter_wing.x_coordinates(),
                                y_positive = shorter_wing.y_coordinates_positive(), y_negative = shorter_wing.y_coordinates_negative(),
                                )
    for x in longer_wing.x_coordinates():
        if not(x in shorter_wing.x_coordinates()):
            shorter_wing.interpolate(x)
    for x in shorter_wing_copy.x_coordinates():
        if not(x in longer_wing.x_coordinates()):
            longer_wing.interpolate(x)
