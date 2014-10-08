#!/usr/bin/env python

def getVisible(slopes, intercepts):
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

def getY(s, i, x):
    return s*x+i
    
def getIntersection(s1, i1, s2, i2):
   return (i2 - i1) / (s1 - s2)
   

slopes = [-2, -1, 0, 1, 2]
intercepts = [9, 27, 54, 95, 96]

print getVisible(slopes, intercepts)
print [True, False, False, True, True]
