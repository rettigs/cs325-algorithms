#!/usr/bin/python

import getopt
import itertools
import math
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
    alg = tsp_order

    # Parse arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "di:o:a:h")
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
            alg = eval(a)
        else:
            usage()

    # Read file
    cities = readFile(infile)

    # Calculate path
    path = alg(cities)
    length = getPathLength(path)

    # Write output
    writeFile(outfile, path, length)

def usage():
    print 'Usage: {0} [-h] [-i infile] [-o outfile] [-d]...'.format(sys.argv[0])
    print '\t-h\tview this help'
    print '\t-i\tspecify an input file of cities, defaults to stdin'
    print '\t-o\tspecify an output file for best path, defaults to stdout'
    print '\t-a\tspecify algorithm to use: tsp_order'
    print '\t-d\tenable debug messages; use -dd for more even more messages'
    sys.exit(2)

def readFile(infile):
    return [City(*line.split()) for line in infile.readlines()]

def writeFile(outfile, path, length):
    outfile.write(str(length)+"\n")
    for city in path:
        outfile.write(str(city)+"\n")

def getPathLength(path):
    length = 0
    for i in xrange(len(path)):
        length += path[i-1].dist(path[i])
    return length

def tsp_order(cities):
    '''Returns a path in the order that the cities were given.'''
    return cities

def tsp_brute(cities):
    '''Returns the shortest path by brute forcing all possible paths.'''
    paths = itertools.permutations(cities)
    length_paths = [(getPathLength(path), path) for path in paths]
    return min(length_paths)[1]

if __name__ == '__main__':
    main()
