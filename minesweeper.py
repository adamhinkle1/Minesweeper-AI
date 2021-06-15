import random
import re
import time


class Mines:
    def __init__(self, gridsize, numberofmines):
        self.flags = []
        self.__currgrid = [[' ' for i in range(gridsize)] for i in range(gridsize)]
        self.__fail = False;
        self.__currcell = (0, 0)
        emptygrid = [['0' for i in range(gridsize)] for i in range(gridsize)]
        self.__mines = self.__getmines(emptygrid, self.__currcell, numberofmines)
        for i, j in self.__mines:
            emptygrid[i][j] = 'X'
        self.__grid = self.__getnumbers(emptygrid)

    def __getrandomcell(self, grid):
        gridsize = len(grid)

        a = random.randint(0, gridsize - 1)
        b = random.randint(0, gridsize - 1)

        return (a, b)

    def __getneighbors(self, grid, rowno, colno):
        gridsize = len(grid)
        neighbors = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                elif -1 < (rowno + i) < gridsize and -1 < (colno + j) < gridsize:
                    neighbors.append((rowno + i, colno + j))

        return neighbors

    def __getmines(self, grid, start, numberofmines):
        mines = []
        neighbors = self.__getneighbors(grid, *start)

        for i in range(numberofmines):
            cell = self.__getrandomcell(grid)
            while cell == start or cell in mines or cell in neighbors:
                cell = self.__getrandomcell(grid)
            mines.append(cell)

        return mines

    def __getnumbers(self, grid):
        for rowno, row in enumerate(grid):
            for colno, cell in enumerate(row):
                if cell != 'X':
                    values = [grid[r][c] for r, c in self.__getneighbors(grid, rowno, colno)]
                    grid[rowno][colno] = str(values.count('X'))

        return grid

    def __showcells(self, rowno, colno):
        if self.__currgrid[rowno][colno] != ' ':
            return

        self.__currgrid[rowno][colno] = self.__grid[rowno][colno]

        if self.__grid[rowno][colno] == '0':
            for r, c in self.__getneighbors(self.__grid, rowno, colno):
                if self.__currgrid[r][c] != 'F':
                    self.__showcells(r, c)

    def __showgrid(self, grid):
        gridsize = len(grid)
        horizontal = '   ' + (4 * gridsize * '-') + '-'
        toplabel = '     '

        for i in range(gridsize):
            if i < 10:
                toplabel = toplabel + str(i) + '   '
            else:
                toplabel = toplabel + str(i) + '  '

        print(toplabel + '\n' + horizontal)

        for idx, i in enumerate(grid):
            row = '{0:2} |'.format(idx)
            for j in i:
                row = row + ' ' + j + ' |'

            print(row + '\n' + horizontal)

        print('')

    def checkcell(self, cell):
        if not self.__fail:
            self.__currcell = cell
            if self.__grid[cell[0]][cell[1]] == 'X':
                self.__fail = True;

        return self.__currgrid

    def showcurrent(self):
        self.__showcells(*self.__currcell)
        self.__showgrid(self.__currgrid)

    def isfail(self):
        return self.__fail

    def checkmines(self):
        if set(self.__mines) == set(self.flags):
            return True
        else:
            return False



#cell class is a datastructure  to hold the cells location, neighbors, and number of touching mines
class cell:

  def __init__(self, cellLocation, neighbors, cellValue):
    self.cellLocation = cellLocation
    self.neighbors = neighbors
    self.cellValue = cellValue

  #If we need to add a neighbor to the cell
  def addNeighbors(self, adjBlank):
    self.neighbors.append(adjBlank)
  #printing the information on the cell
  def printCell(self):
    print("Cell:", self.cellLocation)
    print("Neighbors:", self.neighbors)
    print("Cell Value:", self.cellValue)


# returns a list of "cells" so we can formulate the equations
def equations(sweeper):
    EQUATIONS = []
    # Check everycell
    size = len(sweeper.checkcell((0, 0)))
    for i in range(size):
        for j in range(size):
            if (i, j) not in sweeper.flags:
                x = getEquations(sweeper, i, j)
                # if the cell that is returned, if their neighbor size is less than 7
                # to ensure that it's not just an island of a tile opened.
                if ((len(x.neighbors) != 0) and (len(x.neighbors) < 7)):
                    EQUATIONS.append(x)

    return EQUATIONS


