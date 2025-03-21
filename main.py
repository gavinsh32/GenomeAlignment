# main.py
# Gavin Haynes, Sam Beal
# Simulate and evolve virtual cannons.

import simulator
import population
import cannon
import pandas

# Simulator Settings
WIDTH = 200
HEIGHT = 200
TARGETX = 5
TARGETY = 5
TARGET_WIDTH = 10
FIRE_THRESHOLD = 0

# Population and Growth Settings
INITIAL_SIZE = 200
PER_REPRODUCE_VICTORS = 20
PER_CULL_VICTORS = 30
PER_CULL_POP = 20

# Init the simulator with chosen settings
sim = simulator.Simulator()
sim.initBounds(WIDTH, HEIGHT)
sim.initTarget(TARGETX, TARGETY, TARGET_WIDTH)

pop = population.Population(INITIAL_SIZE)

seq1 = 'ACTGTCAAC'
seq2 = 'TGTCAAC'

align = Alignment(seq1, seq2)

print(align.align())
print(align)

# Main loop
for epoch in range(0, 1):
    # print('Generation', epoch, 'population size', pop.size())

    result = sim.fire(pop, FIRE_THRESHOLD) # fires cannons, and selects the good ones

    # print('Success:', result.size() / pop.size())

    result.cull(PER_CULL_VICTORS) # increase selection pressure

    result.reproduce(PER_REPRODUCE_VICTORS) # reproduce victors
        
    pop.cull(PER_CULL_POP)  # shrink initial population

    pop.join(result)    # join to final