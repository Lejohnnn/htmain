# Problem 2: Minimum Size Sublist Sum
# Given a list of of positive integers nums and a positive integer target return the minimum length of a sublist whose sum is greater than or equal to target. If there is no such sublist return 0 instead.

# Recall that a sublist is a contiguous, non-empty sequence of elements within the list.

# Example 1:

# Input: target = 7, nums = [2,3,1,2,4,3]
# Output: 2
# Explanation: The sublist [4,3] has the minimal length under the problem constraint.
# Example 2:

# Input: target = 4, nums = [1,4,4]
# Output: 1
# Example 3:

# Input: target = 11, nums = [1,1,1,1,1,1,1,1]
# Output: 0

def min_sublist_len(nums, target):
    if(sum(nums) < target):
        return 0
    if target in nums:
        return 1


    x = 1
    start = 0
    count = 0
    for i in range(0, len(nums) -1):
        if (sum(nums[start:x]) == target):
            print(nums[start:x])
            if (count == 0):
                count = len(nums[start:x])
            start += 1
            x += 1
            i = 0
        elif (sum(nums[start:x]) < target):
            print(nums[start:x])
            x += 1
        elif (sum(nums[start:x]) > target):
            print(nums[start:x])
            start += 1
            x += 1
            i = 0




min_sublist_len([2,3,1,2,4,3], 7)