# Formulating the "cell"
def getEquations(sweeper, row, col):
    gridsize = len(sweeper.checkcell((0, 0)))
    cellValue = sweeper.checkcell((0, 0))[row][col]
    # If the cell is still blank, skip it
    if cellValue == ' ':
        return cell((), [], 0)
    # If the cell is 0, skip it
    if cellValue == 0:
        return cell((), [], 0)
    adjBlanks = []
    if (cellValue == 'X'):
        return cell((), [], 0)
    cellValue = int(cellValue)
    # Formulating the neighboring cells for the cell class
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            elif -1 < (row + i) < gridsize and -1 < (col + j) < gridsize:
                x = (row + i, col + j)
                if sweeper.checkcell((0, 0))[x[0]][x[1]] == ' ':
                    if (x[0], x[1]) in sweeper.flags:
                        cellValue -= 1
                    else:
                        adjBlanks.append((x[0], x[1]))

    # Return the cell, with its neighbors and the cell value
    if cellValue != 0:
        return cell((row, col), adjBlanks, int(cellValue))
    else:
        return cell((), [], 0)


# Picking a random cell
def pickRandom(sweeper):
    # A list of possible cells to choose from
    emptyCells = []
    size = len(sweeper.checkcell((0, 0)))
    for i in range(size):
        for j in range(size):
            # Skip this cell if its a known mine
            if (i, j) in sweeper.flags:
                continue
            elif sweeper.checkcell((0, 0))[i][j] == ' ':
                emptyCells.append((i, j))
    # Pick a random one
    x = random.randint(0, len(emptyCells) - 1)
    return (emptyCells[x])


def getSet(eq):
    l = []
    for c in eq:
        for n in c.neighbors:
            l.append(n)
    s = set(l)
    return s


def truthTable(eq, s):
    X = list(s)
    numVar = len(X)
    numRows = 2 ** numVar
    get_bin = lambda x, n: format(x, 'b').zfill(
        n)  ## lambda function that gets the binary of 'x' as a string, and pads with leading zeros up to 'n' digits

    mapping = {}  # dictionary, will map each cell to their list of neighbors as indices of X

    for c in eq:  # for all the border cells
        mappingValue = []  # list will hold the indices in X, which correspond to the cells neighbors
        for neighbor in c.neighbors:  # go through all neighbors for each cell
            for i in range(numVar):  # iterate through X
                if neighbor == X[i]:  # when the neighbor matches the element in X
                    mappingValue.append(i)  # save the INDEX, noting that this cell has a neighbor at X[i]
        mapping[c] = mappingValue  # cell mapped to list of neighboring X indexes

    codingList = []  # this list will hold potential solutions

    for i in range(numRows):  # for every row in truth table
        coding = get_bin(i, numVar)  # get binary string representation of i
        satisfies = True

        for cell, xList in mapping.items():  # go through mapping dictionary
            goal = int(cell.cellValue)
            sum = 0
            for j in xList:  # get each index from the xList
                if coding[j] == '1':  # if this index value is represented as a 1 on the binary coding
                    sum += 1  # increment sum, indicating this is a mine
            if sum != goal:  # if this doesnt give us the correct amount of neighboring mines
                satisfies = False  # falsify this binary coding

        if satisfies == True:  # if this coding passed through every cells equation
            codingList.append(coding)  # add it as potential solution

    return codingList


def compareCodeListSmart(codeList):
    indexProbablityDict = {}
    print(codeList)

    for j in range(len(codeList[0])):
        key = j
        value = 0
        for i in range(len(codeList)):
            if -1 < i + 1 <= len(codeList):
                value += int(codeList[i][j])
        valueProbablity = value / len(codeList)
        indexProbablityDict[key] = valueProbablity
    print(indexProbablityDict)
    return indexProbablityDict


