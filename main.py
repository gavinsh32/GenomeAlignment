# main.py
# Gavin Haynes, Sam Beal
# Simulate and evolve virtual cannons.

import simulator
import population
import cannon

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

class Alignment:
    def __init__(self, sequence1, sequence2):
        self.seq1 = sequence1
        self.seq2 = sequence2
        self.rows = len(self.seq1) + 1
        self.cols = len(self.seq2) + 1
        self.scoringMatrix = self.makeScoringMatrix()

    # Create the scoring matrix for sequences 1 and 2
    def makeScoringMatrix(self):
        m = 4       # match/mismatch value
        gap = -2

        # Make initial scoring matrix
        scoring = [[i * -2 for i in range(0, self.cols)] for _ in range(0, self.rows)]

        for i in range(0, self.rows):
            scoring[i][0] = i * -2

        # Calculate Scoring Matrix
        for i in range(1, self.rows):
            for j in range(1, self.cols):
                a = self.seq1[i-1]           # Char in seq1
                b = self.seq2[j-1]           # Char in seq2
                d = scoring[i-1][j-1]

                # Calculate 3 possible prior moves
                diag = d + (m if a == b else -m)
                right = scoring[i][j-1] + gap
                down = scoring[i-1][j] + gap

                # Set to max of three
                scoring[i][j] = max(diag, max(right, down))
        
        return scoring

    # Untested global alignment
    def traverseScoringMatrix(self):
        pass

    def align(self):
        s = self.seq1
        t = self.seq2
        i, j = 0, 0
        score = 0
        while i < self.rows-1 and j < self.cols-1:
            score += self.scoringMatrix[i][j]
            self.scoringMatrix[i][j] = 'X'
            right = self.scoringMatrix[i][j+1]
            diag = self.scoringMatrix[i+1][j+1]
            down = self.scoringMatrix[i+1][j]
            choice = max(right, max(diag, down))
            if diag == choice:
                i += 1
                j += 1
            elif right == choice:
                i += 1
            else:
                j += 1

        right = self.scoringMatrix[i][j+1]
        diag = self.scoringMatrix[i+1][j+1]
        down = self.scoringMatrix[i+1][j]

        score += max(right, max(diag, down))

        return score, s, t

    def __str__(self):
        # For clarity
        rows = len(self.seq1) + 1
        cols = len(self.seq2) + 1

        text = '         '
        for c in seq2:
            text += f'{c:4}'
        text += '\n'

        for i in range(0, rows):
            text += '  ' if i == 0 else seq1[i - 1] + ' '
            for j in range(0, cols):
                text += f'{repr(self.scoringMatrix[i][j]):>4}'
            text += '\n'

        return text

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