# cannon.py
# Gavin Haynes
# Defines a Cannon object, which reperesents an entity that fires
# projectiles.

import random
import math

GENE_LEN = 90
ALLELES = ['A', 'C', 'T', 'G']

# Cannon entity simulates a projectile launcher
class Cannon:
    tiltGene = None
    powerGene = None
    x = 0
    y = 0

    # Initialize a new Cannon entity with random genes and a position.
    def __init__(self, x=0, y=0):
        self.tiltGene = self.makeRandomGene()
        self.powerGene = self.makeRandomGene()
        self.x = x
        self.y = y

    def makeRandomGene(self):
        return [random.choice(ALLELES) for _ in range(0, GENE_LEN)]

    # Count A's to calculate tilt and power.
    def getStats(self):
        tilt = 0
        power = 0
        for i in range(0, GENE_LEN):
            
            power += 1 if self.powerGene[i] == 'A' else 0
        return (float(tilt), float(power))
    
    def calcTilt(self):
        a = 5
        c = 1
        t = 1
        g = -5
        self.getPowerGene().count('A')

    def calcPower(self):
        pass
    
    # Return a new copy
    def copy(self):
        temp = Cannon(self.x, self.y)
        temp.setTiltGene(self.getTiltGene())
        temp.setPowerGene(self.getPowerGene())
        return temp

    # Decompose tilt and power in to x and y velocities.
    def getVelocity(self):
        tilt, power = self.getStats()
        tilt = tilt * math.pi / 180     # convert tilt to rads
        return (power*math.cos(tilt), power*math.sin(tilt))
    
    # Calculate the position of the cannon's projectile after t seconds.
    def fire(self, t):
        vx, vy = self.getVelocity()
        x0, y0 = self.x, self.y
        g = 9.81
        xf = x0 + vx*t
        yf = y0 + vy*t - (g * t ** 2) / 2
        return (int(xf), int(yf))
    
    def mutateAll(self, n):
        self.mutateTilt(n)
        self.mutatePower(n)

    # Randomly mutate between c1 and c2 number of genes
    def mutateTilt(self, n):  
        # Make a random range of positions in genome
        c = [random.randint(0, GENE_LEN-1) for i in range(0, n)]
        for i in c:
            if self.tiltGene[i] == 'A':
                self.tiltGene[i] = 'C'
            else:
                self.tiltGene[i] = 'A'

    # Randomly mutate between c1 and c2 number of genes
    def mutatePower(self, n):  
        # Make a random range of positions in genome
        c = [random.randint(0, GENE_LEN-1) for i in range(0, n)]
        for i in c:
            if self.powerGene[i] == 'A':
                self.powerGene[i] = 'C'
            else:
                self.powerGene[i] = 'A'

    def getTiltGene(self):
        return self.tiltGene

    def getPowerGene(self):
        return self.powerGene
    
    def setTiltGene(self, newGene):
        self.tiltGene = newGene

    def setPowerGene(self, newGene):
        self.powerGene = newGene