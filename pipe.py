import random
import arcade
from config import *


class Pipe(arcade.Sprite):
    # ############################################################################
    # Description:          The constructor takes in a bunch of other parameters
    #                       as it inherets from an arcade sprite object.  Only
    #                       real important one is init_x_pos
    # ############################################################################
    def __init__(self, filename=DEFAULT_WALL_TEXTURE, scale=1,
                 image_x=0, image_y=0, image_width=0, image_height=0,
                 center_x=0, center_y=0, repeat_count_x=1, repeat_count_y=1,
                 orientation=UPPER, offset_y_coord=0, init_x_pos=WALL_STARTING_X):
        super().__init__(filename=filename, scale=scale, image_x=image_x, image_y=image_y, image_width=image_width,
                         image_height=image_height, center_x=center_x, center_y=center_y, repeat_count_x=repeat_count_x,
                         repeat_count_y=repeat_count_y)

        # If its an upper pipe, flip and shift upward.
        if orientation == UPPER:
            self.angle = 180
            self.position = [init_x_pos, 525 + offset_y_coord]
        else:
            self.position = [init_x_pos, 75 + offset_y_coord]

        # Some helpful variables for our pipe
        self.delete = False
        self.disabled = False
        self.scored = False

    # ############################################################################
    # Description:          Update method for an individual wall moves the x position.
    # ############################################################################
    def update(self, delta_time=0):

        # Disable the wall if position is less than birds
        if self.position[0] < BIRD_X_POSITION:
            self.disabled = True

        # Set the wall to be deleted if out of bounds
        if self.position[0] < -50:
            self.delete = True
        # Otherwise we can move the wall.
        else:
            self.center_x += WALL_SPEED * delta_time

    # ############################################################################
    # Description:          A static method to generate two seperate pipes,
    #                       an upper and a lower.
    # ############################################################################
    @staticmethod
    def generate_pipes(starting_x):
        y_offset = random.randint(-80, 80)
        left = Pipe(offset_y_coord=y_offset,
                    orientation=UPPER, init_x_pos=starting_x)
        right = Pipe(offset_y_coord=y_offset,
                     orientation=LOWER, init_x_pos=starting_x)
        return [left, right]
