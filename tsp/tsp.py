#!/usr/bin/python

from __future__ import division
import getopt
import itertools
import math
import os
import random as rand
import sys

class City(object):
    def __init__(self, ID, x, y):
        self.ID = ID
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        #return "City({})".format(self.ID)
        return "{}".format(self.ID)

    def __repr__(self):
        return str(self.ID)

    def dist(self, other):
        return int(round(math.sqrt(pow(self.x - other.x, 2) + pow(self.y - other.y, 2))))

class CityPair(object):
    def __init__(self, a, b):
        self.pair = frozenset([a, b])

    def __repr__(self):
        return "({}, {})".format(*self.pair)

    def __eq__(self, other):
        return self.pair == other.pair

    def __hash__(self):
        return hash(self.pair)

    def dist(self):
        a, b = self.pair
        return a.dist(b)

# Globals
debug = 0
verbose = 0

def main():

    # Defaults
    infile = sys.stdin
    outfile = sys.stdout
    infilename = None
    outfilename = None
    algs = [g_order]
    pickupMode = False
    lengthOnly = False

    # Parse arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "dvi:o:a:plh")
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        sys.exit(2)
    for o, a in opts:
        if o == "-d":
            global debug
            debug += 1
        elif o == "-v":
            global verbose
            verbose += 1
        elif o == "-i":
            infilename = a
        elif o == "-o":
            outfilename = a
        elif o == "-a":
            algs = map(eval, a.split(','))
        elif o == "-p":
            pickupMode = True
        elif o == "-l":
            lengthOnly = True
        else:
            usage()

    # Read file
    if pickupMode and os.path.isfile(outfilename):
        infile = open(outfilename, 'r')
    elif infilename is not None:
        infile = open(infilename, 'r')
    cities = readFile(infile)
    infile.close()

    # Calculate path
    alg = algs[0]
    path = alg(cities)
    length = getPathLength(path)
    if verbose > 0: sys.stderr.write("{:<28}{}\n".format("Length after "+alg.__name__+": ", length))
    for alg in algs[1:]:
        path = alg(path)
        length = getPathLength(path)
        if verbose > 0: sys.stderr.write("{:<28}{}\n".format("Length after "+alg.__name__+": ", length))

    # Write output
    if outfilename is not None:
        outfile = open(outfilename+".tmp", 'w')
    if pickupMode:
        writeInputFile(outfile, path)
    else:
        writeOutputFile(outfile, path, length, lengthOnly)
    outfile.close()
    if outfilename is not None:
        os.rename(outfilename+".tmp", outfilename)

def usage():
    print 'Usage: {0} [-h] [-i infile] [-o outfile] [-a alg(s)] [-p] [-l] [-v]... [-d]...'.format(sys.argv[0])
    print '\t-h\tview this help'
    print '\t-i\tspecify an input file of cities, defaults to stdin'
    print '\t-o\tspecify an output file for best path, defaults to stdout'
    print '\t-a\tspecify algorithm(s) to use, comma-delimited; must start with generator, which may be followed by any number of filters'
    print '\t-p\t"pickup mode"; write outfile using input format and read it back again if it exists'
    print '\t-l\tdon\'t write the path, just the length'
    print '\t-v\tenable more verbose messages; use -vv for more even more messages'
    print '\t-d\tenable debug messages; use -dd for more even more messages'
    sys.exit(2)

def readFile(infile):
    return [City(*line.split()) for line in infile.readlines()]

def writeOutputFile(outfile, path, length, lengthOnly):
    outfile.write(str(length)+"\n")
    if not lengthOnly:
        for city in path:
            outfile.write(repr(city)+"\n")

def writeInputFile(outfile, path):
    for city in path:
        outfile.write("{} {} {}\n".format(city.ID, city.x, city.y))

def getPathLength(path):
    length = 0
    for i in xrange(len(path)):
        length += path[i-1].dist(path[i])
    return length

def g_order(cities):
    '''Returns a path in the order that the cities were given.'''
    return list(cities)

def g_brute(cities):
    '''Returns the shortest path by brute forcing all possible paths.'''
    paths = itertools.permutations(cities)
    length_paths = [(getPathLength(path), path) for path in paths]
    return min(length_paths)[1]

def g_nn(cities, startIndex=0):
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

