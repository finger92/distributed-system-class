#!/usr/bin/python
#
#  WordCount reducer in Python
import sys

candidate_list = {}
#print "LongValueSum:" + presi + classifier.classify(d) + "\t" + "1"

## collect (key,val) pairs from sort phase
for line in sys.stdin:
    try:
        candidate, count = line.strip().split("\t", 1)
        
        if candidate not in candidate_list:
            candidate_list[candidate] = int(count)
        else:
            candidate_list[candidate] += int(count)
    except ValueError, err:
        sys.stderr.write("Value ERROR: %(err)s\n%(data)s\n" % {"err": str(err), "data": line})
## emit results
for candidate, count in candidate_list.items():
    print candidate + "\t" + str(count);

