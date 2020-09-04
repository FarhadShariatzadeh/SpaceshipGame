from laserbeam import LaserBeam
from asteroid import Asteroid
from spaceship import Spaceship


class GameController:

    def __init__(self, SPACE, fadeout):
        """Initialize the game controller"""
        self.fadeout = fadeout
        self.SPACE = SPACE

        self.spaceship_hit = False
        self.asteroid_destroyed = False
        self.asteroids = [Asteroid(self.SPACE)]
        self.laser_beams = []
        self.spaceship = Spaceship(self.SPACE)

    def update(self):
        """Updates game state on every frame"""
        # asteroid_blow_up is an boolean that break the
        # for loop in intersection
        self.asteroid_blow_up = False
        self.do_intersections()

        for asteroid in self.asteroids:
            asteroid.display()

        for l in range(len(self.laser_beams)):
            if(self.laser_beams[l].counter > 0):
                self.laser_beams[l].display()

        self.spaceship.display()

        # Carries out necessary actions if game over
        if self.spaceship_hit:
            if self.fadeout <= 0:
                fill(1)
                textSize(30)
                text("YOU HIT AN ASTEROID",
                     self.SPACE['w']/2 - 165, self.SPACE['h']/2)
            else:
                self.fadeout -= 1

        if self.asteroid_destroyed:
            fill(1)
            textSize(30)
            text("YOU DESTROYED THE ASTEROIDS!!!",
                 self.SPACE['w']/2 - 250, self.SPACE['h']/2)

    def fire_laser(self, x, y, rot):
        """Add a laser beam to the game"""
        x_vel = sin(radians(rot))
        y_vel = -cos(radians(rot))
        self.laser_beams.append(
            LaserBeam(self.SPACE, x, y, x_vel, y_vel)
            )

    def handle_keypress(self, key, keycode=None):
        if (key == ' '):
            if self.spaceship.intact:
                self.spaceship.control(' ', self)
        if (keycode):
            if self.spaceship.intact:
                self.spaceship.control(keycode)

    def handle_keyup(self):
        if self.spaceship.intact:
            self.spaceship.control('keyup')

    def do_intersections(self):
        ''' determine where asteroids and laser beam itersect!!
        It also determine the intersect btw asteroids and spaceship'''

        for j in range(len(self.asteroids)):
            if self.asteroid_blow_up:
                break
            for i in range(len(self.laser_beams)):
                if (
                        abs(self.asteroids[j].x - self.laser_beams[i].x)
                        < max(self.laser_beams[i].radius, self.asteroids[j].
                              radius)
                        and
                        abs(self.asteroids[j].y - self.laser_beams[i].y)
                        < max(self.laser_beams[i].radius, self.asteroids[j].
                              radius)):
                    self.blow_up_asteroid(i, j)
                    self.laser_beams[i].lifespan = False
                    self.laser_beams.remove(self.laser_beams[i])
                    if self.asteroid_blow_up:
                        break

        # If the space ship still hasn't been blown up
        if self.spaceship.intact:
            # Check each asteroid for intersection
            for i in range(len(self.asteroids)):

                if (
                        abs(self.spaceship.x - self.asteroids[i].x)
                        < max(self.asteroids[i].radius,
                              self.spaceship.radius)
                        and
                        abs(self.spaceship.y - self.asteroids[i].y)
                        < max(self.asteroids[i].radius,
                              self.spaceship.radius)):

                    # We've intersected an asteroid
                    self.spaceship.blow_up(self.fadeout)
                    self.spaceship_hit = True

    def blow_up_asteroid(self, i, j):
        '''decide what is going happend after asteroid hit by
        laser beam!'''
        if self.asteroids[j].asize == 'Large':
            self.asteroids.append(Asteroid(self.SPACE, 'Med',
                                           self.laser_beams[i].x,
                                           self.laser_beams[i].y,
                                           self.laser_beams[i].x_vel,
                                           - self.laser_beams[i].y_vel,
                                           0, 0.0))
            self.asteroids.append(Asteroid(self.SPACE, 'Med',
                                           self.laser_beams[i].x,
                                           self.laser_beams[i].y,
                                           - self.laser_beams[i].x_vel,
                                           self.laser_beams[i].y_vel,
                                           0, 0.0))

        elif self.asteroids[j].asize == 'Med':
            self.asteroids.append(Asteroid(self.SPACE, 'Small',
                                           self.laser_beams[i].x,
                                           self.laser_beams[i].y,
                                           self.laser_beams[i].x_vel,
                                           - self.laser_beams[i].y_vel,
                                           0, 0.0))
            self.asteroids.append(Asteroid(self.SPACE, 'Small',
                                           self.laser_beams[i].x,
                                           self.laser_beams[i].y,
                                           - self.laser_beams[i].x_vel,
                                           self.laser_beams[i].y_vel, 0,
                                           0.0))
            self.asteroids.append(Asteroid(self.SPACE, 'Small',
                                           self.laser_beams[i].x,
                                           self.laser_beams[i].y,
                                           self.laser_beams[i].x_vel,
                                           self.laser_beams[i].y_vel, 0,
                                           0.0))

        elif self.asteroids[j].asize == 'Small':
            self.asteroids[j].asize = ' '

        self.asteroids.remove(self.asteroids[j])
        self.asteroid_blow_up = True
        if len(self.asteroids) == 0:
            self.asteroid_destroyed = True
