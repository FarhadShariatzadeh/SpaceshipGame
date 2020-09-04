from flying_object import FlyingObject


class LaserBeam(FlyingObject):
    """A single laser torpedo"""
    def __init__(self, SPACE, x, y, x_vel, y_vel):
        self.frame_number = 100
        self.LASER_SPEED_FACTOR = 5
        self.SPACE = SPACE
        self.rotation = 0.0
        self.radius = 2.5
        self.diam = self.radius*2
        self.x_vel = x_vel * self.LASER_SPEED_FACTOR
        self.y_vel = y_vel * self.LASER_SPEED_FACTOR
        self.x = x + x_vel
        self.y = y + y_vel
        self.counter = self.frame_number
        self.lifespan = True

    def draw_me(self):
        if self.counter <= 0:
            self.lifespan = Fals

        FILL_COLOR = 1
        fill(FILL_COLOR)
        noStroke()
        ellipse(0, 0, self.diam, self.diam)
        self.counter -= 1
