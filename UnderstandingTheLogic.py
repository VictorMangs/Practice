

def degree(nums):
    if len(nums)<=2:
        return 1
    #Get left right index and get count for checking the degree        
    #Use dictionaries
    l = {}
    r = {}
    c = {}
    #Enumerate to get count and value
    for ind,val in enumerate(nums):
        if val in l:
            pass
        else:
            l[val]=ind
        r[val]=ind
        c[val]=c.get(val,0)+1
    
    #Initialize ans and highest degree
    ans = len(nums)
    deg = max(c.values())
    
    #Scroll through count dictionary and calculate if degree matches value
    for i in c:
        if c[i]==deg:
            ans = min(ans,r[i]-l[i]+1)
            print(ans)

    return ans


def sortByBits(arr):
    #dictionary to hold binary lists based on how many 1s
    arr2 = {}
    #Arr3 to replace arr1
    arr3 = []
    
    #Loop through array and count bins for each element and add to dict
    for i in arr:
        numbin = bin(i).count(str('1'))
        if numbin not in arr2:
            arr2[numbin] = [i]
        else:
            arr2[numbin].append(i)
    
    #Sort the keys
    x = list(sorted(arr2.keys()))
    
    #Loop through sorted keys and add sorted lists from dict to arr3
    for i in x:
        arr3+=sorted(arr2[i])

    #Return  
    arr = arr3
    return arr


def backspaceCompare(s,t):
    a = []
    b = []
    
    for i in s:
        if i=='#':
            try:
                a.pop()
            except:
                pass
        else:
            a.append(i)
        
    for i in t:
        if i=='#':
            try:
                b.pop()
            except:
                pass
        else:
            b.append(i)

    return a==b


nums = [1,2,2,3,1]

ans = degree(nums)

