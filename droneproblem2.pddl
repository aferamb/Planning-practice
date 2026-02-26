(define (problem problem2)
(:domain ubermedics)

(:objects
    d1 - drone
    depot loc1 loc2 - location
    p1 p2 - person
    b1 b2 b3 - crate
    food medicine water - content
)

(:init
    (drone-at d1 depot)

    (person-at p1 loc1)
    (person-at p2 loc2)

    (crate-at b1 depot)
    (crate-at b2 depot)
    (crate-at b3 depot)

    (crate-has b1 food)
    (crate-has b2 medicine)
    (crate-has b3 water)

    (arm-free-left d1)
    (arm-free-right d1)
)

(:goal
    (and
        (person-has p1 food)
        (person-has p2 medicine)
    )
)

)