# Reverse a string

# empty, single , regular
# index switch

string1 = "wolf"
string2 = "abba"
string3 = ""
string4 = "a"

def reverse(string: str) -> None:
    print(string[::-1])

# reverse(string2)


# Two sum

# nums = [2, 7, 11, 15], target = 9

nums = [2, 7, 11, 15]
target = 9

def two_sum(nums: list[int], target: int) -> list[int]:
    found = {}

    for (index, num) in enumerate(nums):    
        diff = target - num
        if diff in found:
            return [found[diff], index]
        
        found[num] = index
    
    return [-1]
    

# result = two_sum(nums,target)
# print(result)

def palindrome(string: str, ignore: list[str] = [" ",","]) -> bool:
    ###
    # Args: string (str): string to check
    # Returns: boolean (True if palindrome, False if not)
    # ###
    left = 0
    right = len(string) -1

    while left < right:
        left_string = string[left].lower()
        right_string = string[right].lower()

        if left_string in ignore:
            left+=1
        elif right_string in ignore:
            right-=1
        elif left_string == right_string:
            left+=1
            right-=1
        else:
            return False

    return True

palindrome_result = palindrome("")
print(palindrome_result)