def g_nnbest(cities):
    '''Returns the best path generated using a greedy nearest-neighbor algorithm from every possible starting city.'''
    minLength = None
    minPath = None
    for i in xrange(len(cities)):
        path = g_nn(cities, i)
        length = getPathLength(path)
        if length < minLength or minLength is None:
            minLength = length
            minPath = path
    return minPath

def g_nncommon(cities):

    # Get all the greedy nearest neighbor paths
    paths = []
    for i in xrange(len(cities)):
        path = g_nn(cities, i)
        length = getPathLength(path)
        paths.append((path, length))

    # Create a new graph with the edges weighted by how common they were.
    edges = {} # Dict of CityPairs (edges) with weights to show the most common paths
    for path, pathLength in paths:
        for i in xrange(len(path)):
            pair = CityPair(path[i-1], path[i])
            pairDist = pair.dist()
            if pair not in edges:
                edges[pair] = 0
            edges[pair] += 1/pairDist

    minLength = None
    minPath = None
    for i in xrange(len(cities)):
        path = _nngraph(cities, edges, i)
        length = getPathLength(path)
        if length < minLength or minLength is None:
            minLength = length
            minPath = path
    return minPath

def _nngraph(cities, edges, startIndex=0):
    '''Given a graph as a list of edges, returns a path generated using a greedy nearest-neighbor algorithm from some edge.'''
    remaining = list(cities)
    curCity = remaining.pop(startIndex)
    path = [curCity]
    while len(remaining) > 0:
        minLength = None
        minCity = None
        for i in xrange(len(remaining)):
            newCity = remaining[i]
            newPair = CityPair(curCity, newCity)
            if newPair in edges:
                newLength = edges[newPair]
            else:
                newLength = 0
            if newLength > minLength or minLength is None:
                minLength = newLength
                minCity = newCity
        path.append(minCity)
        remaining.remove(minCity)
        curCity = minCity
    return path

def f_adjacentswap(path):
    '''Attempts to shorten a path by swapping adjacent cities.'''
    path = list(path) # Copy the path
    while True:
        swapped = False
        for i in xrange(len(path)):
            a, b, c, d = path[i-3], path[i-2], path[i-1], path[i]
            oldLength = a.dist(b) + b.dist(c) + c.dist(d)
            newLength = a.dist(c) + c.dist(b) + b.dist(d)
            if newLength < oldLength:
                path[i-2], path[i-1] = path[i-1], path[i-2]
                swapped = True
        if not swapped: # Stop checking if we went through a whole round without swapping.
            break
    return path

def f_swap(path):
    '''Attempts to shorten a path by swapping cities.  Similar to the adjacent swap algorithm, but doesn't only swap adjacent cities.  Based on genetic.'''
    newPath = list(path)
    while 1:
        oldPath = list(newPath) # Copy the path
        newPath = list(oldPath) # Copy the path
        for i in xrange(len(path)):
            for j in xrange(len(path)):

                oldLength = getPathLength(newPath)

                # Perform mutation
                newPath[i], newPath[j] = newPath[j], newPath[i]

                newLength = getPathLength(newPath)

                # If the mutation was detrimental, undo it
                if newLength > oldLength:
                    #print "New path length {} is greater than {}; undoing mutation".format(newLength, oldLength)
                    newPath[i], newPath[j] = newPath[j], newPath[i]
                elif newLength < oldLength:
                    if verbose > 0: print "New path length {} is less than {}; keeping mutation".format(newLength, oldLength)
                    
        if (getPathLength(newPath) == getPathLength(oldPath)):
            break

    return newPath

def f_inject(path):
    '''Attempts to shorten a path by injecting cities into edges.'''
    path = list(path) # Copy the path
    l = len(path)
    for i in xrange(len(path)): # Iterate over edges to be injected
        a, b = i, (i+1)%l # Indices to edge to be injected
        for j in xrange(len(path)): # Iterate over cities to inject
            t, u, v = j, (j+1)%l, (j+2)%l # Indices to city to inject and its neighbors
            if u != a and u != b:
                oldLength = path[a].dist(path[b]) + path[t].dist(path[u]) + path[u].dist(path[v])
                newLength = path[a].dist(path[u]) + path[u].dist(path[b]) + path[t].dist(path[v])
                if newLength < oldLength:
                    #print path
                    #print "putting {} in between {} and {}".format(path[u], path[a], path[b])
                    path.insert(b, path.pop(u)) # Removes u and inserts it between a and b
                    #print path
                    #print "---"
    return path

