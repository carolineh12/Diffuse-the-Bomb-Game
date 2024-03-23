#include <iostream>
#include <vector>
#include <string>
#include <bitset>

class TargetConverter {
private:
    std::vector<bool> _component;

public:
    // Constructor
    TargetConverter(const std::vector<bool>& component) : _component(component) {}

    // Function to get integer state
    int get_int_state() {
        std::vector<bool> state = _component;
        std::vector<std::string> value;

        for (bool pin : state) {
            // changes bit to boolean
            value.push_back(pin ? "1" : "0");
        }

        // prints the string without spaces
        std::string bitString = "";
        for (const std::string& bit : value) {
            bitString += bit;
        }

        // changes to integer
        int intValue = std::stoi(bitString, nullptr, 2);
        return intValue;
    }
};

int main() {
    // Example TargetConverter instance
    std::vector<bool> component = {false, true, true, false};
    TargetConverter obj(component);

    // Example usage
    int target = 13;
    std::cout << "Target: " << target << std::endl;

    std::string b_target = std::bitset<5>(target).to_string();
    std::replace(b_target.begin(), b_target.end(), ' ', '0'); // zfill equivalent
    std::cout << "Binary target: " << b_target << std::endl;

    std::vector<bool> l_target;
    for (char bit : b_target) {
        // changes bit to boolean
        l_target.push_back(bit == '1');
    }
    std::cout << "Boolean target: ";
    for (bool bit : l_target) {
        std::cout << bit << " ";
    }
    std::cout << std::endl;

    std::vector<std::string> bitStringList;
    for (bool bit : l_target) {
        // changes boolean to string
        bitStringList.push_back(bit ? "1" : "0");
    }
    std::string bitString = "";
    for (const std::string& bit : bitStringList) {
        bitString += bit;
    }
    std::cout << "Bitstring: " << bitString << std::endl;

    // changes to integer
    int value = std::stoi(bitString, nullptr, 2);
    std::cout << "Value: " << value << std::endl;

    return 0;
}
