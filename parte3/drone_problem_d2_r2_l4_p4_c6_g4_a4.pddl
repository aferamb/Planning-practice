(define (problem drone_problem_d2_r2_l4_p4_c6_g4_a4)
(:domain ubermedics-carriers-temporal)
(:objects
	drone1 - drone
	drone2 - drone
	depot - location
	loc1 - location
	loc2 - location
	loc3 - location
	loc4 - location
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
	carrier1 - carrier
	carrier2 - carrier
	n0 - num
	n1 - num
	n2 - num
	n3 - num
	n4 - num
)
(:init
	(drone-at drone1 depot)
	(drone-free drone1)
	(drone-available drone1)
	(drone-at drone2 depot)
	(drone-free drone2)
	(drone-available drone2)
	(crate-at crate1 depot)
	(crate-at crate2 depot)
	(crate-at crate3 depot)
	(crate-at crate4 depot)
	(crate-at crate5 depot)
	(crate-at crate6 depot)
	(carrier-at carrier1 depot)
	(carrier-load carrier1 n0)
	(carrier-free carrier1)
	(carrier-at carrier2 depot)
	(carrier-load carrier2 n0)
	(carrier-free carrier2)
	(next n0 n1)
	(next n1 n2)
	(next n2 n3)
	(next n3 n4)
	(crate-has crate1 food)
	(crate-has crate2 food)
	(crate-has crate3 medicine)
	(crate-has crate4 medicine)
	(crate-has crate5 medicine)
	(crate-has crate6 medicine)
	(person-at person1 loc3)
	(person-free person1)
	(person-at person2 loc3)
	(person-free person2)
	(person-at person3 loc4)
	(person-free person3)
	(person-at person4 loc3)
	(person-free person4)
	(= (fly-cost depot depot) 0)
	(= (fly-cost depot loc1) 33)
	(= (fly-cost depot loc2) 176)
	(= (fly-cost depot loc3) 203)
	(= (fly-cost depot loc4) 155)
	(= (fly-cost loc1 depot) 33)
	(= (fly-cost loc1 loc1) 0)
	(= (fly-cost loc1 loc2) 143)
	(= (fly-cost loc1 loc3) 192)
	(= (fly-cost loc1 loc4) 141)
	(= (fly-cost loc2 depot) 176)
	(= (fly-cost loc2 loc1) 143)
	(= (fly-cost loc2 loc2) 0)
	(= (fly-cost loc2 loc3) 211)
	(= (fly-cost loc2 loc4) 169)
	(= (fly-cost loc3 depot) 203)
	(= (fly-cost loc3 loc1) 192)
	(= (fly-cost loc3 loc2) 211)
	(= (fly-cost loc3 loc3) 0)
	(= (fly-cost loc3 loc4) 52)
	(= (fly-cost loc4 depot) 155)
	(= (fly-cost loc4 loc1) 141)
	(= (fly-cost loc4 loc2) 169)
	(= (fly-cost loc4 loc3) 52)
	(= (fly-cost loc4 loc4) 0)
)
(:goal (and
	(person-has person1 medicine)
	(person-has person2 medicine)
	(person-has person3 food)
	(person-has person4 medicine)
))
)
