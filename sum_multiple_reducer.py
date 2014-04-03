#!/usr/bin/env python
"""A more advanced Reducer, using Python iterators and generators."""

from itertools import groupby
from operator import itemgetter
import sys

def read_mapper_output(file, separator='\t'):
    for line in file:
        yield line.rstrip().split(separator, 1)

def main(separator='\t'):
    data = read_mapper_output(sys.stdin, separator=separator)
    for current_word, group in groupby(data, itemgetter(0)):
        try:
	    for current_word,count in group:
		    count_arr = count.split('\t')
		    total_count_arr =  [0 for x in range(0,len(count_arr))] 
		    for i in range(0,len(count_arr)):
			    total_count_arr[i] += int(count_arr[i])
	    print "%s%s%s" % (current_word, separator, total_count_arr)
        except ValueError:
            pass

if __name__ == "__main__":
    main()
