# cannon.py
# Gavin Haynes
# Defines a Cannon object, which reperesents an entity that fires
# projectiles.

import random
import math

import numpy as np

MUTATIONRATES = np.array([
    [80, 10, 9, 1],   # A
    [5, 70, 20, 5],   # C
    [5, 20, 70, 5],   # T
    [1, 9, 10, 80]    # G
], dtype=float)



def score_matrix():
    # Step 1: Normalize mutation rates to probabilities (row-wise)
    row_sums = MUTATIONRATES.sum(axis=1, keepdims=True)
    prob_matrix = MUTATIONRATES / row_sums

    # Step 2: Assume equal background frequencies for A, C, T, G (25% each)
    background_freq = np.array([0.25, 0.25, 0.25, 0.25])

    # Step 3: Compute log-odds scores using log base 2
    log_odds_matrix = np.log2(prob_matrix / (background_freq * background_freq[:, None]))

    # Step 4: Round values for readability
    log_odds_matrix = np.round(log_odds_matrix, 0)

    # Step 5: Print matrix
    nucleotides = ['A', 'C', 'T', 'G']
    print("Log-Odds Scoring Matrix:\n")
    print("    ", "     ".join(nucleotides))
    for i, row in enumerate(log_odds_matrix):
        print(nucleotides[i], row)

# Cannon entity simulates a projectile launcher
class Cannon:
    # Initialize a new Cannon entity with random genes and a position.
    def __init__(self):
        self.GENE_LEN = 32
        self.ALLELES = ['A', 'C', 'T', 'G']
        self.tiltGene = self.makeRandomGene()
        self.powerGene = self.makeRandomGene()

    def makeRandomGene(self) -> list[str]:
        return [random.choice(self.ALLELES) for _ in range(0, self.GENE_LEN)]

    # Count A's to calculate tilt and power.
    def getStats(self):
        return self.calcTilt(), self.calcPower()
    
    # Compute the score of a gene
    def calcGene(self, gene):
        score = 0
        for allele in gene:
            match allele:
                case 'A': 
                    score += 5
                case 'C':
                    score += 1
                case 'T':
                    score += -1
                case 'G':
                    score += -5
                case _:
                    pass
        return score

    def calcTilt(self):
        return self.calcGene(self.getTiltGene())

    def calcPower(self):
        return self.calcGene(self.getPowerGene())
    
    # Return a new copy
    def copy(self):
        temp = Cannon()
        temp.setTiltGene(self.getTiltGene())
        temp.setPowerGene(self.getPowerGene())
        return temp

    # Decompose tilt and power in to x and y velocities.
    def getVelocity(self):
        tilt, power = self.getStats()
        tilt = tilt * math.pi / 180     # convert tilt to rads
        return (power*math.cos(tilt), power*math.sin(tilt))
    
    # Calculate the position of the cannon's projectile after t seconds.
    def fire(self, t) -> tuple[int, int]:
        vx, vy = self.getVelocity()
        x0, y0 = 0, 0
        g = 9.81
        xf = x0 + vx*t
        yf = y0 + vy*t - (g * t ** 2) / 2
        return (int(xf), int(yf))

    def mutateTilt(self, percent: int): 
        self.mutateGene(self.getTiltGene(), percent)

    def mutatePower(self, percent: int):
        self.mutateGene(self.getPowerGene(), percent)

    def mutateGene(self, gene: list, percent: int):
        for i in range(0, self.percent(percent)):
            gene[i] = self.mutateAllele(random.choice(gene))

    # Mutate a single allele to another with weighted probability
    def mutateAllele(self, allele):
        p = MUTATIONRATES[allele]
        pool = []
        for i in range(0, len(p)):
            pool += [self.ALLELES[i] for _ in range(0, p[i])]
        # print(pool)
        return random.choice(pool)

    def percent(self, n):
        return n // 100 * self.size()

    def size(self):
        return len(self.getTiltGene())

    def getTiltGene(self):
        return self.tiltGene

    def getPowerGene(self):
        return self.powerGene
    
    def setTiltGene(self, newGene):
        self.tiltGene = newGene

    def setPowerGene(self, newGene):
        self.powerGene = newGene