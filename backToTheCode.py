import sys
import random
import operator


class Directions:
    NW, N, NE, W, E, SW, S, SE = range(8)


def get_random_direction():
    return random.randint(0, 7)


# the arena
m = [['.' for i in range(35)] for j in range(20)]

# the arenas at evey round of the game (BackInTime)
# key is the step number, value is the arena
bit = {}

# how many opponents
opponent_count = int(raw_input())

# next destinations
destinations = [(0, 0)]
current_dest = 0

# feel the corner
feel_the_corner = 3


def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def is_area_free(x1, y1, step1, step2):
    if step2 is None:
        x2 = step1[0]
        y2 = step1[1]
    else:
        x1 = step1[0]
        y1 = step1[1]
        x2 = step2[0]
        y2 = step2[1]

    if x1 == x2 and y1 == y2:
        return m[y1][x1] != '.'

    print >> sys.stderr, "Checking area x1:", x1, " y1:", y1, " x2:", x2, " y2:", y2
    step_x = +1 if x1 < x2 else -1
    step_y = +1 if y1 < y2 else -1

    for x in range(x1, x2, step_x):
        for y in range(y1, y2, step_y):
            print >> sys.stderr, "Area free. Checking x:", x, " y:", y
            if m[y][x] != '.':
                print >> sys.stderr, "Area not free. x:", x, " y:", y, " m:", m[y][x]
                return False

    print >> sys.stderr, "Area x1:", x1, " y1:", y1, " x2:", x2, " y2:", y2, " is free."
    return True


def get_closest_opponent(opps, x, y):
    min_dist = 99999
    closest_opponent = None
    for opp in opps:
        distance = manhattan_distance(x, y, opp[0], opp[1])
        if distance < min_dist:
            closest_opponent = opp
            min_dist = distance
            print >> sys.stderr, "Min distance: ", min_dist, " closest: ", closest_opponent

    return closest_opponent, distance


def is_out_of_bounds(x, y):
    return y < 0 or y > 19 or x < 0 or x > 34


def move_to_direction(x, y, direction):
    if direction == Directions.N:
        y -= 1

    elif direction == Directions.NE:
        y -= 1
        x += 1

    elif direction == Directions.E:
        x += 1

    elif direction == Directions.SE:
        x += 1
        y += 1

    elif direction == Directions.S:
        y += 1

    elif direction == Directions.SW:
        y += 1
        x -= 1

    elif direction == Directions.W:
        x -= 1

    elif direction == Directions.NW:
        x -= 1
        y -= 1

    print >> sys.stderr, "Moving to direction ", direction, " given x:", x, " y:", y
    if is_out_of_bounds(x, y):
        return None, None

    return x, y


def get_coordinates_from_direction(x, y, direction, size):
    half_size = size / 2
    step1 = []
    step2 = None
    print >> sys.stderr, "Getting coords for direction: ", direction

    if direction == Directions.N:
        step1 = (min(34, x + half_size), max(0, y - size))
        step2 = (max(0, x - half_size), y)

    elif direction == Directions.NE:
        step1 = (min(34, x + size), max(0, y - size))

    elif direction == Directions.E:
        step1 = (min(34, x + size), max(0, y - half_size))
        step2 = (x, min(19, y + half_size))

    elif direction == Directions.SE:
        step1 = (min(34, x + size), min(19, y + size))

    elif direction == Directions.S:
        step1 = (min(34, x + half_size), min(19, y + size))
        step2 = (max(0, x - half_size), y)

    elif direction == Directions.SW:
        step1 = (max(0, x - size), min(19, y + size))

    elif direction == Directions.W:
        step1 = (max(0, x - size), min(19, y + half_size))
        step2 = (x, max(0, y - half_size))

    elif direction == Directions.NW:
        step1 = (max(0, x - size), max(0, y - size))

    print >> sys.stderr, "step1: " + str(step1) + " step2: " + str(step2)
    return step1, step2


def get_most_free_area_coords(x, y):
    areas = {}
    for i in range(4):
        for j in range(7):
            occupied_cells = 0
            for k in range(5):
                for l in range(5):
                    # print >> sys.stderr, "(", (i * 5 + k), "," , (j * 5 + l), ")"
                    if m[i * 5 + k][j * 5 + l] != '.':
                        occupied_cells += 1
            areas[(i, j)] = occupied_cells
            print >> sys.stderr, "areas(", i, ",", j, "):", occupied_cells

    # searches the areas with less occupied cells
    area_density = 999
    for k in areas.keys():
        print >> sys.stderr, "area(", k, ") = ", areas[k]
        if areas[k] < area_density:
            area_density = areas[k]

    # gets the closest of these areas
    min_distance = 999
    index = 0
    myx = x % 5
    myy = y % 5
    for k in areas.keys():
        if areas[k] == area_density:
            distance = abs(myx - k[0]) + abs(myy - k[1])
            if min_distance > distance:
                min_distance = distance
                index = k

    print >> sys.stderr, "going to area ", index
    return index[1] * 5 + 2, index[0] * 5 + 2


