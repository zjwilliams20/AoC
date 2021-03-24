#########################
# day 20
#########################

import re
import numpy as np


class Piece():
    '''Piece contains an ID and data as a NumPy array'''


    def __init__(self, idNum, data):
        self.id = idNum
        self.data = data

    def frontEdges(self):
        '''only get front edges; flip the third and fourth edges to preserve
           an edge after piece rotation
        '''
        return np.array([self.data[0,:], self.data[:,-1], 
                         np.flip(self.data[-1,:]), np.flip(self.data[:,0])])

    def allEdges(self):
        '''get edges and flipped edges'''
        front = self.frontEdges()
        back = np.fliplr(front)
        return np.vstack((front, back))

    def rotate(self, k=1):
        '''rotate data k*90 degrees CCW'''
        self.data = np.rot90(self.data, k=k)

    def flipud(self): self.data = np.flipud(self.data)
    def fliplr(self): self.data = np.fliplr(self.data)

    def match(self, other):
        '''check if two pieces match each other'''
        aFront = self.frontEdges()
        bAll = other.allEdges()
        diffs = np.array([aFront - bAll[i] for i in range(len(bAll))])
        for bIdx, arr in enumerate(diffs):
            for aIdx, row in enumerate(arr):
                if all(row == 0):
                    return (aIdx, bIdx)
        return False

    def orient(self, other):
        '''orient self to fit other'''

        aI, bI = other.match(self)
        pieceMap = {0:6, 1:7, 2:4, 3:5}
        if bI < 4:
            self.flipud()
            aI, bI = other.match(self)
        self.rotate((bI - pieceMap[aI]) % 4)

    def strip(self):
        '''remove borders'''
        self.data = self.data[1:-1,1:-1]

    def __eq__(self, other): return self.id == other.id
    def __repr__(self): return self.__str__()

    def __str__(self):
        fill = True
        pieceStr = f'Piece {self.id}:\n'
        for rI, row in enumerate(self.data):
            for nI, num in enumerate(row):
                if (rI in [0, len(self.data)-1] or 
                    nI in [0, len(self.data)-1] or fill):
                    if num == 1 : pieceStr += '#'
                    else: pieceStr += '.'
                else: pieceStr += ' '
            pieceStr += '\n'
        return pieceStr + '\n'


