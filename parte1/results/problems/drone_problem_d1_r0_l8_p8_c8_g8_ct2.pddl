(define (problem drone_problem_d1_r0_l8_p8_c8_g8_ct2)
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
	loc7 - location
	loc8 - location
	crate1 - crate
	crate2 - crate
	crate3 - crate
	crate4 - crate
	crate5 - crate
	crate6 - crate
	crate7 - crate
	crate8 - crate
	food - contents
	medicine - contents
	person1 - person
	person2 - person
	person3 - person
	person4 - person
	person5 - person
	person6 - person
	person7 - person
	person8 - person
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
	(crate-at crate7 depot)
	(crate-at crate8 depot)
	(crate-has crate1 food)
	(crate-has crate2 food)
	(crate-has crate3 medicine)
	(crate-has crate4 medicine)
	(crate-has crate5 medicine)
	(crate-has crate6 medicine)
	(crate-has crate7 medicine)
	(crate-has crate8 medicine)
	(person-at person1 loc4)
	(person-at person2 loc7)
	(person-at person3 loc7)
	(person-at person4 loc2)
	(person-at person5 loc2)
	(person-at person6 loc4)
	(person-at person7 loc1)
	(person-at person8 loc4)
)
(:goal (and

	(drone-at drone1 depot)	(person-has person1 medicine)
	(person-has person2 medicine)
	(person-has person3 medicine)
	(person-has person4 food)
	(person-has person6 food)
	(person-has person6 medicine)
	(person-has person7 medicine)
	(person-has person8 medicine)
	))
)
