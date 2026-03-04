(define (problem drone_problem_d1_r0_l6_p6_c6_g6_ct2)
(:domain ubermedics)
(:objects
	drone1 - drone
	depot - location
	loc1 - location
	loc2 - location
	loc3 - location
	loc4 - location
	loc5 - location
	loc6 - location
	crate1 - crate
	crate2 - crate
	crate3 - crate
	crate4 - crate
	crate5 - crate
	crate6 - crate
	food - contents
	medicine - contents
	person1 - person
	person2 - person
	person3 - person
	person4 - person
	person5 - person
	person6 - person
)
(:init
	(drone-at drone1 depot)
	(arm-free-left drone1)
	(arm-free-right drone1)
	(crate-at crate1 depot)
	(crate-at crate2 depot)
	(crate-at crate3 depot)
	(crate-at crate4 depot)
	(crate-at crate5 depot)
	(crate-at crate6 depot)
	(crate-has crate1 food)
	(crate-has crate2 food)
	(crate-has crate3 food)
	(crate-has crate4 food)
	(crate-has crate5 food)
	(crate-has crate6 medicine)
	(person-at person1 loc1)
	(person-at person2 loc2)
	(person-at person3 loc1)
	(person-at person4 loc1)
	(person-at person5 loc3)
	(person-at person6 loc1)
)
(:goal (and

	(drone-at drone1 depot)	(person-has person1 food)
	(person-has person2 food)
	(person-has person3 food)
	(person-has person4 food)
	(person-has person4 medicine)
	(person-has person6 food)
	))
)
