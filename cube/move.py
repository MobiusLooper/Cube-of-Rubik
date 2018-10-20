class Move():
    def __init__(self, axis, level, rotation):
        self.axis = axis
        self.level = level
        self.rotation = rotation

    def invert(self):
        return Move(self.axis, self.level, 1 - self.rotation)