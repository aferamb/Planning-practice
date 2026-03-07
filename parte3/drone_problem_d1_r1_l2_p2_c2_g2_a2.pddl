(define (problem drone_problem_d1_r1_l2_p2_c2_g2_a2)
(:domain ubermedics-carriers-temporal)
(:objects
	drone1 - drone
	depot - location
	loc1 - location
	loc2 - location
	crate1 - crate
	crate2 - crate
	food - contents
	medicine - contents
	person1 - person
	person2 - person
	carrier1 - carrier
	n0 - num
	n1 - num
	n2 - num
)
(:init
	(drone-at drone1 depot)
	(drone-free drone1)
	(drone-available drone1)
	(crate-at crate1 depot)
	(crate-at crate2 depot)
	(carrier-at carrier1 depot)
	(carrier-load carrier1 n0)
	(carrier-free carrier1)
	(next n0 n1)
	(next n1 n2)
	(crate-has crate1 food)
	(crate-has crate2 medicine)
	(person-at person1 loc1)
	(person-free person1)
	(person-at person2 loc1)
	(person-free person2)
	(= (fly-cost depot depot) 0)
	(= (fly-cost depot loc1) 70)
	(= (fly-cost depot loc2) 173)
	(= (fly-cost loc1 depot) 70)
	(= (fly-cost loc1 loc1) 0)
	(= (fly-cost loc1 loc2) 130)
	(= (fly-cost loc2 depot) 173)
	(= (fly-cost loc2 loc1) 130)
	(= (fly-cost loc2 loc2) 0)
)
(:goal (and
	(person-has person2 food)
	(person-has person2 medicine)
))
)
