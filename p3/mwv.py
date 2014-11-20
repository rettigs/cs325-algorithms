#!/usr/bin/env python

import re, sys

# usage: python mwv.py inputfilename solutionfilename

def main(instancefile, solutionfile):
    instance = readinstance(instancefile)
    solution = readsolution(solutionfile)
    checksolution(instance, solution)
        
def readinstance(filename):
    # the first line of the input file gives the number of rows of A
    # the second line of the input file gives the number of columns of A
    # each line thereafter represents a row of space separated entries of A

    f = open(filename,'r')
    nrows = int(f.readline())
    ncols = int(f.readline())

    A = []
    line = f.readline()
    for i in range(nrows):
        lineparse = re.findall(r'[^,;\s]+', line)
        col = []
        for j in range(ncols):
            col.append(int(lineparse[j]))
        A.append(col)
        line = f.readline()
    f.close()
    return [nrows, ncols, A]

def readsolution(filename):
    # first line is the value of the solution
    # second line is the number of grid entries in the solution
    # remaining lines are the grid entries as space separated row col entries as they are visited in order
    # indices must start at 0

    # read in solution value and size
    f = open(filename,'r')
    value = int(f.readline())
    size = int(f.readline())

    # read in grid entries
    walk = []
    for i in range(size):
        line = f.readline()              
        lineparse = re.findall(r'[^,;\s]+', line)
        walk.append([int(lineparse[0]),int(lineparse[1])])
    f.close()

    return [value, size, walk]

def checksolution(instance, solution):
    nrows = instance[0]
    ncols = instance[1]
    A = instance[2]
    value = solution[0]
    size = solution[1]
    walk = solution[2]

    # is the solution feasible?
    if walk[-1][0] == nrows-1 or walk[-1][1] == ncols-1:
        print('walk ends in last row or column, good!')
    else:
        print('walk does not end in last row or column, bad!')
        return
        
    for i in range(size-1):
        if not(walk[i][0]+1 == walk[i+1][0] or walk[i][1]+1 == walk[i+1][1]):
            print('walk does go one row down or one column to right in each step, bad!')
            return
    print('walk is valid, good!')

    # does your walk value match what you say it does?
    calc_value = 0
    for i in range(size):
        calc_value = calc_value + A[walk[i][0]][walk[i][1]]
    if calc_value == value:
        print 'walk value matches what you say,', value, ' - good!'
    else:
        print 'you say the walk has value', value, 'but it has value', calc_value, ' - bad!'

main(sys.argv[1], sys.argv[2])
