(define (domain ubermedics-carriers-temporal)

    (:requirements :typing :durative-actions :fluents)

    (:types
        drone location person crate contents carrier num
    )

    (:predicates
        (drone-at ?d - drone ?l - location)
        (person-at ?p - person ?l - location)
        (crate-at ?b - crate ?l - location)
        (carrier-at ?k - carrier ?l - location)

        (crate-has ?b - crate ?c - contents)
        (person-has ?p - person ?c - contents)

        (holding ?d - drone ?b - crate)
        (drone-free ?d - drone)

        (in-carrier ?b - crate ?k - carrier)
        (carrier-load ?k - carrier ?n - num)

        (next ?n1 - num ?n2 - num)

        (drone-available ?d - drone)
        (carrier-free ?k - carrier)
        (person-free ?p - person)
    )

    (:functions
        (fly-cost ?from - location ?to - location)
    )

    (:durative-action fly
        :parameters (?d - drone ?from - location ?to - location)
        :duration (= ?duration (fly-cost ?from ?to))
        :condition (and
            (at start (drone-at ?d ?from))
            (at start (drone-free ?d))
            (at start (drone-available ?d))
        )
        :effect (and
            (at start (not (drone-at ?d ?from)))
            (at start (not (drone-available ?d)))
            (at end (drone-at ?d ?to))
            (at end (drone-available ?d))
        )
    )

    (:durative-action pick-up-box
        :parameters (?d - drone ?b - crate ?l - location)
        :duration (= ?duration 5)
        :condition (and
            (at start (drone-at ?d ?l))
            (at start (crate-at ?b ?l))
            (at start (drone-free ?d))
            (at start (drone-available ?d))
        )
        :effect (and
            (at start (not (crate-at ?b ?l)))
            (at start (not (drone-free ?d)))
            (at start (not (drone-available ?d)))
            (at end (holding ?d ?b))
            (at end (drone-available ?d))
        )
    )

    (:durative-action put-box-on-carrier
        :parameters (?d - drone ?b - crate ?k - carrier ?l - location ?n1 - num ?n2 - num)
        :duration (= ?duration 5)
        :condition (and
            (at start (drone-at ?d ?l))
            (at start (carrier-at ?k ?l))
            (at start (holding ?d ?b))
            (at start (carrier-load ?k ?n1))
            (at start (next ?n1 ?n2))
            (at start (drone-available ?d))
            (at start (carrier-free ?k))
        )
        :effect (and
            (at start (not (holding ?d ?b)))
            (at start (not (carrier-load ?k ?n1)))
            (at start (not (drone-available ?d)))
            (at start (not (carrier-free ?k)))

            (at end (in-carrier ?b ?k))
            (at end (carrier-load ?k ?n2))
            (at end (drone-free ?d))
            (at end (drone-available ?d))
            (at end (carrier-free ?k))
        )
    )

    (:durative-action pick-box-from-carrier
        :parameters (?d - drone ?b - crate ?k - carrier ?l - location ?n1 - num ?n2 - num)
        :duration (= ?duration 5)
        :condition (and
            (at start (drone-at ?d ?l))
            (at start (carrier-at ?k ?l))
            (at start (in-carrier ?b ?k))
            (at start (drone-free ?d))
            (at start (carrier-load ?k ?n2))
            (at start (next ?n1 ?n2))
            (at start (drone-available ?d))
            (at start (carrier-free ?k))
        )
        :effect (and
            (at start (not (in-carrier ?b ?k)))
            (at start (not (carrier-load ?k ?n2)))
            (at start (not (drone-free ?d)))
            (at start (not (drone-available ?d)))
            (at start (not (carrier-free ?k)))

            (at end (holding ?d ?b))
            (at end (carrier-load ?k ?n1))
            (at end (drone-available ?d))
            (at end (carrier-free ?k))
        )
    )

    (:durative-action move-carrier
        :parameters (?d - drone ?k - carrier ?from - location ?to - location)
        :duration (= ?duration (fly-cost ?from ?to))
        :condition (and
            (at start (drone-at ?d ?from))
            (at start (carrier-at ?k ?from))
            (at start (drone-free ?d))
            (at start (drone-available ?d))
            (at start (carrier-free ?k))
        )
        :effect (and
            (at start (not (drone-at ?d ?from)))
            (at start (not (carrier-at ?k ?from)))
            (at start (not (drone-available ?d)))
            (at start (not (carrier-free ?k)))

            (at end (drone-at ?d ?to))
            (at end (carrier-at ?k ?to))
            (at end (drone-available ?d))
            (at end (carrier-free ?k))
        )
    )

    (:durative-action deliver-box
        :parameters (?d - drone ?b - crate ?p - person ?l - location ?c - contents)
        :duration (= ?duration 5)
        :condition (and
            (at start (drone-at ?d ?l))
            (at start (person-at ?p ?l))
            (at start (holding ?d ?b))
            (at start (crate-has ?b ?c))
            (at start (drone-available ?d))
            (at start (person-free ?p))
        )
        :effect (and
            (at start (not (holding ?d ?b)))
            (at start (not (drone-available ?d)))
            (at start (not (person-free ?p)))

            (at end (person-has ?p ?c))
            (at end (drone-free ?d))
            (at end (drone-available ?d))
            (at end (person-free ?p))
        )
    )
)