#!/usr/bin/python

import getopt
import itertools
import math
import sys

class Tile(object):
    def __init__(self, value):
        self.value = int(value)
        self.maxValue = int(value)
        self.prev = None

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

    # Calculate stuff
    maxTile = getMaxTile(array)
    maxPath = getPath(array, maxTile)

    # Write output
    writeFile(outfile, maxTile.maxValue, maxPath)

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

def getMaxTile(array):
    '''Returns the tile with the greatest path through the array.'''
    h = len(array)
    w = len(array[0])
    maxTile = array[0][0]
    for y in xrange(h):
        for x in xrange(w):
            cur = array[y][x]

            if y > 0:
                prev = array[y-1][x]
                newMaxValue = prev.maxValue + cur.value
                if newMaxValue >= cur.maxValue:
                    cur.maxValue = newMaxValue
                    cur.prev = prev

            if x > 0:
                prev = array[y][x-1]
                newMaxValue = prev.maxValue + cur.value
                if newMaxValue >= cur.maxValue:
                    cur.maxValue = newMaxValue
                    cur.prev = prev

            if cur.maxValue > maxTile.maxValue and (y == h - 1 or x == w - 1):
                maxTile = cur

    return maxTile

def getPath(array, tile):
    '''Given an array and the coords to a tile, returns the path to that tile.'''
    path = [tile.coords]
    while(tile.prev):
        path.append(tile.coords)
        tile = tile.prev
    return path[::-1]

if __name__ == '__main__':
    main()
