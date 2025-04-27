# Problem 3: Most Common Word
# Given a string of words separated by spaces, find the word that appears the most in the string. Feel free to assume that there will be no ties.

# Example
# Input: "hello world hello hello world hi"
# Ouput: "hello"

# Explanation: hello appears the most often (3 times) in the string.

from collections import defaultdict

def most_common_word(s):
  words = s.split(" ")
  word_count = {}
  most = 0
  common = " "
  for wrd in words:
    if wrd in word_count.keys():
      word_count[wrd] += 1
    else: 
      word_count[wrd] = 1

  for key, value in word_count.items():
    if value > most:
      most = value
      common = key
  return common


most_common_word("hello world hello hello world hi")