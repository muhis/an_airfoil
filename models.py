from scipy.interpolate import interp1d
class Wings():

    def __init__(self, description, x_points, y_positive, y_negative):
        self.x_points = x_points
        self.y_positive = y_positive
        self.y_negative = y_negative
        self.description = description

    def __len__(self):
        return len(self.x_points)

    def interpolate(self,index, x_point):
        f_positive = interp1d(self.x_points, self.y_positive, kind = 'cubic')
        f_negative = interp1d(self.x_points, self.y_negative, kind = 'cubic')
        self.x_points.insert(index, x_point)
        self.y_positive.insert(index, float(f_positive(x_point)))
        self.y_negative.insert(index, float(f_negative(x_point)))
