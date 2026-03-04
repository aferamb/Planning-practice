#!/usr/bin/env python3

########################################################################################
# Problem instance generator for the emergency drones domain (Practica 1 Parte 1).
# Based on the skeleton from Linköping University TDDD48 2021 course.
# https://www.ida.liu.se/~TDDD48/labs/2021/lab1/index.en.shtml
#
# HOW TO RUN:
#   python generate-problem.py -d 1 -r 0 -l 3 -p 3 -c 3 -g 3
#
# PARAMETERS:
#   -d  Number of drones
#   -r  Number of carriers (not used in parte 1, set to 0)
#   -l  Number of locations (not counting the depot)
#   -p  Number of persons
#   -c  Number of crates
#   -g  Number of goal assignments (person needs crate with content)
#
# OUTPUT:
#   A .pddl problem file named after the parameter combination.
########################################################################################


from optparse import OptionParser
import random
import math
import sys

########################################################################################
# Hard-coded options
########################################################################################

# These are the possible content types that crates can contain.
# Both types must appear in every problem (at least one crate per type).
# To add a new content type (e.g., "water"), simply add it here and
# update the domain's goal predicates accordingly — NO domain changes needed.
content_types = ["food", "medicine"]


########################################################################################
# Random seed
########################################################################################

# Uncomment this line for reproducible results during testing:
# random.seed(0)

########################################################################################
# Helper functions
########################################################################################

def distance(location_coords, location_num1, location_num2):
    """
    Computes the Euclidean distance between two locations identified by index.
    Each location has an (x, y) coordinate stored in location_coords.
    This is used internally by flight_cost() for Part 2 of the practice.
    """
    x1 = location_coords[location_num1][0]
    y1 = location_coords[location_num1][1]
    x2 = location_coords[location_num2][0]
    y2 = location_coords[location_num2][1]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def flight_cost(location_coords, location_num1, location_num2):
    """
    Returns the integer cost of flying between two locations (by index).
    The cost is floor(euclidean_distance) + 1 to avoid zero-cost flights.
    Used in Part 2 when numeric planning is introduced.
    """
    return int(distance(location_coords, location_num1, location_num2)) + 1


def setup_content_types(options):
    """
    Randomly assigns crates to content types (food, medicine, etc.).
    Guarantees:
      - At least one crate per content type.
      - Enough crates of each type to satisfy the requested number of goals.

    Returns:
        crates_with_contents: list of lists.
          crates_with_contents[i] = list of crate names that contain content_types[i].
    """
    while True:
        num_crates_with_contents = []
        crates_left = options.crates

        # Distribute crates among all content types, leaving at least 1 for each remaining type.
        for x in range(len(content_types) - 1):
            types_after_this = len(content_types) - x - 1
            max_now = crates_left - types_after_this  # Reserve at least 1 for each remaining type
            num = random.randint(1, max_now)
            num_crates_with_contents.append(num)
            crates_left -= num

        # Last content type gets all remaining crates
        num_crates_with_contents.append(crates_left)

        # Maximum achievable goals: for each content type, at most min(crates, persons) goals.
        # (A person can only need each content once, and we can only give each crate once.)
        maxgoals = sum(min(num_crates, options.persons) for num_crates in num_crates_with_contents)

        # If the random split supports enough goals, accept it; otherwise retry.
        if options.goals <= maxgoals:
            break

    # Print a summary of the content distribution
    print()
    print("Types\tQuantities")
    for x in range(len(num_crates_with_contents)):
        if num_crates_with_contents[x] > 0:
            print(content_types[x] + "\t " + str(num_crates_with_contents[x]))

    # Assign crate names to each content type bucket
    crates_with_contents = []
    counter = 1
    for x in range(len(content_types)):
        crates = []
        for y in range(num_crates_with_contents[x]):
            crates.append("crate" + str(counter))  # crate1, crate2, ...
            counter += 1
        crates_with_contents.append(crates)

    return crates_with_contents


def setup_location_coords(options):
    """
    Assigns random (x, y) coordinates to each location for use in flight cost calculations.
    The depot is at (0, 0). Other locations get random coordinates in [1, 200] x [1, 200].

    Returns:
        location_coords: list of (x, y) tuples, one per location (depot first).
    """
    location_coords = [(0, 0)]  # Depot is at the origin
    for x in range(1, options.locations + 1):
        location_coords.append((random.randint(1, 200), random.randint(1, 200)))

    print("Location positions", location_coords)
    return location_coords


