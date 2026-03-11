(define (problem drone_problem_d1_r0_l12_p12_c12_g12_ct2)
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
	(crate-has crate1 food)
	(crate-has crate2 food)
	(crate-has crate3 food)
	(crate-has crate4 food)
	(crate-has crate5 food)
	(crate-has crate6 food)
	(crate-has crate7 medicine)
	(crate-has crate8 medicine)
	(crate-has crate9 medicine)
	(crate-has crate10 medicine)
	(crate-has crate11 medicine)
	(crate-has crate12 medicine)
	(person-at person1 loc3)
	(person-at person2 loc10)
	(person-at person3 loc9)
	(person-at person4 loc12)
	(person-at person5 loc7)
	(person-at person6 loc10)
	(person-at person7 loc4)
	(person-at person8 loc1)
	(person-at person9 loc1)
	(person-at person10 loc1)
	(person-at person11 loc5)
	(person-at person12 loc8)
)
(:goal (and

	(drone-at drone1 depot)	(person-has person1 food)
	(person-has person1 medicine)
	(person-has person4 food)
	(person-has person5 medicine)
	(person-has person7 food)
	(person-has person7 medicine)
	(person-has person8 medicine)
	(person-has person9 food)
	(person-has person10 medicine)
	(person-has person11 food)
	(person-has person12 food)
	(person-has person12 medicine)
	))
)
