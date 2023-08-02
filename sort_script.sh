#!/bin/bash
cd $1/Output/
sort -n +1 +2 -3 results -o SortedResult
# should sort from high to low for columns 1 and 2, and from low to high in column 3 (the scores are negative)