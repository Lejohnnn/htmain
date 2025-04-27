#include <vector>
#include <stack>

std::vector<int> dailyTemperatures(std::vector<int>& temperatures) {
    
    int n = temperatures.size();
    std::vector<int> answer(n, 0); // Initialize the answer array with 0
    std::stack<int> st; // Stack to keep track of indices of temperatures

    for (int currentDayIndex = 0; currentDayIndex < n; ++currentDayIndex) {
        // While the stack is not empty and the current temperature is greater than the temperature at the index stored at the top of the stack
        while (!st.empty() && temperatures[currentDayIndex] > temperatures[st.top()]) {

            int prevDayIndex = st.top(); // Get the index of the previous day

            st.pop(); // Remove it from the stack

            answer[prevDayIndex] = currentDayIndex - prevDayIndex; // Calculate the number of days waited (current index - index of prev day)
        }

        // If stack is empty:
        st.push(currentDayIndex); // Push the current day's index onto the stack
    }

    return answer;
}