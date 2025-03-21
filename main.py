# main.py
# Gavin Haynes, Sam Beal
# Simulate and evolve virtual cannons.

import simulator
import population
import cannon
import Alignment
import pandas
import random
import matplotlib.pyplot as plt

# General Settings
N_EPOCHS = 16
N_RUNS = 4

# Simulator Settings
WIDTH = 200
HEIGHT = 200
TARGETX = 5
TARGETY = 5
TARGET_WIDTH = 10
FIRE_THRESHOLD = 0

# Population and Growth Settings
INITIAL_SIZE = 256
PER_REPRODUCE_VICTORS = 20
PER_CULL_VICTORS = 30
PER_CULL_POP = 20

# Alignment Settings
N_INDIVIDUALS_COMPARED = 10

# Init the simulator with chosen settings
sim = simulator.Simulator()
sim.initBounds(WIDTH, HEIGHT)
sim.initTarget(TARGETX, TARGETY, TARGET_WIDTH)

# Main engine
runs = []
for run in range(0, N_RUNS):
    align_avgs = [0 for _ in range(0, N_EPOCHS)]
    pop = population.Population(INITIAL_SIZE)
    # Main loop
    for epoch in range(0, N_EPOCHS):
        # Compute average population alignment score for 10 random individuals
        individuals = pop.getPop()
        align_avg = 0
        for i in range(0, N_INDIVIDUALS_COMPARED):
            # Randomly select two individuals
            ind1 = random.choice(individuals)
            ind2 = random.choice(individuals)
            a = ind1.getTiltGene()
            b = ind2.getTiltGene()
            align = Alignment.Alignment(a, b)
            score, s, t = align.align()
            align_avg += score

        align_avgs[epoch] += align_avg // N_INDIVIDUALS_COMPARED

        result = sim.fire(pop, FIRE_THRESHOLD) # fires cannons, and selects the good ones

        result.cull(PER_CULL_VICTORS) # increase selection pressure

        result.reproduce(PER_REPRODUCE_VICTORS) # reproduce victors

        pop.cull(PER_CULL_POP)  # shrink initial population

        pop.join(result)    # join to final

    runs.append(align_avgs)

avgAlignPerGen = []

# Convert run data to avg vs. generation
for g in range(0, N_EPOCHS):
    avg = 0
    for r in range(0, N_RUNS):
        avg += runs[r][g]
    avg /= N_RUNS
    avgAlignPerGen.append(avg)

# Convert data to Pandas Dataframe and plot
xAxis = [i for i in range(0, len(avgAlignPerGen))]
data = {'Generation': xAxis, 'Average Alignment Score': avgAlignPerGen}
dataframe = pandas.DataFrame(data)
dataframe.plot(
    x = 'Generation',
    y = 'Average Alignment Score',
    kind = 'line',
    title = 'Average Alignment Score vs. Generation, Initial Size = ' + repr(INITIAL_SIZE),
    xlabel = 'Generation',
    ylabel = 'Average Alignment Score',
    grid = True,
    figsize = (8, 6)
)
plt.savefig('initialsize' + repr(INITIAL_SIZE) + '.jpg')