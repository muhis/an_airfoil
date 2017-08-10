from models import AirFoil


def equate(first_air_foil, second_air_foil):
    """Take two airfoil objects and interpolate both of them."""
    # Take copy of the x_coordinates before the change.
    first_airfoil_copy = first_air_foil.x_coordinates[:]
    second_air_foil_copy = second_air_foil.x_coordinates[:]
    first_air_foil.interpolate(second_air_foil_copy)
    second_air_foil.interpolate(first_airfoil_copy)
