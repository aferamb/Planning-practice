(define (problem drone_problem_d1_r0_l13_p13_c13_g13_ct2)
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
	loc9 - location
	loc10 - location
	loc11 - location
	loc12 - location
	loc13 - location
	crate1 - crate
	crate2 - crate
	crate3 - crate
	crate4 - crate
	crate5 - crate
	crate6 - crate
	crate7 - crate
	crate8 - crate
	crate9 - crate
	crate10 - crate
	crate11 - crate
	crate12 - crate
	crate13 - crate
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
	person9 - person
	person10 - person
	person11 - person
	person12 - person
	person13 - person
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
	(crate-at crate9 depot)
	(crate-at crate10 depot)
	(crate-at crate11 depot)
	(crate-at crate12 depot)
	(crate-at crate13 depot)
	(crate-has crate1 food)
	(crate-has crate2 food)
	(crate-has crate3 food)
	(crate-has crate4 food)
	(crate-has crate5 food)
	(crate-has crate6 food)
	(crate-has crate7 food)
	(crate-has crate8 food)
	(crate-has crate9 food)
	(crate-has crate10 food)
	(crate-has crate11 medicine)
	(crate-has crate12 medicine)
	(crate-has crate13 medicine)
	(person-at person1 loc13)
	(person-at person2 loc11)
	(person-at person3 loc11)
	(person-at person4 loc2)
	(person-at person5 loc5)
	(person-at person6 loc5)
	(person-at person7 loc12)
	(person-at person8 loc7)
	(person-at person9 loc10)
	(person-at person10 loc13)
	(person-at person11 loc9)
	(person-at person12 loc13)
	(person-at person13 loc3)
)
(:goal (and

	(drone-at drone1 depot)	(person-has person1 food)
	(person-has person2 food)
	(person-has person3 food)
	(person-has person4 food)
	(person-has person4 medicine)
	(person-has person5 medicine)
	(person-has person6 food)
	(person-has person6 medicine)
	(person-has person7 food)
	(person-has person8 food)
	(person-has person9 food)
	(person-has person10 food)
	(person-has person11 food)
	))
)
