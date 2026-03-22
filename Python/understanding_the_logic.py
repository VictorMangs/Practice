def lengthOfLongestSubstring(s: str) -> int: 
	d = {}
	l = 0
	ans = 0

	for r,char in enumerate(s):

		ans = max(ans,r-l)

		while char in d and l<=r:
			left_char = s[l]
			d[left_char] -= 1
			if d[left_char] == 0: 
				d.pop(left_char)
			l+=1
			
		d[char] = d.get(char,0)+1
		
	ans = max(ans,len(s)-l)
	return ans