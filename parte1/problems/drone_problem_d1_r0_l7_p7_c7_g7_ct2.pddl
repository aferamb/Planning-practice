(define (problem drone_problem_d1_r0_l7_p7_c7_g7_ct2)
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
	crate1 - crate
	crate2 - crate
	crate3 - crate
	crate4 - crate
	crate5 - crate
	crate6 - crate
	crate7 - crate
	food - contents
	medicine - contents
	person1 - person
	person2 - person
	person3 - person
	person4 - person
	person5 - person
	person6 - person
	person7 - person
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
	(crate-has crate1 food)
	(crate-has crate2 food)
	(crate-has crate3 food)
	(crate-has crate4 medicine)
	(crate-has crate5 medicine)
	(crate-has crate6 medicine)
	(crate-has crate7 medicine)
	(person-at person1 loc1)
	(person-at person2 loc5)
	(person-at person3 loc5)
	(person-at person4 loc6)
	(person-at person5 loc2)
	(person-at person6 loc3)
	(person-at person7 loc1)
)
(:goal (and
	(drone-at drone1 depot)
	(person-has person1 food)
	(person-has person1 medicine)
	(person-has person2 food)
	(person-has person3 medicine)
	(person-has person4 medicine)
	(person-has person5 food)
	(person-has person5 medicine)
	))
)
