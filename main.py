# main.py
# Gavin Haynes, Sam Beal
# Simulate and evolve virtual cannons.

import simulator
import population
import cannon

# Settings
width = 100
height = 100
targetx = 50
targety = 30
targetw = 10
psize = 100

sim = simulator.Simulator()
sim.initBounds(width, height)
sim.initTarget(targetx, targety, targetw)

pop = population.Population(psize)

for epoch in range(0, 16):
    print('Generation', epoch, 'population size', pop.size())
        
    result = sim.fire(pop, 0) # fires cannons, and selects the good ones

    print('Success:', result.size() / pop.size())

    result.reproduce(20)
    result.cull(30) # increase selection pressure
        
    pop.cull(20)
    pop.join(result)