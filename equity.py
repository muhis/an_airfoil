from scipy.interpolate import interp1d
def equate(wing1, wing2):
    if len(wing1) > len(wing2):
        longer_wing = wing1
        shorter_wing = wing2
    else:
        longer_wing = wing2
        shorter_wing = wing1

    for x in longer_wing.x_points:
        if not(x in shorter_wing.x_points):
            x_index = longer_wing.x_points.index(x)
            shorter_wing.interpolate(x_index, x)