def f_injectiter(path):
    '''Attempts to shorten a path by injecting cities into edges.  Repeats until injecting fails'''
    newPath = list(path) # Copy the path
    while 1:
        oldPath = list(newPath) # Copy the path
        newPath = f_inject(oldPath)
        if (getPathLength(newPath) == getPathLength(oldPath)):
            break
    return newPath

def f_genswap(path, iters=100000, mutations=3):
    '''Attempts to improve the given path using a genetic algorithm.  Performs up to the given number of mutations per iteration, but always at least 1.'''
    newPath = list(path) # Copy the path
    for i in xrange(iters):

        oldLength = getPathLength(newPath)

        # Generate a random number of mutations
        switches = []
        for j in xrange(rand.randint(1, mutations+1)):
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
        elif newLength < oldLength:
            if verbose > 1: print "New path length {} is less than {}; keeping mutation".format(newLength, oldLength)

    return newPath

def f_geninject(path, iters=100000):
    l = len(path)
    cityrange = range(l)
    for x in xrange(iters):
        i, j = rand.sample(cityrange, 2)
        a, b = i, (i+1)%l # Indices to edge to be injected
        t, u, v = j, (j+1)%l, (j+2)%l # Indices to city to inject and its neighbors
        if u != a and u != b:
            oldLength = path[a].dist(path[b]) + path[t].dist(path[u]) + path[u].dist(path[v])
            newLength = path[a].dist(path[u]) + path[u].dist(path[b]) + path[t].dist(path[v])
            if newLength < oldLength:
                path.insert(b, path.pop(u)) # Removes u and inserts it between a and b
                if verbose > 1: print "Keeping mutation"
    return path

def f_geninjectmulti(path, iters=10000):
    l = len(path)
    cityrange = range(l)
    for x in xrange(iters):
        oldLength = getPathLength(path)

        # Generate a random number of mutations
        randf = rand.random()
        if randf > 0.9:
            m = 3
        elif randf > 0.6:
            m = 2
        else:
            m = 1
        mutations = [rand.sample(cityrange, 2) for m in xrange(m)]

        # Perform the mutations
        for i, j in mutations:
            path.insert(i, path.pop(j))
            if debug > 1: print "Injecting city {} before city {}".format(j, i)

        newLength = getPathLength(path)

        # If the mutation was detrimental, undo it
        if newLength > oldLength:
            #print "New path length {} is greater than {}; undoing mutation".format(newLength, oldLength)
            for i, j in mutations[::-1]:
                path.insert(j, path.pop(i))
        elif newLength < oldLength:
            if verbose > 1: print "New path length {} is less than {}; keeping mutation".format(newLength, oldLength)

    return path

def g_growinject(cities):
    '''Starts with a loop between 3 cities and then injects new cities based on which ones increase the path length the least.'''
    path = cities[:3]
    rem = cities[3:]

    while len(rem) > 0:
        # For each iteration, we add one city by calculating the path increase of injecting each remaining city into each edge in the current path and using the best one.
        deltas = [] # List of deltas of the form (path length, a index, b index)
        for i in xrange(len(path)): # For each edge given by a city 'c' and the city before it 'a'...
            for j in xrange(len(rem)): # For each possible city that could be injected 'b'...
                # Calculate the increase in path length caused by that injection.
                a, b, c = path[i-1], rem[j], path[i]
                ilen = a.dist(c)
                flen = a.dist(b) + b.dist(c)
                delta = flen - ilen
                deltas.append((delta, i, j))
        _, i, j = min(deltas)
        path.insert(i, rem.pop(j))
    return path

def g_gcm(cities):
    '''"Greedy Cluster Merge"; always connects the closest two groups of cities until they are all connected.'''
    paths = [[city] for city in cities]
    while len(paths) > 1:
        if debug > 0: print paths
        distances = [] # List of distances of the format (distance, source path, destination path, source city index, destination city index)
        for s in paths:
            for d in paths:
                if s is not d:
                    for i in xrange(-1, 1):
                        for j in xrange(-1, 1):
                            distance = s[i].dist(d[j])
                            distances.append((distance, s, d, i, j))
                            if debug > 1: print "distance between {} and {}: {}".format(s[i], d[j], distance)
        _, s, d, i, j = min(distances)
        if debug > 0: print "min is between {} and {}".format(s, d)
        if debug > 1: print "--------------------"
        if i == 0:
            s.reverse()
        if j == -1:
            d.reverse()
        s.extend(d)
        paths.remove(d)
    return paths[0]

if __name__ == '__main__':
    main()
