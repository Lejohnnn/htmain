def left_sum(nums):
    left = [0]
    total = 0
    for number in nums:
        total += number
        left.append(total)
    return left[0:-1]

def right_sum(nums):
    right = [0]
    total = 0
    nums = nums[::-1]
    for number in nums:
        total += number
        right.append(total)
    return right[0:-1][::-1]

def left_right_difference(nums):
    left_nums = left_sum(nums)
    right_nums = right_sum(nums)
    diffs = []
    for i in range(len(left_nums)):
        diffs.append(abs(left_nums[i] - right_nums[i]))
    print(left_nums)
    print(right_nums)
    print(diffs)
    return diffs
    
left_right_difference([10,4,8,3])