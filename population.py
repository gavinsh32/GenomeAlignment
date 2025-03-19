# population.py

import math
import random
import cannon

# Defines a list of cannons, and extends cannon functionality to work on a population
class Population:
    population = [] # list of cannons

    # Init a new population from scratch
    def __init__(self, n=100, existing=None):
        random.seed()
        if existing is None:
            self.population = [cannon.Cannon() for i in range(0, n)]
        else:
            self.setPop(existing)
    
    # Fire all cannons and get the coordinates of each at time t
    def fire(self, t: float):
        return [cannon.fire(t) for cannon in self.getPop()]
    
    # Kill a percent of the total population randomly.
    def cull(self, percent: int) -> None:
        for i in range(0, self.percent(percent)):
            # Pick a random index from population
            victim = random.randrange(0, self.size())
            self.getPop().pop(victim)   # Pop vitcim from population

    def globalAlignment(self):
        # Get Mutation Rate Matrix
        # Convert to Log Odds
        logOdds = cannon.MUTATIONRATES
        print(logOdds)
        for i in range(0, 4):
            for j in range(0, 4):
                pass
        # Convert to Scoring Matrix
        # Perform Alignment
        # Return 
        pass

    # Mutate at most n characters in each tilt gene
    def mutateTilt(self, n: int, per: int) -> None:
        for i in range(0, self.percent(per)):
            random.choice(self.getPop()).mutateTilt(n)

    # Mutate at most n characters in each power gene
    def mutatePower(self, n: int, per: int) -> None:
        for i in range(0, self.percent(per)):
            random.choice(self.getPop()).mutatePower(n)

    # Return a percent of the population size.
    def percent(self, per: int) -> int:
        if 0 <= per and per <= 100:
            return int(self.size() * per / 100)
        else:
            return 0

    # Return a copy of the population
    def copy(self):
        return [cannon.copy() for cannon in self.getPop()]

    # Return the length of the population
    def size(self):
        return len(self.getPop())

    # Get a list of all cannon entities in population.
    def getPop(self):
        return self.population
    
    # Set the population to the new list of cannons
    def setPop(self, newPopulation):
        self.population = newPopulation

    # Return a reference to a cannon at an index
    def at(self, index) -> cannon:
        if 0 <= index and index < self.size():
            return self.population[index]
        else:
            return None

    # Reproduce population by a percent, and return children
    def reproduce(self, per):        
        children = [random.choice(self.getPop()) for _ in range(0, self.percent(per))]
        self.population += children

    # Join this population with another
    def join(self, population):
        if population is not None:
            self.setPop(self.getPop() + population.getPop())

    def append(self, cannon: cannon):
        if cannon is not None:
            self.getPop().append(cannon)

    # Get all tilt genes.
    def getTiltGenes(self):
        return [cannon.getTiltGene() for cannon in self.getPop()]
    
    # Get all power genes.
    def getPowerGenes(self):
        return [cannon.getPowerGene() for cannon in self.getPop()]

    # Get the tilt and power of all cannons.
    def getStats(self):
        return [cannon.getStats() for cannon in self.getPop()]
    
    # Get the x and y velocities of all cannons.
    def getVelocities(self):
        return [cannon.getVelocity() for cannon in self.getPop()]