def get_best_direction(x, y, ox, oy):
    """
    returns the best Direction to go to, given the player coords (x, y)
    and the opponent coords (ox, oy)
    """
    direction = None

    # straight direction threshold (for going N,E,S,W instead of NE,SE,SW,NW)
    threshold = 5

    if x - threshold > ox > x + threshold and y < oy:
        direction = Directions.N

    elif x - threshold > ox > x + threshold and y >= oy:
        direction = Directions.S

    elif x >= ox and y - threshold > oy > y + threshold:
        direction = Directions.W

    elif x < ox and y - threshold > oy > y + threshold:
        direction = Directions.E

    elif ox >= x and oy < y:
        direction = Directions.SW

    elif ox < x and oy <= y:
        direction = Directions.SE

    elif ox >= x and oy > y:
        direction = Directions.NW

    elif ox < x and oy >= y:
        direction = Directions.NE

    # if player and opponent share the same position
    else:
        direction = get_random_direction()

    if direction is None:
        print >> sys.stderr, "NO DIRECTION FOUND. x:" + str(x) + " y:" + str(y) + " ox:" + str(ox) + " oy:" + str(oy)

    print >> sys.stderr, "Best direction is ", direction
    return direction


def get_escape_direction_from_edge(x, y):
    direction = None
    if x <= feel_the_corner and y <= feel_the_corner:
        direction = Directions.SE

    elif x <= feel_the_corner and y > 19 - feel_the_corner:
        direction = Directions.NE

    elif x > 34 - feel_the_corner and y <= feel_the_corner:
        direction = Directions.SW

    elif x > 34 - feel_the_corner and y > 19 - feel_the_corner:
        direction = Directions.NW

    elif x <= feel_the_corner:
        direction = Directions.E

    elif x > 34 - feel_the_corner:
        direction = Directions.W

    elif y <= feel_the_corner:
        direction = Directions.S

    elif y > 19 - feel_the_corner:
        direction = Directions.N

    if direction is None:
        print >> sys.stderr, "NO DIRECTION FOUND for escaping. x:" + str(x) + " y:" + str(y)

    return direction


def find_new_area(x, y, closest_opponent, size, destinations):
    # TODO quando piu' di meta' dell'arena e' occupata, non cerco piu' di stare lontano degli avversari, ma mi butto sulle tracce libere

    ox = closest_opponent[0]
    oy = closest_opponent[1]
    escaping = False

    # if I'm near to an edge, 
    if x <= feel_the_corner or x > 34 - feel_the_corner \
            or y <= feel_the_corner or y > 19 - feel_the_corner:
        escaping = True
        direction = get_escape_direction_from_edge(x, y)

    while True:

        # TODO fix on the edge
        # if we're on the edge, we just go for a straight line
        #        if x == 0 or x == 34 or y == 0 or y == 19:
        #            destinations.append(step1)

        # if we're not close to an edge, gets the new coordinates where to go
        if not escaping:
            direction = get_best_direction(x, y, ox, oy)

        step1, step2 = get_coordinates_from_direction(x, y, direction, size)

        # if the new area is free, it's ok
        if is_area_free(x, y, step1, step2):
            break

        # if it's not good, we try to make a smaller square
        size -= 1

        # if there's no room, even with smaller squares
        if size == 2:

            # we retry going away, starting with a normal square
            size = 5

            # we'll go away
            while True:
                x, y = move_to_direction(x, y, direction)
                if x is None:
                    step1 = get_most_free_area_coords(x, y)
                    return append_destinations(step1, None, (x, y), destinations)
                else:
                    step1, step2 = get_coordinates_from_direction(x, y, direction, size)
                    if is_area_free(x, y, step1, step2):
                        return append_destinations(step1, step2, (x, y), destinations)

        print >> sys.stderr, "Area (", x, ",", y, ") - ", step1, " - ", step2, " is not free. Reducing size to ", size

    return append_destinations(step1, step2, (x, y), destinations)


def append_destinations(step1, step2, step3, destinations):
    destinations.append(step1)
    if step2 is not None:
        destinations.append(step2)
    destinations.append(step3)
    print >> sys.stderr, "updated destinations: " + str(destinations)
    return destinations


def next_dests(x, y, opps, destinations):
    # gets the closest opponent
    closest_opponent, distance = get_closest_opponent(opps, x, y)

    # se ci sono due opps alla stessa distanza, prendo un random


    size = distance / 4
    return find_new_area(x, y, closest_opponent, size, destinations)


# main game loop
while 1:

    game_round = int(raw_input())
    px, py, back_in_time_left = [int(i) for i in raw_input().split()]
    opponents = []
    for i in xrange(opponent_count):
        opponents.append([int(j) for j in raw_input().split()])

    # if I detect a BIT of another user, randomly move something

    # dopo che definisco un obiettivo, poi controllo le distanze ed eventualmente lo 
    # allargo un po', in funzione di quanti si sono allontanati gli opponents

    # quando rimangono poche celle libere, vado diretto su quelle

    # reads the actual state of the arena
    for i in xrange(20):
        row = raw_input()
        for j in range(34):
            m[i][j] = row[j]

    grid = ''
    for i in xrange(20):
        for j in range(34):
            grid += m[i][j]
        grid += '\n'
    print >> sys.stderr, grid

    # updates the BIT
    bit[game_round] = [row[:] for row in m]

    # if is the first round, or we reached our destination
    if game_round == 1 or (px == destinations[current_dest][0] and py == destinations[current_dest][1]):
        current_dest += 1
        if len(destinations) == current_dest:
            destinations = next_dests(px, py, opponents, destinations)

    # outputs our next destination
    print str(destinations[current_dest][0]) + " " + str(destinations[current_dest][1])