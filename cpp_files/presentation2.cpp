#include <iostream>
#include <vector>
#include <algorithm> // For max function
using namespace std;

int maxSubarraySum(const vector<int>& arr) {

    // Handles Edge Case: Empty Array
    if (arr.empty()) {
        cout << "The array is empty. No subarray exists." << endl;
        return 0; 
    }

    int maxSum = arr[0]; // Initialize with the first element
    int currentSum = 0;

    for (int num : arr) {
        currentSum += num;         // Add the current element to the running sum
        maxSum = max(maxSum, currentSum); // Update the maximum sum
        if (currentSum < 0) {      // Reset current sum if it goes below zero
            currentSum = 0;
        }
    }

    return maxSum;
}

int main() {
    vector<int> arr = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
    int result = maxSubarraySum(arr);

    cout << "The maximum subarray sum is: " << result << endl;
    return 0;
}
