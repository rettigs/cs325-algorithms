#!/usr/bin/python

import getopt
import itertools
import math
import sys

class Tile(object):
    def __init__(self, value):
        self.value = int(value)
        self.maxValue = int(value)

    def __repr__(self):
        return "({}, {}, {})".format(self.value, self.maxValue, self.maxPath)

    def __cmp__(self, other):
        return self.value.__cmp__(other.value)

# Globals
debug = 0

def main():

    # Defaults
    infile = sys.stdin
    outfile = sys.stdout

    # Parse arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "di:o:h")
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
        else:
            usage()

    # Read file
    array = readFile(infile)

    printArray(array)

    # Calculate path
    value, path = getMaxPath(array)

    # Write output
    writeFile(outfile, value, path)

def usage():
    print 'Usage: {0} [-h] [-i infile] [-o outfile] [-d]...'.format(sys.argv[0])
    print '\t-h\tview this help'
    print '\t-i\tspecify an input file, defaults to stdin'
    print '\t-o\tspecify an output file, defaults to stdout'
    print '\t-d\tenable debug messages; use -dd for more even more messages'
    sys.exit(2)

def readFile(infile):
    '''Reads the array into memory, where each tile is a tuple containing the tile's value, the maximum value attainable to the tile, and the path to get there.'''
    array = [[Tile(value) for value in line.split()] for line in infile.readlines()[2:]]
    h = len(array)
    w = len(array[0])
    for y in xrange(h):
        for x in xrange(w):
            array[y][x].coords = (y, x)
            array[y][x].maxPath = [(y, x)]
    return array

def writeFile(outfile, value, path):
    outfile.write(str(value)+"\n")
    outfile.write(str(len(path))+"\n")
    for tileCoord in path:
        outfile.write("{} {}\n".format(*tileCoord))

def printArray(array):
    for line in array:
        print line
    print ""

def getMaxPath(array):
    '''Returns the path through the array with the highest value in the format of (value, path).'''
    h = len(array)
    w = len(array[0])
    maxTile = array[0][0]
    for y in xrange(h):
        for x in xrange(w):
            cur = array[y][x]
            print "Checking tile at {}".format(cur.coords)

            if y > 0:
                prev = array[y-1][x]
                newMaxValue = prev.maxValue + cur.value
                #print newMaxValue
                if newMaxValue >= maxTile.maxValue:
                    cur.maxValue = newMaxValue
                    cur.maxPath = list(prev.maxPath)
                    cur.maxPath.append(cur.coords)

            if x > 0:
                prev = array[y][x-1]
                newMaxValue = prev.maxValue + cur.value
                #print newMaxValue
                if newMaxValue >= maxTile.maxValue:
                    cur.maxValue = newMaxValue
                    cur.maxPath = list(prev.maxPath)
                    cur.maxPath.append(cur.coords)

            #print "curTile is now: {}".format(cur)
            if cur.maxValue > maxTile.maxValue:
                #print "curTile is now new maxTile"
                maxTile = cur
                #print "maxTile unchanged"

            printArray(array)

    return (maxTile.maxValue, maxTile.maxPath)

if __name__ == '__main__':
    main()
