#!/usr/bin/env python
import random
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
	visibility = [False for n in xrange(len(slopes))]
	for i in xrange(0, len(slopes)):
		a3actualWork(slopes[i], intercepts[i], visibleSlopes, visibleIntercepts, visibility, i)
	return visibility
	
def a3actualWork(slope, intercept, visibleSlopes, visibleIntercepts, visibility, i):
	if len(visibleSlopes) < 2:
		visibleSlopes.append(slope)
		visibleIntercepts.append(intercept)
		visibility[i] = True
	else:
		k = len(visibleLines) - 1
		j = k - 1
		jkIntersectionY = visibleSlopes[j] * (visibleIntercepts[j] - visibleIntercepts[k]) + visibleIntercepts[j] * (visibleSlopes[k] - visibleSlopes[j])
		i_Y = slope * (visibleIntercepts[j] - visibleIntercepts[k]) + intercept * (visibleSlopes[k] - visibleSlopes[j])
		if jkIntersectionY > i_Y:
			visibleSlopes.append(slope)
			visibleIntercepts.append(intercept)
			visibility[i] = True
		else:
			visibleSlopes.pop()
			visibleIntercepts.pop()
			#visibility[
			a3actualWork(slope, intercept, visibleSlopes, visibleIntercepts)

def buildRandomNumbersList(size):
	return random.sample(range(-9000, 9000), size)	#arbitrary range
	
slopes1 = buildRandomNumbersList(100)
intercepts1 = buildRandomNumbersList(100)
slopes1.sort()

slopes = [-2, -1, 0, 1, 2]
intercepts = [9, 27, 54, 95, 96]

#print a1(slopes, intercepts)
#print a2(slopes, intercepts)
#print [True, False, False, True, True]
a1start = time.time()
print a1(slopes1, intercepts1)
a1end = time.time()
print a1end - a1start
a2start = time.time()
print a2(slopes1, intercepts1)
a2end = time.time()
print a2end - a2start