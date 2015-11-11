#!/usr/bin/env python

import sys

# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # split the line into words
    words = line.split('","')
    # increase counters
    #for word in words:
        # write the results to STDOUT (standard output);
        # what we output here will be the input for the
        # Reduce step, i.e. the input for reducer.py
        #
        # tab-delimited; the trivial word count is 1
    if float(words[9].split(',')[1])==0:
        #change hours to minutes
        v = int(words[7][0:2])*60+int(words[7][2:4])-(int(words[6][0:2])*60+int(words[6][2:4]))
        print '%s\t%s' % (words[2], v)
