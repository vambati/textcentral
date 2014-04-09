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
    	total_count_arr =  []
        try:
	    for current_word,count in group:
		    count_arr = count.split('\t')

		    # Initialize 
		    if(total_count_arr==[]):
			total_count_arr = [int(x) for x in count_arr]

		    # Sum along all the lines 
		    for i in range(0,len(count_arr)):
			    total_count_arr[i] += int(count_arr[i])
        except ValueError:
            pass
	print "%s%s%s" % (current_word, separator, total_count_arr)

if __name__ == "__main__":
    main()
