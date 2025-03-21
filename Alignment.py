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

        score += max(right, max(diag, down))

        return score, s, t

    def __str__(self):
        # For clarity
        rows = len(self.seq1) + 1
        cols = len(self.seq2) + 1

        text = '         '
        for c in self.seq2:
            text += f'{c:4}'
        text += '\n'

        for i in range(0, rows):
            text += '  ' if i == 0 else self.seq1[i - 1] + ' '
            for j in range(0, cols):
                text += f'{repr(self.scoringMatrix[i][j]):>4}'
            text += '\n'

        return text