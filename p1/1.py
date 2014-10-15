#!/usr/bin/env python
import random
import sys
import time

class Line(object):
    def __init__(self, slope, intercept, visible):
        self.slope = slope
        self.intercept = intercept
        self.visible = visible

    def __repr__(self):
        return "({}, {}, {})".format(self.slope, self.intercept, self.visible)

def toLines(slopes, intercepts, visible):
    lines = []
    for i in xrange(len(slopes)):
        lines.append(Line(slopes[i], intercepts[i], visible))
    return lines

def toLists(lines):
    slopes = []
    intercepts = []
    visible = []
    for l in lines:
        slopes.append(l.slope)
        intercepts.append(l.intercept)
        visible.append(l.visible)
    return [slopes, intercepts, visible]

def a1(slopes, intercepts):
    lines = toLines(slopes, intercepts, True)
    for nj, j in enumerate(lines):
        for ni, i in enumerate(lines[nj+1:], nj+1):
            for nk, k in enumerate(lines[ni+1:], ni+1):
                # compute intersection
                jkIntersectionY = j.slope * (j.intercept - k.intercept) + j.intercept * (k.slope - j.slope)
                i_Y = i.slope * (j.intercept - k.intercept) + i.intercept * (k.slope - j.slope)
                if jkIntersectionY > i_Y:
                    i.visible = False
    return lines
	
def a2(slopes, intercepts):
    lines = toLines(slopes, intercepts, True)
    for nj, j in enumerate(lines):
        for ni, i in enumerate(lines[nj+1:], nj+1):
            for nk, k in enumerate(lines[ni+1:], ni+1):
                # break if line has already been marked as not visible
                if i.visible:
                    # compute intersection
                    jkIntersectionY = j.slope * (j.intercept - k.intercept) + j.intercept * (k.slope - j.slope)
                    i_Y = i.slope * (j.intercept - k.intercept) + i.intercept * (k.slope - j.slope)
                    if jkIntersectionY > i_Y:
                        i.visible = False
    return lines
	
def a3(slopes, intercepts):
    visibleSlopes = []
    visibleIntercepts = []
    visibleIndices = []
    visibility = [False for n in xrange(len(slopes))]
    for i in xrange(0, len(slopes)):
        a3actualWork(slopes[i], intercepts[i], visibleSlopes, visibleIntercepts, visibleIndices, visibility, i)
    return visibility
	
def a3actualWork(slope, intercept, visibleSlopes, visibleIntercepts, visibleIndices, visibility, i):
	if len(visibleSlopes) < 2:
		visibleSlopes.append(slope)
		visibleIntercepts.append(intercept)
		visibility[i] = True
		visibleIndices.append(i)
	else:
		k = len(visibleSlopes) - 1
		j = k - 1
		jkIntersectionY = visibleSlopes[j] * (visibleIntercepts[j] - visibleIntercepts[k]) + visibleIntercepts[j] * (visibleSlopes[k] - visibleSlopes[j])
		i_Y = slope * (visibleIntercepts[j] - visibleIntercepts[k]) + intercept * (visibleSlopes[k] - visibleSlopes[j])
		if jkIntersectionY >= i_Y:
			visibleSlopes.append(slope)
			visibleIntercepts.append(intercept)
			visibility[i] = True
			visibleIndices.append(i)
		else:
			visibleSlopes.pop()
			visibleIntercepts.pop()
			visibility[visibleIndices[k]] = False
			visibleIndices.pop()
			a3actualWork(slope, intercept, visibleSlopes, visibleIntercepts, visibleIndices, visibility, i)

def a4(slopes, intercepts):
    lines = toLines(slopes, intercepts, True)
    vlines = []

    # Start with the first two lines since they have to be visible if they're the only ones.
    vlines.append(lines[0])
    vlines.append(lines[1])

    for i in xrange(2, len(lines)):
        vlines.append(lines[i])
        _removeCovered(vlines)

    return lines

def _removeCovered(vlines):
    '''Given a list of visible lines for which another line was appended, recursively remove the 2nd to last element if it became covered by the new line.'''
    if len(vlines) < 3: # All lines are visible if there are only 1 or 2.
        return vlines
    else:
        a, b, c = vlines[-3:] # Get the last 3 elements of vlines.
        intersectionY = a.slope * (a.intercept - b.intercept) + a.intercept * (b.slope - a.slope)
        newline_Y = c.slope * (a.intercept - b.intercept) + c.intercept * (b.slope - a.slope)
        if newline_Y > intersectionY: # If line b is covered, remove it and recurse.
            b.visible = False
            vlines.pop(-2)
            return _removeCovered(vlines)
        else: # If line b is still visible, do nothing.
            return vlines