def mark(probabilityDictionary, s, sweeper):
    flagged = False
    print(probabilityDictionary)
    print(s)
    for index, cord in enumerate(s):
        probility = probabilityDictionary[index]
        print(probility)
        if probility == 0:
            sweeper.checkcell(cord)
            sweeper.showcurrent()
            flagged = True
        elif probility == 1:
            sweeper.flags.append(cord)
            flagged = True
        else:
            print(cord, "not certain")
    return flagged


# These are the quickest and easiest methods to pick a cell
def easySweep(sweeper):
    changed = False
    size = len(sweeper.checkcell((0, 0)))
    for i in range(size):
        for j in range(size):
            check = scanAdjacent(sweeper, i, j)
            if check:
                changed = True
                # sweeper.showcurrent()
    return changed


def scanAdjacent(sweeper, row, col):
    # get grid size, to be used in setting border limits for neighbors
    changed = False
    gridsize = len(sweeper.checkcell((0, 0)))
    cellValue = sweeper.checkcell((0, 0))[row][col]
    if cellValue == ' ':
        return changed
    adjMines = 0
    adjBlanks = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:  # skip the current cell
                continue
            elif -1 < (row + i) < gridsize and -1 < (col + j) < gridsize:  # get adjacent cells
                x = (row + i, col + j)
                # if we already know this adjacent cell is a mine, increment number of adjacent mines
                if x in sweeper.flags:
                    adjMines += 1
                # if this cell is unknown add to adjacent blanks
                elif sweeper.checkcell((0, 0))[x[0]][x[1]] == ' ':
                    adjBlanks.append((x[0], x[1]))
    # if the total number of nearby blank cells + known mines equals the cells value
    if int(cellValue) == (adjMines + len(adjBlanks)):
        s1 = len(set(sweeper.flags))
        [sweeper.flags.append(x) for x in adjBlanks]
        s2 = len(set(sweeper.flags))
        if s2 > s1:
            changed = True
    # if we are already at the limit number of nearby mines, check every blank nearby
    elif int(cellValue) == adjMines:
        changed = True
        for x in adjBlanks:
            sweeper.checkcell(x)
        sweeper.showcurrent()

    return changed


def getAdjacentCells(eq, sizeList):
    if len(eq) < 10:
        return eq
    index = random.randint(0, len(eq) - 1)
    firstCell = eq[index]
    newList = []
    newList.append(firstCell)
    progress = True
    while ((len(newList) < sizeList) and progress):
        progress = False
        for curr in newList:
            i = curr.cellLocation[0]
            j = curr.cellLocation[1]
            for cell in eq:
                ii = cell.cellLocation[0]
                jj = cell.cellLocation[1]
                if ((i == ii) and ((j == jj - 1) or (j == jj + 1))):
                    if cell not in newList:
                        progress = True
                        newList.append(cell)
                elif ((j == jj) and ((i == ii - 1) or (i == ii + 1))):
                    if cell not in newList:
                        progress = True
                        newList.append(cell)
    return newList


start_time = time.time()
gridsize = 40
n_mines = 200
field = Mines(gridsize, n_mines)
field.showcurrent()
count = 0
# Tends to run forever when the system of equations is huge
while not (field.checkmines() or field.isfail()):
    # easiest and quickest way to choose mines
    if easySweep(field):
        continue
    else:
        sizeList = 15
        print("***********Running Truth Table*****************")
        eq = getAdjacentCells(equations(field), sizeList)
        s = getSet(eq)
        codingList = truthTable(eq, s)
        count1 = 0
        flag = False
        while (len(codingList) == 0) and (count1 < 5):
            count1 += 1
            codingList = truthTable(eq, s)
        if count1 != 5:
            nextMovesList = compareCodeListSmart(codingList)
            flag = mark(nextMovesList, s, field)
            field.checkmines()
            field.showcurrent()

        if (not flag):
            count += 1
        if (not flag) and (count == 5):
            count = 0
            if len(field.flags) != n_mines:
                randomCell = pickRandom(field)
                print("Random pick:", randomCell)
                field.checkcell(randomCell)
                field.showcurrent()

field.showcurrent()

if field.checkmines():
    if not field.isfail():
        print('we win')
else:
    print('failed')
print("--- %s seconds ---" % (time.time() - start_time))