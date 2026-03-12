(define (domain ubermedics-carriers)

    (:requirements :strips :typing)

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
    )

    (:action fly
        :parameters (?d - drone ?from - location ?to - location)
        :precondition (and
            (drone-at ?d ?from)
        )
        :effect (and
            (not (drone-at ?d ?from))
            (drone-at ?d ?to)
        )
    )

    (:action pick-up-box
        :parameters (?d - drone ?b - crate ?l - location)
        :precondition (and
            (drone-at ?d ?l)
            (crate-at ?b ?l)
            (drone-free ?d)
        )
        :effect (and
            (not (crate-at ?b ?l))
            (not (drone-free ?d))
            (holding ?d ?b)
        )
    )

    (:action put-box-on-carrier
        :parameters (?d - drone ?b - crate ?k - carrier ?l - location ?n1 - num ?n2 - num)
        :precondition (and
            (drone-at ?d ?l)
            (carrier-at ?k ?l)
            (holding ?d ?b)
            (carrier-load ?k ?n1)
            (next ?n1 ?n2)
        )
        :effect (and
            (not (holding ?d ?b))
            (drone-free ?d)
            (in-carrier ?b ?k)
            (not (carrier-load ?k ?n1))
            (carrier-load ?k ?n2)
        )
    )

    (:action pick-box-from-carrier
        :parameters (?d - drone ?b - crate ?k - carrier ?l - location ?n1 - num ?n2 - num)
        :precondition (and
            (drone-at ?d ?l)
            (carrier-at ?k ?l)
            (in-carrier ?b ?k)
            (drone-free ?d)
            (carrier-load ?k ?n2)
            (next ?n1 ?n2)
        )
        :effect (and
            (not (in-carrier ?b ?k))
            (not (drone-free ?d))
            (holding ?d ?b)
            (not (carrier-load ?k ?n2))
            (carrier-load ?k ?n1)
        )
    )

    (:action move-carrier
        :parameters (?d - drone ?k - carrier ?from - location ?to - location)
        :precondition (and
            (drone-at ?d ?from)
            (carrier-at ?k ?from)
            (drone-free ?d)
        )
        :effect (and
            (not (drone-at ?d ?from))
            (not (carrier-at ?k ?from))
            (drone-at ?d ?to)
            (carrier-at ?k ?to)
        )
    )

    (:action deliver-box
        :parameters (?d - drone ?b - crate ?p - person ?l - location ?c - contents)
        :precondition (and
            (drone-at ?d ?l)
            (person-at ?p ?l)
            (holding ?d ?b)
            (crate-has ?b ?c)
        )
        :effect (and
            (not (holding ?d ?b))
            (drone-free ?d)
            (person-has ?p ?c)
        )
    )

)