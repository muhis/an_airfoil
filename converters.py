def wing_from_lednicer(data):
    middle_point = int((len(data) - 1) / 2) + 1
    # End of file.
    eof = len(data) - 1
    x = []
    y_positive = []
    y_negative = []
    # Get the first half of the file, starting from 3 row until the middle point
    for row in data[3:middle_point]:
        try:
            # First item of the row is the x point, the second is the positive y point.
            x.append(float(row.split()[0]))
            y_positive.append(float(row.split()[1]))
        except ValueError:
            pass
    # Get the second half of the file to get the negative y points.
    for row in data[(middle_point + 1):eof]:
        try:
            y_negative.append(float(row.split()[1]))
        except ValueError:
            pass
    return Wings(description = data[0], x_points = x, y_positive = y_positive, y_negative = y_negative)

def wing_from_selig(data):
    middle_point = int((len(data) - 1) / 2)
    # End of file
    eof = len(data) - 1
    x = []
    y_positive = []
    y_negative = []
    # Flipping coordinations, selig coordinates descends.
    flipped_first_half = data[middle_point::-1]
    for row in flipped_first_half[:-1]:
        try:
            x.append(float(row.split()[0]))
            y_positive.append(float(row.split()[1]))
        except ValueError:
            pass
    for row in data[middle_point:eof]:
        try:
            y_negative.append(float(row.split()[1]))
        except ValueError:
            pass
    return Wings(description = data[0], x_points = x, y_positive = y_positive, y_negative = y_negative)

def wing_from_data(input_data):
    # Variable is not empty
    if input_data:
        # determine file format: selig or Lednicer
        third_line = input_data[2]
        first_word_fourth_line = input_data[3].split()[0]
        if not(third_line):
            # The dat format is Lednicer.
            return lednicer_to_wing (input_data)
        else:
            # The dat format is selig.
            return selig_to_wing(input_data)
