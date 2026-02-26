(define (problem droneproblem1)
  (:domain ubermedics)

  (:objects
    d1 - drone
    depot loc1 - location
    p1 - person
    b1 - crate
    food - content
  )

  (:init
    (drone-at d1 depot)
    (person-at p1 loc1)
    (crate-at b1 depot)
    (crate-has b1 food)
    (arm-free-left d1)
    (arm-free-right d1)
  )

  (:goal
    (and
      (person-has p1 food)
    )
  )
)