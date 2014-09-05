#!/usr/bin/python
'''
THIS PROGRAM IS PROVIDED WITHOUT ANY WARRANTY; YOU CAN USE IT IN ANY WAY YOU WANT
'''

from sys import argv
from math import sin, cos, tan, atan, pi, sqrt

help = '''
It's a tiny script which calculates circle transformation parameters for drawing orthographic projections of the globe, like the one on the USSR state emblem.
Globe is all about circles, and circles are seen as ellipses on the orthographic projection; to draw one, you can clone a base circle, apply width scale and rotation transformations to it, and cut the visible part of its curve.
While it's easy to calculate width scale coefficient and rotation angle for latitude circles, it's somewhat more complicated for meridian circles.
That's what this script is for: it's given a number of meridians for a globe hemisphere (e. g., 6 if it's splitted into 7 sectors at meridian angles 0/7*pi, 1/7*pi, ... 7/7*pi, first and last one being hemisphere edges) and an optional pitch angle (typically 45 deg.) and outputs above-named parameters for meridians between 0 and 90 deg. (you can draw the rest by mirroring).

Usage: '''+argv[0]+''' [NUMBER OF MERIDIANS] [PITCH ANGLE]
E. g.: '''+argv[0]+''' 6 45
'''

n = 7
ang_prj = pi/4
if len(argv)>1:
    n = int(argv[1])+1
    if len(argv)>2:
        ang_prj = int(argv[2])/360.0*2*pi
else:
    print help

def main(ang_prj, ang_mrd):
    ang={}
    ang[0] = atan(cos(pi/2-ang_mrd)*tan(ang_prj))
    ang[1] = atan(cos(ang_mrd)*tan(ang[0]))
    ang[2] = atan(tan(ang_mrd)*sin(ang[1]))
    ang[3] = atan(tan(ang[2])/cos(ang[1]))
    ang[4] = pi/2-ang[1]
    ang[5] = atan(tan(ang[4])/cos(ang[3]))
    ang[6] = ang[3]+ang_prj
    ang[7] = atan(sin(ang[6])*tan(ang[5]))
    # Angle between the surface of the meridian cut of the globe sphere and the projection surface
    # its cos is the width scale coefficient which should be applied to the globe circle to get an ellipse of the meridinan cut projection
    ang[8] = atan(1/sqrt(1/(tan(ang[6])*tan(ang[6]))+1/(tan(ang[7])*tan(ang[7]))))
    # Angle between the major axis of the elliptic projection of the meridian cut and the vertical axis of the projection surface
    # it is the angle which the ellipse should be rotated by to get the meridian cut projection
    ang[9] = atan(cos(ang[6])*tan(ang[5]))
    print 'Width scale: '+str(cos(ang[8]))
    print 'Rotation angle: '+str(ang[9]/pi*180)+' deg.'

# From pi*1/n to pi*(n div 2)/n (for odd n) or to pi*((n div 2)-1)/n (for even n)
for m in xrange(0, n//2+n%2):
    print 'Meridian angle: pi*'+str(m)+'/'+str(n)
    main(ang_prj, pi*m/n)
    print
