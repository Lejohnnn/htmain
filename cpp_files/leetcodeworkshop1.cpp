#include <stack>
#include <string>

class Solution {
public:
    bool isValid(std::string s) {
        std::stack<char> st; // Create an empty stack to store opening brackets

        for (char c : s) { // Loop through each character in the string
            if (c == '(' || c == '{' || c == '[') {
                // If the character is an opening bracket
                st.push(c); // Push it onto the stack
            } else {
                // If the character is a closing bracket
                if (st.empty() || 
                    (c == ')' && st.top() != '(') || 
                    (c == '}' && st.top() != '{') || 
                    (c == ']' && st.top() != '[')) {
                    return false; // The string is not valid
                }
                st.pop(); // Otherwise, pop the opening bracket from the stack
            }
        }

        return st.empty(); // If the stack is empty, all brackets are matched
    }
};
