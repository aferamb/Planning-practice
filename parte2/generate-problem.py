#!/usr/bin/env python3

# Examples:
# Exercise 2.1
# python3 generate-problem.py -d 1 -r 1 -l 4 -p 4 -c 6 -g 4 -a 4 --exercise 1
#
# Exercise 2.2
# python3 generate-problem.py -d 1 -r 1 -l 4 -p 4 -c 6 -g 4 -a 4 --exercise 2

# Run (examples): 
# planutils run metric-ff -- dronedomain2.pddl drone_problem_ex2_d1_r1_l4_p4_c6_g4_a4.pddl
# planutils run downward -- --alias lama-first dronedomain2.pddl drone_problem_ex2_d1_r1_l4_p4_c6_g4_a4.pddl

from optparse import OptionParser
import random
import math
import sys

content_types = ["food", "medicine"]


def distance(location_coords, location_num1, location_num2):
    x1 = location_coords[location_num1][0]
    y1 = location_coords[location_num1][1]
    x2 = location_coords[location_num2][0]
    y2 = location_coords[location_num2][1]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def flight_cost(location_coords, location_num1, location_num2):
    return int(distance(location_coords, location_num1, location_num2)) + 1


def setup_content_types(options):
    while True:
        num_crates_with_contents = []
        crates_left = options.crates

        for x in range(len(content_types) - 1):
            types_after_this = len(content_types) - x - 1
            max_now = crates_left - types_after_this
            num = random.randint(1, max_now)
            num_crates_with_contents.append(num)
            crates_left -= num

        num_crates_with_contents.append(crates_left)

        maxgoals = sum(min(num_crates, options.persons) for num_crates in num_crates_with_contents)

        if options.goals <= maxgoals:
            break

    crates_with_contents = []
    counter = 1

    for x in range(len(content_types)):
        crates = []
        for y in range(num_crates_with_contents[x]):
            crates.append("crate" + str(counter))
            counter += 1
        crates_with_contents.append(crates)

    return crates_with_contents


def setup_location_coords(options):
    location_coords = [(0, 0)]  # depot
    for _ in range(1, options.locations + 1):
        location_coords.append((random.randint(1, 200), random.randint(1, 200)))
    return location_coords


def setup_person_needs(options, crates_with_contents):
    need = [[False for _ in range(len(content_types))] for _ in range(options.persons)]
    goals_per_contents = [0 for _ in range(len(content_types))]

    for _ in range(options.goals):
        generated = False
        while not generated:
            rand_person = random.randint(0, options.persons - 1)
            rand_content = random.randint(0, len(content_types) - 1)

            if (goals_per_contents[rand_content] < len(crates_with_contents[rand_content])
                    and not need[rand_person][rand_content]):
                need[rand_person][rand_content] = True
                goals_per_contents[rand_content] += 1
                generated = True

    return need


