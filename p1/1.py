#!/usr/bin/env python
import random
import sys
import time

def a1(slopes, intercepts):
    visibility = [True for n in xrange(len(slopes))]
    for j in xrange(len(slopes)):
        for i in xrange(j+1, len(slopes)):
            for k in xrange(i+1, len(slopes)):
                # compute intersection
                jkIntersectionY = slopes[j] * (intercepts[j] - intercepts[k]) + intercepts[j] * (slopes[k] - slopes[j])
                i_Y = slopes[i] * (intercepts[j] - intercepts[k]) + intercepts[i] * (slopes[k] - slopes[j])
                if jkIntersectionY > i_Y:
                    visibility[i] = False
    return visibility
	
def a2(slopes, intercepts):
    visibility = [True for n in xrange(len(slopes))]
    for j in xrange(len(slopes)):
        for i in xrange(j+1, len(slopes)):
            for k in xrange(i+1, len(slopes)):
				# break if line has already been marked as not visible
				if visibility[i] != False:
					# compute intersection
					jkIntersectionY = slopes[j] * (intercepts[j] - intercepts[k]) + intercepts[j] * (slopes[k] - slopes[j])
					i_Y = slopes[i] * (intercepts[j] - intercepts[k]) + intercepts[i] * (slopes[k] - slopes[j])
					if jkIntersectionY > i_Y:
						visibility[i] = False
    return visibility
	
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
			visibileIndices.pop()
			a3actualWork(slope, intercept, visibleSlopes, visibleIntercepts)

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
        a1res = a1(testSet[0], testSet[1])
        if a1res != testSet[2]:
            print "A1 test {} failed:".format(i)
            print "\tGot {}, should be {}.".format(a1res, testSet[2])

        a2res = a2(testSet[0], testSet[1])
        if a2res != testSet[2]:
            print "A2 test {} failed:".format(i)
            print "\tGot {}, should be {}.".format(a2res, testSet[2])

        a3res = a3(testSet[0], testSet[1])
        if a3res != testSet[2]:
            print "A3 test {} failed:".format(i)
            print "\tGot {}, should be {}.".format(a3res, testSet[2])

    print "Correctness tests complete."

def timeTest():
    print "Lines\tA1 Time\tA2 Time\tA3 Time"
    for i in xrange(100, 1100, 100):
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

        print "{}\t{.3f}\t{.3f}\t{.3f}".format(i, a1time, a2time, a3time)

if __name__ == '__main__':
    if sys.argv[1] == "test":
        correctTest()
    elif sys.argv[1] == "time":
        timeTest()
