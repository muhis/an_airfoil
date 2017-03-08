class Wings():

    def __init__(self, description, x_points, y_positive, y_negative):
        self.x_points = x_points
        self.y_positive = y_positive
        self.y_negative = y_negative
        self.description = description

    def __len__(self):
        return len(self.x_points)
