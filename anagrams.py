"""
Please submit the attendance form! https://goo.gle/TechX24InterviewAttendance

Return elements that appear exactly once in a list of strings
"""

def inOnce(words):
    dict = {}
    finalw = []
    for word in words:
        if word in dict:
            dict[word] += 1
        else:
            dict[word] = 1
    
    for key, value in dict.items():
        if value == 1:
            finalw.append(key)
        else:
            continue

    return finalw

"""
Given two strings, string_a and string_b, determine whether any anagram of string_b, occurs as a substring of string_a.

Two words are anagrams if one word can be obtained by rearranging the letters of the other word. 

Anagram: word -> drow, orwd, ...
NOT anagram: word -> dow, roww, ...

The check should not be case sensitive. Punctuation and spaces should be ignored. (i.e., consider only letters)

string_a = "crowd", string_b = "word" ("rowd") --> TRUE
string_a = "crowd", string_b = "no" --> FALSE
string_a = "Here come dots and lines that helped build America", string_b = "The Morse Code" --> TRUE

string_a = "orcwd", string_b = "word" --> FALSE
"orcw", "rcwd"

B: "abb"
substring: "aab"
"""

def anagram(string_a, string_b):
    size = len(string_b)
    dictB = {}
    substrings = []
    for c in range(len(string_a)):
        if c == (len(string_a) - len(string_b)):
            substrings.append(string_a[c: c + size])
            break
        else:
            substrings.append(string_a[c: c + size])

    for char in string_b:
        if char in dictB:
            dictB[char] += 1
        else:
            dictB[char] = 1

    for s in substrings:
        subDict = {}
        for char in s:
            if char in subDict:
                subDict[char] += 1
            else:
                subDict[char] = 1

        if dictB == subDict:
            return True
        else:
            continue

    return False
