import random
import copy
import math


def distance(a, b):
    # Just a quick implementation of distance between 2 points
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def algo(cones, car):
    # Algorithm for sorting the cones into the correct order
    # both orders include the cone detected closest to the car
    goal = len(cones) + 1
    # distances is used in calculating the cone closest to the car
    distances, order1, order2 = [], [], []
    # order2 is in reverse order, as it is heading backwards from the closest cone to the car
    # a rough idea of what direction the car is going at a given cone, based on the last 2 cones
    heading_f = (1, 0)
    # heading_b is similar, just used for estimating where the car came from
    heading_b = (-1, 0)
    # finding the cone closest to the car at the beginning, this will serve as the start point of further calculations
    for cone in cones:
        distances.append(distance(cone, car))
    closest = cones[distances.index(min(distances))]
    order1.append(closest)
    order2.append(closest)
    cones.remove(closest)
    # main logic behind ordering
    while len(order1) + len(order2) is not goal:
        # forward_finder is a point created by using a linear estimation for where the next cone should be based on the past 2,
        # this helps us find the next cone with more precision
        forward_finder = (order1[-1][0] + heading_f[0], order1[-1][1] + heading_f[1])
        cur_forward = (order1[-1][0], order1[-1][1])
        # backward_finder is similar, just for cones that are potentially behind the previous one
        backward_finder = (order2[-1][0] + heading_b[0], order2[-1][1] + heading_b[1])
        cur_backward = (order2[-1][0], order2[-1][1])
        # distances from the previous cones and estimated positions
        df1, df2, db1, db2 = [], [], [], []
        for cone in cones:
            df1.append(distance(cone, cur_forward))
            df2.append(distance(cone, forward_finder))
            db1.append(distance(cone, cur_backward))
            db2.append(distance(cone, backward_finder))
        # finding nearest cone in front of the order
        if df1.index(min(df1)) == df2.index(min(df2)):
            next_forward = cones[df1.index(min(df1))]
        else:
            # if 2 cones are equidistant from the previous one, we choose the one closer to the estimated location
            next_forward = cones[df2.index(min(df2))]
        df = min(df1)
        # finding nearest cone behind the order
        if db1.index(min(db1)) == db2.index(min(db2)):
            next_backward = cones[db1.index(min(db1))]
        else:
            next_backward = cones[db2.index(min(db2))]
        db = min(db1)
        # similar to prim's algorithm, just with 2 potential new edges each time, we add the cone closer to
        # the front or the end of the ordering, this ensures that when one end of the cone order is reached,
        # the code responsible for expanding that way doesn't go off the rails
        if df < db or min(df2) < min(db2):
            order1.append(next_forward)
            # not a unit vector
            heading_f = (order1[-2][0] - order1[-1][0], order1[-2][1] - order1[-1][1])
            cones.remove(next_forward)
        else:
            order2.append(next_backward)
            heading_b = (order2[-2][0] - order2[-1][0], order2[-2][1] - order2[-1][1])
            cones.remove(next_backward)
    # order2 was reversed, and will be used to output the final order
    order2.reverse()
    for i in range(1, len(order1)):
        order2.append(order1[i])
    return order2


def compare_test(cones, sol):
    # complete way to test
    print(f"Recieved order: {cones}")
    correct = True
    i = 0
    for cone in cones:
        if cone[0] == sol[i][0] and cone[1] == sol[i][1]:
            i += 1
        else:
            correct = False
            break
    return correct


# Setup for the two test cases, including random cone order and car position
t1 = [(-1, 1), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1)]
sol1 = copy.deepcopy(t1)
t2 = [(1, 1), (2, 1), (3.5, 0.5), (4.5, -0.5), (5, -2), (4.5, -3.5), (3.5, -4.5), (2, -5), (1, -5)]
sol2 = copy.deepcopy(t2)
car = (0, 0)
random.shuffle(t1)
random.shuffle(t2)
print(f"Input 1: {t1}")
if compare_test(algo(t1, car), sol1):
    print("Test 1 Passed")
else:
    print("Test 1 Failed")
print(f"Correct solution: {sol1}")
print("\n \n \n")
print(f"Input 2: {t2}")
if compare_test(algo(t2, car), sol2):
    print("Test 2 Passed")
else:
    print("Test 2 Failed")
print(f"Correct solution: {sol2}")
