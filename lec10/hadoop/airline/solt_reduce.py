#!/usr/bin/env python

from operator import itemgetter
import sys

airports = {};

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
   
    # parse the input we got from mapper.py
    airport, lateTime = line.split('\t', 1)
    
    # convert count (currently a string) to int
    try:
        lateTime = int(lateTime)
        
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if airport not in airports.keys():
        airports[airport] = []
    airports[airport].append(lateTime)
time = 0
for airport in airports:
    for lt in airports[airport]:
        if int(lt) > 0:
            time = time + lt
print '%s\t%sminutes' % ('total-time', time)
    

