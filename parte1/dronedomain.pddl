(define (domain ubermedics)

(:requirements :strips :typing)

(:types 
    drone
    location
    person
    crate
    contents
    carrier
)

(:predicates 
    (drone-at ?d - drone ?l - location)
    (person-at ?p - person ?l - location)
    (crate-at ?b - crate ?l - location)
    (crate-has ?b - crate ?c - contents)
    (person-has ?p - person ?c - contents)
    (carrying-left ?d - drone ?b - crate)
    (carrying-right ?d - drone ?b - crate)
    (arm-free-left ?d - drone)
    (arm-free-right ?d - drone)
)

(:action fly
    :parameters (?d - drone ?from - location ?to - location)
    :precondition (drone-at ?d ?from)
    :effect (and
        (not (drone-at ?d ?from))
        (drone-at ?d ?to)
    )
)

(:action pick-up-left
    :parameters (?d - drone ?b - crate ?l - location)
    :precondition (and
        (drone-at ?d ?l)
        (crate-at ?b ?l)
        (arm-free-left ?d)
    )
    :effect (and
        (not (crate-at ?b ?l))
        (not (arm-free-left ?d))
        (carrying-left ?d ?b)
    )
)

(:action pick-up-right
    :parameters (?d - drone ?b - crate ?l - location)
    :precondition (and
        (drone-at ?d ?l)
        (crate-at ?b ?l)
        (arm-free-right ?d)
    )
    :effect (and
        (not (crate-at ?b ?l))
        (not (arm-free-right ?d))
        (carrying-right ?d ?b)
    )
)

(:action deliver-left
    :parameters (?d - drone ?b - crate ?p - person ?l - location ?c - contents)
    :precondition (and
        (drone-at ?d ?l)
        (person-at ?p ?l)
        (carrying-left ?d ?b)
        (crate-has ?b ?c)
    )
    :effect (and
        (not (carrying-left ?d ?b))
        (arm-free-left ?d)
        (person-has ?p ?c)
    )
)

(:action deliver-right
    :parameters (?d - drone ?b - crate ?p - person ?l - location ?c - contents)
    :precondition (and
        (drone-at ?d ?l)
        (person-at ?p ?l)
        (carrying-right ?d ?b)
        (crate-has ?b ?c)
    )
    :effect (and
        (not (carrying-right ?d ?b))
        (arm-free-right ?d)
        (person-has ?p ?c)
    )
)

)