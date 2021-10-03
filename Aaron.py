#!/usr/bin/env python
from ants import *

# define a class with a do_turn method
# the Ants.run method will parse and update bot input
# it will also run the do_turn method for us


class MyBot:
    def __init__(self):
        # define class level variables, will be remembered between turns
        pass

    # do_setup is run once at the start of the game
    # after the bot has received the game settings
    # the ants class is created and setup by the Ants.run method
    def do_setup(self, ants):
        # initialize data structures after learning the game settings
        self.unseen = []
        self.hills = []
        for row in range(ants.rows):
            for col in range(ants.cols):
                self.unseen.append((row, col))

    # do turn is run once per turn
    # the ants class has the game state and is updated by the Ants.run method
    # it also has several helper methods to use
    def do_turn(self, ants):
        orders = {}  # Dictionary of all orders issued
        targets = {}  # Dictioanary of all food targets

        def do_move_direction(loc, direction):
            new_loc = ants.destination(loc, direction)
            if (ants.unoccupied(new_loc) and new_loc not in orders):
                ants.issue_order((loc, direction))
                orders[new_loc] = loc
                return True
            else:
                return False

        def do_move_location(loc, dest):
            directions = ants.direction(loc, dest)
            for direction in directions:
                if do_move_direction(loc, direction):
                    targets[dest] = loc
                    return True
            return False

        # loop through all my ants and try to give them orders
        # the ant_loc is an ant location tuple in (row, col) form
        for ant_loc in ants.my_ants():
            # try all directions in given order
            directions = ('n', 'e', 's', 'w')
            for direction in directions:

                for hill_loc in ants.my_hills():
                    orders[hill_loc] = None

                # find close food
                ant_dist = []
                for food_loc in ants.food():
                    for ant_loc in ants.my_ants():
                        dist = ants.distance(ant_loc, food_loc)
                        ant_dist.append((dist, ant_loc, food_loc))
                ant_dist.sort()
                for dist, ant_loc, food_loc in ant_dist:
                    if food_loc not in targets and ant_loc not in targets.values():
                        do_move_location(ant_loc, food_loc)

            # unblock own hill
                for hill_loc in ants.my_hills():
                    if hill_loc in ants.my_ants() and hill_loc not in orders.values():
                        for direction in ('s', 'e', 'w', 'n'):
                            if do_move_direction(hill_loc, direction):
                                break
            # check if we still have time left to calculate more orders
            if ants.time_remaining() < 10:
                break


if __name__ == '__main__':
    # psyco will speed up python a little, but is not needed
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass

    try:
        # if run is passed a class with a do_turn method, it will do the work
        # this is not needed, in which case you will need to write your own
        # parsing function and your own game state class
        Ants.run(MyBot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')f