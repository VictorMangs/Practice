def productExceptSelf(arr):
  prefix = 1
  helper = [1]*len(arr)

  for i in range(len(arr)):
    helper[i] = prefix
    prefix *= arr[i]
    print(helper)
  postfix = 1

  for i in range(len(arr)-1,-1,-1):
    helper[i] *= postfix
    postfix *= arr[i]
    print(postfix)
  print(helper)

productExceptSelf([1,2,0,4,5])

x = "sksksk"
if x.isal