def buildRandomNumbersList(size):
	return random.sample(range(-9000, 9000), size)	#arbitrary range

def correctTest():
    testSets = [
        [[-1, 0, 1], [3, 0, -1], [True, False, True]],
        [[-2, -1, 0, 1, 2], [9, 27, 54, 95, 96], [True, False, False, True, True]],
        [[-2, -1, 0, 1, 2], [0, 0, 0, 0, 0], [True, True, True, True, True]],
        [[-2, -1, 0, 1, 2], [2, 0, 0, -4, -6], [True, False, True, False, True]],
        [[-2, -1, 0, 1, 2], [2, 1, 0, 1, 2], [True, False, False, False, True]]
    ]

    for (i, testSet) in enumerate(testSets):
        a1res = toLists(a1(testSet[0], testSet[1]))
        if a1res[2] != testSet[2]:
            print "A1 test {} failed:".format(i)
            print "\tGot {}, should be {}.".format(a1res[2], testSet[2])

        a2res = toLists(a2(testSet[0], testSet[1]))
        if a2res[2] != testSet[2]:
            print "A2 test {} failed:".format(i)
            print "\tGot {}, should be {}.".format(a2res[2], testSet[2])

        a3res = a3(testSet[0], testSet[1])
        if a3res != testSet[2]:
            print "A3 test {} failed:".format(i)
            print "\tGot {}, should be {}.".format(a3res[2], testSet[2])

        a4res = toLists(a4(testSet[0], testSet[1]))
        if a4res[2] != testSet[2]:
            print "A4 test {} failed:".format(i)
            print "\tGot {}, should be {}.".format(a4res[2], testSet[2])

    print "Correctness tests complete."

def timeTest():
    print "Lines\tA1 Time\tA2 Time\tA3 Time\tA4 Time"

    for i in xrange(100, 1000, 100):
        slopes = buildRandomNumbersList(i)
        intercepts = buildRandomNumbersList(i)
        slopes.sort()

        a1start = time.time()
        a1res = a1(slopes, intercepts)
        a1time = time.time() - a1start

        a2start = time.time()
        a2res = a2(slopes, intercepts)
        a2time = time.time() - a2start

        a3start = time.time()
        a3res = a3(slopes, intercepts)
        a3time = time.time() - a3start

        a4start = time.time()
        a4res = a4(slopes, intercepts)
        a4time = time.time() - a3start

        print "{}\t{:.3f}s\t{:.3f}s\t{:.3f}s\t{:.3f}s".format(i, a1time, a2time, a3time, a4time)

    for i in xrange(1000, 10000, 1000):
        slopes = buildRandomNumbersList(i)
        intercepts = buildRandomNumbersList(i)
        slopes.sort()

        a3start = time.time()
        a3res = a3(slopes, intercepts)
        a3time = time.time() - a3start

        a4start = time.time()
        a4res = a4(slopes, intercepts)
        a4time = time.time() - a3start

        print "{}\t\t\t{:.3f}s\t{:.3f}s".format(i, a3time, a4time)

def solveTest():
    testSets = [eval(x) for x in open("solve_these.txt", 'r').readlines()]

    for (i, testSet) in enumerate(testSets):
        resultSets = []
        resultSets.append(toLists(a1(testSet[0], testSet[1]))[2])
        resultSets.append(toLists(a2(testSet[0], testSet[1]))[2])
        resultSets.append((a3(testSet[0], testSet[1])))
        resultSets.append(toLists(a4(testSet[0], testSet[1]))[2])
        for j in xrange(len(resultSets)):
            if resultSets[j] != resultSets[0]:
                print "Test Set {}: A{}() result does not match A1() result.".format(i, j+1)
                print "\tA1() result: {}".format(resultSets[0])
                print "\tA{}() result: {}".format(j+1, resultSets[j])
        print resultSets[0]

if __name__ == '__main__':
    if sys.argv[1] == "test":
        correctTest()
    elif sys.argv[1] == "time":
        timeTest()
    elif sys.argv[1] == "solve":
        solveTest()