def setup_person_needs(options, crates_with_contents):
    """
    Randomly generates the goal assignments: which person needs which content type.
    Each person can need at most one crate of each content type.
    The total number of goal assignments equals options.goals.

    Args:
        options: parsed command-line options
        crates_with_contents: output of setup_content_types()

    Returns:
        need: 2D boolean list.
          need[person_idx][content_idx] = True means that person needs that content.
    """
    # Initialize: no person needs anything yet
    need = [[False for i in range(len(content_types))] for j in range(options.persons)]
    # Track how many goals we've assigned per content type (to respect crate limits)
    goals_per_contents = [0 for i in range(len(content_types))]

    for goalnum in range(options.goals):
        generated = False
        while not generated:
            rand_person = random.randint(0, options.persons - 1)
            rand_content = random.randint(0, len(content_types) - 1)

            # Assign this goal only if:
            # 1. We haven't used all crates of this content type yet
            # 2. This person doesn't already need this content type
            if (goals_per_contents[rand_content] < len(crates_with_contents[rand_content])
                    and not need[rand_person][rand_content]):
                need[rand_person][rand_content] = True
                goals_per_contents[rand_content] += 1
                generated = True

    return need


########################################################################################
# Main program
########################################################################################

def main():
    """
    Entry point: parses command-line arguments, generates all object/init/goal data,
    and writes a complete PDDL problem file to disk.
    """

    parser = OptionParser(usage='python generate-problem.py [-help] options...')
    parser.add_option('-d', '--drones',    metavar='NUM', dest='drones',    type=int, help='number of drones')
    parser.add_option('-r', '--carriers',  metavar='NUM', dest='carriers',  type=int, help='number of carriers (use 0 for parte 1)')
    parser.add_option('-l', '--locations', metavar='NUM', dest='locations', type=int, help='number of locations (excluding depot)')
    parser.add_option('-p', '--persons',   metavar='NUM', dest='persons',   type=int, help='number of persons')
    parser.add_option('-c', '--crates',    metavar='NUM', dest='crates',    type=int, help='number of crates')
    parser.add_option('-g', '--goals',     metavar='NUM', dest='goals',     type=int, help='number of goal assignments')

    (options, args) = parser.parse_args()

    # Validate that all required arguments are present
    if options.drones    is None: print("You must specify --drones (use --help for help)");    sys.exit(1)
    if options.carriers  is None: print("You must specify --carriers (use --help for help)");  sys.exit(1)
    if options.locations is None: print("You must specify --locations (use --help for help)"); sys.exit(1)
    if options.persons   is None: print("You must specify --persons (use --help for help)");   sys.exit(1)
    if options.crates    is None: print("You must specify --crates (use --help for help)");    sys.exit(1)
    if options.goals     is None: print("You must specify --goals (use --help for help)");     sys.exit(1)

    # Validate logical constraints
    if options.goals > options.crates:
        print("Cannot have more goals than crates"); sys.exit(1)
    if len(content_types) > options.crates:
        print("Cannot have more content types than crates:", content_types); sys.exit(1)
    if options.goals > len(content_types) * options.persons:
        print("For", options.persons, "persons, you can have at most", len(content_types) * options.persons, "goals"); sys.exit(1)

    # Print summary of chosen parameters
    print("Drones\t\t", options.drones)
    print("Carriers\t", options.carriers)
    print("Locations\t", options.locations)
    print("Persons\t\t", options.persons)
    print("Crates\t\t", options.crates)
    print("Goals\t\t", options.goals)

    # ---------------------------------------------------------------------------------
    # Build object name lists
    # ---------------------------------------------------------------------------------
    drone    = []
    person   = []
    crate    = []
    carrier  = []
    location = []

    location.append("depot")  # The depot is always location index 0
    for x in range(options.locations):
        location.append("loc" + str(x + 1))   # loc1, loc2, ...

    for x in range(options.drones):
        drone.append("drone" + str(x + 1))    # drone1, drone2, ...

    for x in range(options.carriers):
        carrier.append("carrier" + str(x + 1))  # carrier1, ... (unused in parte 1)

    for x in range(options.persons):
        person.append("person" + str(x + 1))   # person1, person2, ...

    for x in range(options.crates):
        crate.append("crate" + str(x + 1))    # crate1, crate2, ...

    # ---------------------------------------------------------------------------------
    # Randomize the world
    # ---------------------------------------------------------------------------------

    # Assign crates to content types (e.g., crate1=food, crate2=medicine)
    crates_with_contents = setup_content_types(options)

    # Give each location a random (x,y) coordinate (used for flight costs in parte 2)
    location_coords = setup_location_coords(options)

    # Decide which persons need which content types
    need = setup_person_needs(options, crates_with_contents)

    # Assign each person to a random non-depot location (persons are never at the depot)
    # location[0] = depot, so we pick from location[1:]
    person_locations = []
    for p in range(options.persons):
        # randint(1, options.locations) picks a valid non-depot location index
        person_locations.append(location[random.randint(1, options.locations)])

    # ---------------------------------------------------------------------------------
    # Build name for the output file
    # ---------------------------------------------------------------------------------
    problem_name = (
        "drone_problem"
        "_d" + str(options.drones)
        + "_r" + str(options.carriers)
        + "_l" + str(options.locations)
        + "_p" + str(options.persons)
        + "_c" + str(options.crates)
        + "_g" + str(options.goals)
        + "_ct" + str(len(content_types))
    )

    # ---------------------------------------------------------------------------------
    # Write PDDL problem file
    # ---------------------------------------------------------------------------------
    with open(problem_name + ".pddl", 'w') as f:

        # --- Problem header ---
        f.write("(define (problem " + problem_name + ")\n")
        f.write("(:domain drone-domain)\n")

        # --- Objects section ---
        # Declares all instances of each type used in this problem.
        f.write("(:objects\n")

        for x in drone:
            f.write("\t" + x + " - drone\n")         # e.g. drone1 - drone

        for x in location:
            f.write("\t" + x + " - location\n")      # depot - location, loc1 - location, ...

        for x in crate:
            f.write("\t" + x + " - crate\n")         # crate1 - crate, ...

        for x in content_types:
            f.write("\t" + x + " - contents\n")      # food - contents, medicine - contents

        for x in person:
            f.write("\t" + x + " - person\n")        # person1 - person, ...

        # Carriers are only relevant in Part 2; we include them in the object list
        # so the generator works for future labs without modification.
        for x in carrier:
            f.write("\t" + x + " - carrier\n")       # carrier1 - carrier, ...

        f.write(")\n")

        # --- Init section ---
        # Describes the initial state of the world.
        f.write("(:init\n")

        # Every drone starts at the depot, with both arms free.
        for d in drone:
            f.write("\t(at-drone " + d + " depot)\n")   # Drone is at the depot
            f.write("\t(arm1-free " + d + ")\n")        # Arm 1 is free (no crate held)
            f.write("\t(arm2-free " + d + ")\n")        # Arm 2 is free (no crate held)

        # All crates start at the depot.
        for c in crate:
            f.write("\t(at-crate " + c + " depot)\n")  # Crate at depot initially

        # Declare what each crate contains.
        # We iterate through content type buckets to know which crates hold which contents.
        for content_idx in range(len(content_types)):
            content_name = content_types[content_idx]
            for c in crates_with_contents[content_idx]:
                # e.g. (crate-contents crate1 food)
                f.write("\t(crate-contents " + c + " " + content_name + ")\n")

        # Each person is at a randomly chosen non-depot location.
        for p_idx in range(options.persons):
            p_name  = person[p_idx]
            p_loc   = person_locations[p_idx]
            # e.g. (at-person person1 loc2)
            f.write("\t(at-person " + p_name + " " + p_loc + ")\n")

        f.write(")\n")

        # --- Goal section ---
        # All goals are positive conjuncts — no negative goals.
        f.write("(:goal (and\n")

        # The drone should return to the depot when done.
        for d in drone:
            f.write("\n")
            # e.g. (at-drone drone1 depot)
            f.write("\t(at-drone " + d + " depot)\n")

        # Each person that needs a content type should have it by the end.
        for p_idx in range(options.persons):
            for ct_idx in range(len(content_types)):
                if need[p_idx][ct_idx]:
                    p_name       = person[p_idx]
                    content_name = content_types[ct_idx]
                    # e.g. (has-content person1 food)
                    f.write("\t(has-content " + p_name + " " + content_name + ")\n")

        f.write("\t))\n")
        f.write(")\n")

    print("\nGenerated: " + problem_name + ".pddl")


if __name__ == '__main__':
    main()
