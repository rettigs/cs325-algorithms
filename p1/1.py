#!/usr/bin/env python

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

slopes = [-2, -1, 0, 1, 2]
intercepts = [9, 27, 54, 95, 96]

print a1(slopes, intercepts)
print [True, False, False, True, True]
