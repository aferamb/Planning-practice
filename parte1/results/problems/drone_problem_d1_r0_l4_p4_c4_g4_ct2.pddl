(define (problem drone_problem_d1_r0_l4_p4_c4_g4_ct2)
(:domain ubermedics)
(:objects
	drone1 - drone
	depot - location
	loc1 - location
	loc2 - location
	loc3 - location
	loc4 - location
	crate1 - crate
	crate2 - crate
	crate3 - crate
	crate4 - crate
	food - contents
	medicine - contents
	person1 - person
	person2 - person
	person3 - person
	person4 - person
)
(:init
	(drone-at drone1 depot)
	(arm-free-left drone1)
	(arm-free-right drone1)
	(crate-at crate1 depot)
	(crate-at crate2 depot)
	(crate-at crate3 depot)
	(crate-at crate4 depot)
	(crate-has crate1 food)
	(crate-has crate2 medicine)
	(crate-has crate3 medicine)
	(crate-has crate4 medicine)
	(person-at person1 loc3)
	(person-at person2 loc4)
	(person-at person3 loc2)
	(person-at person4 loc4)
)
(:goal (and

	(drone-at drone1 depot)	(person-has person1 medicine)
	(person-has person2 medicine)
	(person-has person3 medicine)
	(person-has person4 food)
	))
)
