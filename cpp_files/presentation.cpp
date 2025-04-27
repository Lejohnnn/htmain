#include <iostream>
#include <vector>
using namespace std;

int findSecondLargest(const vector<int>& arr) {

    // Handles Edge Case: array of length less than 2 [10]
    if (arr.size() < 2) {
        cout << "Array must contain at least two elements." << endl;
        return -1; 

    int largest = arr[0];
    int secondLargest = arr[0];
    bool foundSecondLargest = false;

    for (int i = 1; i < arr.size(); ++i) {
        if (arr[i] > largest) {
            secondLargest = largest;
            largest = arr[i];
            foundSecondLargest = true;
        } else if (arr[i] > secondLargest && arr[i] < largest) {
            secondLargest = arr[i];
            foundSecondLargest = true;
        }
    }

     // Handles Edge Case: all array elements are the same [10, 10, 10]
    if (!foundSecondLargest) {
        cout << "No second largest element exists." << endl;
        return -1; 
    }

    return secondLargest;
}
