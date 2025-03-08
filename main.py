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

# Initialize simulator, bounds, and target position
sim = simulator.Simulator()
sim.initBounds(width, height)
sim.initTarget(targetx, targety, width)

# Engine
pop = population.Population(n=psize)
for epoch in range(0, 1):
    print('Generation', epoch, 'population size', pop.size())
    indiv = cannon.Cannon()
    print(indiv.getTiltGene())
    indiv.mutateTilt(10)
    print(indiv.getTiltGene())