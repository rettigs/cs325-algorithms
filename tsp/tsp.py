#!/usr/bin/python

import getopt
import itertools
import math
import random as rand
import sys

class City(object):
    def __init__(self, ID, x, y):
        self.ID = ID
        self.x = int(x)
        self.y = int(y)

    def __repr__(self):
        return str(self.ID)

    def dist(self, other):
        return int(round(math.sqrt(pow(self.x - other.x, 2) + pow(self.y - other.y, 2))))

# Globals
debug = 0

def main():

    # Defaults
    infile = sys.stdin
    outfile = sys.stdout
    alg = tsp_nn
    lengthOnly = False

    # Parse arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "di:o:a:lh")
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        sys.exit(2)
    for o, a in opts:
        if o == "-d":
            debug += 1
        elif o == "-i":
            infile = open(a, 'r')
        elif o == "-o":
            outfile = open(a, 'w')
        elif o == "-a":
            alg = eval("tsp_"+a)
        elif o == "-l":
            lengthOnly = True
        else:
            usage()

    # Read file
    cities = readFile(infile)

    # Calculate path
    path = alg(cities)
    length = getPathLength(path)

    # Write output
    writeFile(outfile, path, length, lengthOnly)

def usage():
    print 'Usage: {0} [-h] [-i infile] [-o outfile] [-d]...'.format(sys.argv[0])
    print '\t-h\tview this help'
    print '\t-i\tspecify an input file of cities, defaults to stdin'
    print '\t-o\tspecify an output file for best path, defaults to stdout'
    print '\t-a\tspecify algorithm to use: tsp_order'
    print '\t-l\tdon\'t write the path, just the length'
    print '\t-d\tenable debug messages; use -dd for more even more messages'
    sys.exit(2)

def readFile(infile):
    return [City(*line.split()) for line in infile.readlines()]

def writeFile(outfile, path, length, lengthOnly):
    outfile.write(str(length)+"\n")
    if not lengthOnly:
        for city in path:
            outfile.write(str(city)+"\n")

def getPathLength(path):
    length = 0
    for i in xrange(len(path)):
        length += path[i-1].dist(path[i])
    return length

def tsp_order(cities):
    '''Returns a path in the order that the cities were given.'''
    return list(cities)

def tsp_brute(cities):
    '''Returns the shortest path by brute forcing all possible paths.'''
    paths = itertools.permutations(cities)
    length_paths = [(getPathLength(path), path) for path in paths]
    return min(length_paths)[1]

def tsp_nn(cities, startIndex=0):
    '''Returns a path generated using a greedy nearest-neighbor algorithm from the city at the given starting index.'''
    remaining = list(cities)
    curCity = remaining.pop(startIndex)
    path = [curCity]
    while len(remaining) > 0:
        minLength = None
        minCity = None
        for i in xrange(len(remaining)):
            newCity = remaining[i]
            newLength = curCity.dist(newCity)
            if newLength < minLength or minLength is None:
                minLength = newLength
                minCity = newCity
        path.append(minCity)
        remaining.remove(minCity)
        curCity = minCity
    return path

def tsp_nnbest(cities):
    '''Returns the best path generated using a greedy nearest-neighbor algorithm from every possible starting city.'''
    minLength = None
    minPath = None
    for i in xrange(len(cities)):
        path = tsp_nn(cities, i)
        length = getPathLength(path)
        if length < minLength or minLength is None:
            minLength = length
            minPath = path
    return minPath

def genetic(path, iters=1000, mutations=1):
    '''Attempts to improve the given path using a genetic algorithm.  Performs up to the given number of mutations per iteration, but always at least 1.'''
    newPath = list(path) # Copy the path
    for i in xrange(iters):

        oldLength = getPathLength(newPath)

        # Generate a random number of mutations
        switches = []
        for j in xrange(0, rand.randint(1, mutations)):
            # For each mutation, pick 2 random cities and swap the order in which they are visited
            nums = range(len(newPath))
            a = nums.pop(rand.randint(0, len(nums)-1))
            b = nums.pop(rand.randint(0, len(nums)-1))
            switches.append((a, b))

        # Perform the mutations
        for a, b in switches:
            newPath[a], newPath[b] = newPath[b], newPath[a]
            #print "Switching cities {} and {}".format(a, b)

        newLength = getPathLength(newPath)

        # If the mutation was detrimental, undo it
        if newLength > oldLength:
            #print "New path length {} is greater than {}; undoing mutation".format(newLength, oldLength)
            for a, b in switches[::-1]:
                newPath[a], newPath[b] = newPath[b], newPath[a]
        else:
            print "New path length {} is less than {}; keeping mutation".format(newLength, oldLength)

    return newPath

def tsp_ordergen(cities, iters=1000, mutations=1):
    '''Returns a path that begins as the given city order and is then improved by a genetic algorithm.'''
    path = tsp_order(cities)
    path = genetic(path)
    return path

if __name__ == '__main__':
    main()
