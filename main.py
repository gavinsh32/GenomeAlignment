# main.py
# Gavin Haynes, Sam Beal
# Simulate and evolve virtual cannons.

import simulator
import population
import cannon
import analyze


# Settings
width = 100
height = 100
targetx = 50
targety = 30
targetw = 10

# Engine
def generation(sim, psize, reproduction):
    time = []
    pop = population.Population(n=psize)
    for epoch in range(0, 16):
        print('Generation', epoch, 'population size', pop.size())
        time.append(epoch)
        
        result = sim.fire(pop, 0) # fires cannons, and selects the good ones
        success = result.size() / pop.size()
        print('Success:', success)
        result.reproduce(reproduction)
        result.cull(30) # increase selection pressure
        # result.mutate()
        for obj in result.population:
            obj.mutateTilt(10)
            obj.mutatePower(10)
        
        analyze.save_sequence(result, epoch, success)
        
        pop.cull(20)
        pop.join(result)
    return time

# Initialize simulator, bounds, and target position
sim = simulator.Simulator()
sim.initBounds(width, height)
sim.initTarget(targetx, targety, width)

# population size and reproduction rate
psize = 100
reproduction = 0

# keep track of time for graphing
time = generation(sim, psize, reproduction)
#analyze.graphs_generations()
#analyze.graph_gene_count()