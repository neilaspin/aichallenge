# This is a useful module to import, as it provides some nice functionality. Keep in mind that the core algorithm of a problem should still be written by you for an assessment.
from ants import *
from random import randint


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
        pass

    # do turn is run once per turn
    # the ants class has the game state and is updated by the Ants.run method
    # it also has several helper methods to use
    # Up to here this is pretty much just the template you started with.
    def do_turn(self, ants):
        # track all moves, prevent collisions
        orders = {}

        # targetedFoodLocations = set()
        # This is a piece of code that tries to give a move order to an ant, but checks if the move not leading to any collisions.
        def do_move_direction(loc, direction):
            new_loc = ants.destination(loc, direction)
            if (ants.unoccupied(new_loc) and new_loc not in orders):
                ants.issue_order((loc, direction))
                orders[new_loc] = loc
                return True
            else:
                return False

        # This is a function that gets called after the A* has found the food.
        # It uses a dictionary of loccations and the locations that led to them, i.e their parents to go up the tree.
        # parentsMap has a location a key, adn then returns the parent location as data.
        # The function gets called with a start location, which was the locatin that the A* algorithm found its target and terminated.
        # It then uses the while loop to go up the tree, using second step as the child node and then current node as the parent node.
        # Once it reaches the original location, it then returns the direction an ant would have to go to the current node.
        def getDirectionFromResults(locationAndParentsMap, startLocation):
            secondStep = startLocation
            currNode = locationAndParentsMap[0]
            parentsMap = locationAndParentsMap[1]
            while currNode in parentsMap:
                secondStep = currNode
                currNode = parentsMap.get(currNode)
            return ants.direction(startLocation, secondStep)[0]

        # this actually implement the BFS algorithm, in a relatively compact fashion.
        def BFS(startLocation):
            # this varialbe initializes a dictionary that stores the parents of each location, i.e. the location that lead to the current location
            parents = {}
            # this is the core queue that runs the BFS algorithm, at the beginning you add the starting node.
            queue = [startLocation]
            # This is a set used to check if a location has been visited before. In contrast to what we discussed in the lecture, you can also have set for both the explored nodes and those in the queue, as neither should be readded to the queue.
            # This gets problematic when you later need to check if you should still update a cost function for something in the queue, and you need to know if something has already been expanded, but for BFS this is not strictly needed.
            visited = {startLocation}
            while queue:
                # This was added to stop the BFS from growing too much if it finds no solution - I will discuss some alternatives in the follow up comments, but this will work.
                # It is important to consider failure condidtions, such as taking to long, for an algorithm, and then have code to deal with it.
                if len(queue) > 50:
                    return None
                # this returns the first item in the queue to expand it.
                currLoc = queue.pop(0)
                # If the node to expand is a food location the algorithm is done. Here the problem evaluation only happens when the node gets expanded, which is fine, but it would be faster to do this when nodes are added to the queue.
                if (currLoc in ants.food()):
                    # the BFS implementation here returns the final location if found the food, and a dictionary that contains locations and the locations leading to them, i.e. the locations of the parent nodes.
                    # This then requires some postprocessing, done by the function above, to extract the first move. This postprocessing is basically the backtracking in the graph.
                    return (currLoc, parents)
                # If the current node is not a food location it gets expanded, there are four possible action the ant can take.
                for direction in ('n', 'e', 's', 'w'):
                    # this uses a function form the ants module to generate locations based on the current location and a direction, which is done once for each action.
                    new_loc = ants.destination(currLoc, direction)
                    # this line check if the actions are applicable, i.e. it checks that they do not lead to an already visited location, nor to an impassable tile, like a wall.
                    if (new_loc not in visited) and (ants.passable(new_loc)):
                        # if resulting locations are applicable, three things will happen: the new location will be marked as visited, by adding it to the visited set
                        visited.add(new_loc)
                        # the dictionary that tracks the parents also gets updated
                        parents[new_loc] = currLoc
                        # and then they get added to the queue, in the end.
                        queue.append(new_loc)
            # if the queue becomes empty wihtout finding a food location, then we have another failure case, and return none.
            return None

        # the BFS search is run for every ant, each trying to go to the nearest food location.
        for ant_loc in ants.my_ants():
            # this ensures that there is enough time left, otherwise it breaks out of the loop using BFS.
            if ants.time_remaining() < 10:
                break
            # this calls BFS for every ant, ... the BFS here is hardcoded to look for a path to food locations. You could also, alternatively give it a set of goal locations.
            bfsResult = BFS(ant_loc)
            # If the BFS found something, you can then use the parent dictionary to get a direction and add that direction as order.
            if bfsResult is not None:
                direction = getDirectionFromResults(bfsResult, ant_loc)
                if do_move_direction(ant_loc, direction):
                    continue
                # this is the fallback behaviour generation, ... if an ant is not moving to the closest food, it will move randomly.
            directions = ('w', 'n', 's', 'e')
            i = 0
            while True:
                if do_move_direction(ant_loc, directions[randint(0, 3)]) or i > 5:
                    break
                i = i + 1

            # past here we are jsut looking at code from the template:


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
        print('ctrl-c, leaving ...')