def main():
    parser = OptionParser(usage='python generate-problem.py [-help] options...')
    parser.add_option('-d', '--drones', metavar='NUM', dest='drones', action='store', type=int,
                      help='the number of drones')
    parser.add_option('-r', '--carriers', metavar='NUM', type=int, dest='carriers',
                      help='the number of carriers')
    parser.add_option('-l', '--locations', metavar='NUM', type=int, dest='locations',
                      help='the number of locations apart from the depot')
    parser.add_option('-p', '--persons', metavar='NUM', type=int, dest='persons',
                      help='the number of persons')
    parser.add_option('-c', '--crates', metavar='NUM', type=int, dest='crates',
                      help='the number of crates available')
    parser.add_option('-g', '--goals', metavar='NUM', type=int, dest='goals',
                      help='the number of goal assignments')
    parser.add_option('-a', '--carrier-capacity', metavar='NUM', type=int, dest='carrier_capacity',
                      default=4, help='carrier capacity')
    parser.add_option('-e', '--exercise', metavar='NUM', type=int, dest='exercise',
                      default=1, help='part 2 exercise: 1 or 2')
    parser.add_option('-s', '--seed', metavar='NUM', type=int, dest='seed',
                      default=None, help='random seed')

    (options, args) = parser.parse_args()

    if options.seed is not None:
        random.seed(options.seed)

    if options.drones is None:
        print("You must specify --drones")
        sys.exit(1)

    if options.carriers is None:
        print("You must specify --carriers")
        sys.exit(1)

    if options.locations is None:
        print("You must specify --locations")
        sys.exit(1)

    if options.persons is None:
        print("You must specify --persons")
        sys.exit(1)

    if options.crates is None:
        print("You must specify --crates")
        sys.exit(1)

    if options.goals is None:
        print("You must specify --goals")
        sys.exit(1)

    if options.goals > options.crates:
        print("Cannot have more goals than crates")
        sys.exit(1)

    if len(content_types) > options.crates:
        print("Cannot have more content types than crates")
        sys.exit(1)

    if options.goals > len(content_types) * options.persons:
        print("Too many goals for the number of persons and content types")
        sys.exit(1)

    if options.carrier_capacity < 1:
        print("Carrier capacity must be at least 1")
        sys.exit(1)

    if options.exercise not in [1, 2]:
        print("Exercise must be 1 or 2")
        sys.exit(1)

    if options.exercise == 1:
        domain_name = "ubermedics-carriers"
    else:
        domain_name = "ubermedics-carriers-costs"

    drone = []
    person = []
    crate = []
    carrier = []
    location = []
    nums = []

    location.append("depot")

    for x in range(options.locations):
        location.append("loc" + str(x + 1))

    for x in range(options.drones):
        drone.append("drone" + str(x + 1))

    for x in range(options.carriers):
        carrier.append("carrier" + str(x + 1))

    for x in range(options.persons):
        person.append("person" + str(x + 1))

    for x in range(options.crates):
        crate.append("crate" + str(x + 1))

    for x in range(options.carrier_capacity + 1):
        nums.append("n" + str(x))

    crates_with_contents = setup_content_types(options)
    location_coords = setup_location_coords(options)
    need = setup_person_needs(options, crates_with_contents)

    problem_name = (
        "drone_problem"
        + "_ex" + str(options.exercise)
        + "_d" + str(options.drones)
        + "_r" + str(options.carriers)
        + "_l" + str(options.locations)
        + "_p" + str(options.persons)
        + "_c" + str(options.crates)
        + "_g" + str(options.goals)
        + "_a" + str(options.carrier_capacity)
    )

    if options.seed is not None:
        problem_name += "_s" + str(options.seed)

    with open(problem_name + ".pddl", 'w') as f:
        f.write("(define (problem " + problem_name + ")\n")
        f.write("(:domain " + domain_name + ")\n")

        f.write("(:objects\n")

        for x in drone:
            f.write("\t" + x + " - drone\n")

        for x in location:
            f.write("\t" + x + " - location\n")

        for x in crate:
            f.write("\t" + x + " - crate\n")

        for x in content_types:
            f.write("\t" + x + " - contents\n")

        for x in person:
            f.write("\t" + x + " - person\n")

        for x in carrier:
            f.write("\t" + x + " - carrier\n")

        for x in nums:
            f.write("\t" + x + " - num\n")

        f.write(")\n")

        f.write("(:init\n")

        for x in drone:
            f.write(f"\t(drone-at {x} depot)\n")
            f.write(f"\t(drone-free {x})\n")

        for x in crate:
            f.write(f"\t(crate-at {x} depot)\n")

        for x in carrier:
            f.write(f"\t(carrier-at {x} depot)\n")
            f.write(f"\t(carrier-load {x} n0)\n")

        for i in range(len(nums) - 1):
            f.write(f"\t(next {nums[i]} {nums[i + 1]})\n")

        for i in range(len(content_types)):
            for c in crates_with_contents[i]:
                f.write(f"\t(crate-has {c} {content_types[i]})\n")

        for i in range(len(person)):
            loc = location[random.randint(1, len(location) - 1)]
            f.write(f"\t(person-at {person[i]} {loc})\n")

        if options.exercise == 2:
            f.write("\t(= (total-cost) 0)\n")

            for i in range(len(location)):
                for j in range(len(location)):
                    if i == j:
                        cost = 0
                    else:
                        cost = flight_cost(location_coords, i, j)
                    f.write(f"\t(= (fly-cost {location[i]} {location[j]}) {cost})\n")

        f.write(")\n")

        f.write("(:goal (and\n")
        for x in range(options.persons):
            for y in range(len(content_types)):
                if need[x][y]:
                    f.write(f"\t(person-has {person[x]} {content_types[y]})\n")
        f.write("))\n")

        if options.exercise == 2:
            f.write("(:metric minimize (total-cost))\n")

        f.write(")\n")


if __name__ == '__main__':
    main()