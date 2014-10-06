#!/usr/bin/env python

def getVisible(slopes, intercepts):
    visibility = [True for n in xrange(len(slopes))]
    for j in xrange(len(slopes)):
        for i in xrange(j+1, len(slopes)):
            for k in xrange(i+1, len(slopes)):
                # compute intersection
                jkIntersectionX = getIntersection(slopes[j], intercepts[j], slopes[k], intercepts[k])
                jkIntersectionY = getY(slopes[k], intercepts[k], jkIntersectionX)
                i_Y = getY(slopes[i], intercepts[i], jkIntersectionX)
                if jkIntersectionY > i_Y:
                    visibility[i] = False
                return visibility

def getY(s, i, x):
    return s*x+i
    
def getIntersection(s1, i1, s2, i2):
   return (i2 - i1) / (s1 - s2)
   

slopes = [-2, -1, 0, 1, 2]
intercepts = [9, 27, 54, 95, 96]

print getVisible(slopes, intercepts)
print [True, False, False, True, True]