class Puzzle():
    '''Puzzle provides an interface for solving an arbitrary list of Pieces'''


    def __init__(self, pieces):
        self.pieces = pieces.copy()
        self.dim = int(np.sqrt(len(pieces)))
        self.pieceSz = len(pieces[0].data)
        
        # initialize to null pieces
        dummyData = np.zeros((self.pieceSz, self.pieceSz))
        self.built = [
            [Piece(0, dummyData) for _ in range(self.dim)] 
                                 for _ in range(self.dim)
        ]

        # set the first three pieces
        self.start()

        # fill in the rest
        self.build()
        
    def start(self):
        '''put together the first three pieces'''

        corners, _, _ = enPuzzle(self.pieces)
        a = corners[0]
        b = self.find(a)
        c = self.find(a)
        self.pieces.remove(a)
        
        # get the matching edges
        aI, bI = a.match(b)

        # flip a if necessary
        if aI in [0, 3]:
            a.rotate(2)
        b.orient(a)

        # flip a and b if necessary
        aI, cI = a.match(c)
        if aI == 0:
            a.flipud()
            b.flipud()
        elif aI == 3:
            a.fliplr()
            b.fliplr()
        c.orient(a)

        # update match indicies
        _, bI = a.match(b)
        _, cI = a.match(c)

        # update class information
        self.built[0][0] = a
        if bI == 4:     # b below a
            self.built[1][0] = b
            self.built[0][1] = c
        elif cI == 4:   # b right of a 
            self.built[0][1] = b
            self.built[1][0] = c

    def find(self, piece):
        '''find a matching piece, remove from the list'''

        for t in self.pieces:
            if piece != t and piece.match(t):
                self.pieces.remove(t)
                return t
        raise AssertionError(f"could't match piece: {piece}")

    def findRight(self, piece):
        '''find a matching piece for the right edge and remove from list'''

        for t in self.pieces:
            match = piece.match(t)
            if piece != t and match:
                if match[0] == 1:
                    self.pieces.remove(t)
                    return t
        raise AssertionError(f"could't match piece: {piece}")

    def findBelow(self, piece):
        '''find a matching piece for the bottom edge'''

        for t in self.pieces:
            match = piece.match(t)
            if piece != t and match:
                if match[0] == 2:
                    self.pieces.remove(t)
                    return t
        raise AssertionError(f"could't match piece: {piece}")

    def build(self):
        '''build the puzzle, filling them in top to bottom left to right'''

        iterInd = [(i, j) for i in range(self.dim) for j in range(self.dim-1)]
        iterInd.pop(0)
        for ind in iterInd:
            row, col = ind[0], ind[1]
            current = self.built[row][col]
            if col == 0 and row != self.dim-1:
                below = self.findBelow(current)
                right = self.findRight(current)
                below.orient(current)
                right.orient(current)
                self.built[row+1][col] = below
                self.built[row][col+1] = right
            else:
                right = self.findRight(current)
                right.orient(current)
                self.built[row][col+1] = right

    def strip(self):
        '''remove borders from every piece, update piece size'''

        for row in self.built:
            for piece in row:
                piece.strip()
        self.pieceSz = len(self.built[0][0].data)

    def hunt(self, monsterInd, h, l):
        '''
        Hunt the seamonster, i.e. try to find the pattern in the grid rotated
        and flipped to any of its 8 orientations. Return the number of spaces
        in the grid that aren't a sea monster.
        '''
        
        # get current grid
        init = self.full()

        def reverseInd(init, ind, k):
            '''reverse the grid from an arbitrary orientation specified by k'''
            # rotate indicies
            for rot in range(k % 4):
                ind = [(x[1], init.shape[0]-1-x[0]) for x in ind]
            # flip indicies
            if k >= 4:
                ind = [(x[0], init.shape[0]-1-x[1]) for x in ind]
            return ind
        
        # get the indicies to check
        iterInd = np.array([(i, j) for i in range(init.shape[0] - h+1) 
                                   for j in range(init.shape[1] - l+1)])
        
        target = len(monsterInd)
        huntedInd = set()

        for k in range(8):

            # reset seas
            seas = init
            # manipulate as needed
            if k >= 4:
                seas = np.fliplr(init)
            seas = np.rot90(seas, k % 4)

            # check all relevant indicies
            for ind in iterInd:
                
                y, x = ind[0], ind[1]
                mY, mX = zip(*monsterInd)
                mX = np.array(mX)
                mY = np.array(mY)
                if sum(seas[y+mY, x+mX]) == target:
                    hInd = reverseInd(seas, zip(y+mY, x+mX), k)
                    hInd = zip(y+mY, x+mX)
                    huntedInd.update(hInd)
        return int(np.sum(init) - len(huntedInd))

    def full(self, k=0):
        '''return the current puzzle rotated as np array'''

        full = np.zeros((self.dim*self.pieceSz, self.dim*self.pieceSz))
        for rI, row in enumerate(self.built):
            for tI, piece in enumerate(row):
                full[rI*self.pieceSz:(rI+1)*self.pieceSz, 
                     tI*self.pieceSz:(tI+1)*self.pieceSz] = piece.data
        return np.rot90(full, k)

    def __repr__(self):
        return self.__str__()

    def __str__(self, ind=[], k=0):
        puzzStr = ''
        full = self.full(k)
        for rI, row in enumerate(self.full(k)):
            for nI, num in enumerate(row):
                if (rI, nI) in ind: puzzStr += 'O'
                elif num == 1:      puzzStr += '#'
                else:               puzzStr += '.'
            puzzStr += '\n'
        return puzzStr + '\n'


with open('input/day20', 'r') as file:
    pieces = []    
    for line in file.readlines():
        if 'Tile' in line:
            match = re.search(r'(\d+)', line)
            pieceNum = int(match.group(1))
            pieceData = np.zeros((0,10), dtype=int)
        elif line != '\n':
            pieceData = np.vstack(
                (pieceData, [0 if c == '.' else 1 for c in line.strip()])
            )
        else:
            pieces.append(Piece(pieceNum, pieceData))


def enPuzzle(pieces):
    '''divide puzzle into piece types'''

    corners = []
    borders = []
    middles = []
    for a in pieces:
        aFront = a.frontEdges()
        nMatches = 0
        for b in pieces:
            if a == b: continue
            if a.match(b): nMatches += 1
        if nMatches == 2:   corners.append(a)
        elif nMatches == 3: borders.append(a)
        elif nMatches == 4: middles.append(a)
        else: raise AssertionError('huh?')
    return corners, borders, middles

# part 1
corners, borders, middles = enPuzzle(pieces)
print(f'part 1: {np.prod([c.id for c in corners])}')

# part 2
p = Puzzle(pieces)
p.strip()


def makeMonster(pattern):
    '''create a monster from an arbitrary pattern of "#"'''

    monsterInd= [(i, j) for i, line in enumerate(pattern) for j, char in enumerate(line) if char == '#']
    h, l = len(pattern), len(pattern[0])
    return monsterInd, h, l


# make seamonster
seamonster = ['                  # ',
              '#    ##    ##    ###',
              ' #  #  #  #  #  #   ']
monsterInd, h, l = makeMonster(seamonster)

# how rough was it
habitatWaterRoughness = p.hunt(monsterInd, h, l)
print(f'part 2: {habitatWaterRoughness}')
