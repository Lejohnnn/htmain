# Problem 2: Find Unique
# You are given a list of integers called nums. The numbers stored in the list appear twice except for one number, which only appears once. Write a method that finds this number.

# Example
# Input: [1, 4, 1, 3, 5, 5, 4]
# Output: 3

# Explanation: 3 is the only number in the list that appears once.
# Use left and right arrow keys to adjust the split region size

from collections import defaultdict

def find_unique(nums):
  counts = {}
  for number in nums:
      if number in counts:
        counts[number] += 1
      else: 
        counts[number] = 1
  
  for key, value in counts.items():
    if value == 1:
      return key

find_unique([1, 4, 1, 3, 5, 5, 4])