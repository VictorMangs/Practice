

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
    arr2 = {}
    arr3 = []
    
    for i in arr:
        numbin = bin(i).count(str('1'))
        if numbin not in arr2:
            arr2[numbin] = [i]
        else:
            arr2[numbin].append(i)
    
    x = list(sorted(arr2.keys()))
    
    for i in x:
        arr3+=sorted(arr2[i])
        
    arr = arr3
    return arr



nums = [1,2,2,3,1]

ans = degree(nums)

