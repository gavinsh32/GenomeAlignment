# simulator.py
# Handles the environment where cannons "shoot"

import population
import cannon
import math
import random

class Simulator:
    # Init a simulation environment with a population of cannons
    def __init__(self):
        self.target = (50, 40, 60, 50)
        self.dimensions = (100, 100)

    # Init a square target from the bottom left corner
    def initTarget(self, x1, y1, w):
        self.target = (x1, y1, x1 + w, y1 + w)

    # Init dimensions of simulator
    def initBounds(self, w, h):
        self.dimensions = (w, h)

    # Fire all cannons, return all which come within some threshold of the target
    def fire(self, pop : population, threshold: int) -> population:
        step=0.1
        max=3
        hit = []    # Cannons which hit the target 
        minDist = [1000000 for i in range(0, pop.size())]   # The closest they came to the target

        # For each cannon in population
        for i in range(0, pop.size()):
            cannon = pop.at(i)
            t = 0
            while t < max:
                result = cannon.fire(t)
                #print('Firing:', result)

                # Check if the cannon came closer to the target
                dist = self.distToTarget(result)
                if dist < minDist[i]:
                    minDist[i] = dist

                # Cannon hit the target
                if self.inTarget(result):
                    hit.append(cannon)
                    #print('Hit target at', result)
                    break

                # Cannon went out of bounds
                elif not self.inBounds(result):
                    #print('Fell out of bounds at', result)
                    break

                t += step

        # Select individuals within the threshold
        return self.select(pop, minDist, threshold)

    # Select all cannons from a population under a threshold t
    def select(self, pop: population, dists: list, thresh: int) -> population:
        newpop = population.Population(0)
        for i in range(0, pop.size()):
            if (dists[i] <= thresh):
                newpop.append(pop.at(i))
        return newpop

    # Check if the projectile is in the target
    def inTarget(self, coord):
        x, y = coord
        x0, y0, x1, y1 = self.getTarget()
        return x0 <= x <= x1 and y0 <= y <= y1

    # Check if a coordinate is in bounds
    def inBounds(self, coord):
        x, y = coord
        w, h = self.dimensions
        return 0 <= x <= w and 0 <= y <= h

    # Snap a coordinate to simulator bounds
    def snapToBounds(self, coord) -> tuple[int, int]:
        x, y = coord
        w, h = self.dimensions
        if x < 0: x = 0
        if x > w: x = w
        if y < 0: y = 0
        if y > h: y = h
        return (x, y)
    
    # Get target coordinates
    def getTarget(self) -> tuple[int, int, int, int]:
        return self.target
    
    # Get the coords of the center of the target
    def getTargetCenter(self) -> tuple[int, int]:
        x0, y0, x1, y1 = self.getTarget()
        return (x1 + x0) / 2, (y1 + y0) / 2

    # Find the distance from a coordinate to the center of the target
    def distToTarget(self, coord) -> int:
        tx, ty = self.getTargetCenter()
        x, y = coord
        return 0 if self.inTarget(coord) else math.sqrt((ty-y)**2 + (tx-x)**2)