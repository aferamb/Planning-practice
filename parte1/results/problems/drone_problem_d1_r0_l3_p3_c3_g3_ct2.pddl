(define (problem drone_problem_d1_r0_l3_p3_c3_g3_ct2)
(:domain ubermedics)
(:objects
	drone1 - drone
	depot - location
	loc1 - location
	loc2 - location
	loc3 - location
	crate1 - crate
	crate2 - crate
	crate3 - crate
	food - contents
	medicine - contents
	person1 - person
	person2 - person
	person3 - person
)
(:init
	(drone-at drone1 depot)
	(arm-free-left drone1)
	(arm-free-right drone1)
	(crate-at crate1 depot)
	(crate-at crate2 depot)
	(crate-at crate3 depot)
	(crate-has crate1 food)
	(crate-has crate2 food)
	(crate-has crate3 medicine)
	(person-at person1 loc3)
	(person-at person2 loc1)
	(person-at person3 loc2)
)
(:goal (and

	(drone-at drone1 depot)	(person-has person1 food)
	(person-has person1 medicine)
	(person-has person2 food)
	))
)
