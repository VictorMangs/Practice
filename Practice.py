import re
###Notes###

##Binary Search (must be sorted) (O-logn)

#-set up left (0) and right (len-1), check ends/return if target
#-while l<r
#-mid = (l+r)//2,check mid/return if target
#-if mid is less l = mid+1, else r = mid-1

#Binary Notes
#Pre-processing - Sort if collection is unsorted.
#Binary Search - Using a loop or recursion to divide search space in half after each comparison.
#Post-processing - Determine viable candidates in the remaining space.


##Two Pointer




##Regex

string = 'Random regex string 0193-5921-1212121-12-3 that works'
pattern = re.compile(r'\d{7}')
lst = pattern.findall(string)

for m in lst:
    print(m)