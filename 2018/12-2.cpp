#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <tuple>
#include <chrono>
#include <ctime>

std::vector<bool> get_initial_state(std::string input) {
    std::vector<bool> output(input.size());
    int i = 0;
    for (char c : input) {
        output[i++] = (c == '#');
    }
    return output;
}

void print_state(std::vector<bool> state) {
    for (bool s : state) {
        std::cout << (s ? '#' : '.');
    }
    std::cout << std::endl;
}

std::tuple<std::vector<bool>, int> evolve(std::vector<bool> initial_state, bool matches[], int left_index) {
    for (int i = 0; i < initial_state.size(); i++) {
        if (initial_state[i]) {
            if (i > 1) {
                initial_state.erase(initial_state.begin(), initial_state.begin() + (i - 1));
                left_index += i - 1;
            }
            break;
        }
    }
    for (int i = initial_state.size() - 1; i >= 0; i--) {
        if (initial_state[i]) {
            if (i < initial_state.size() - 1) {
                initial_state.erase(initial_state.begin() + (i + 2), initial_state.end());
            }
            break;
        }
    }

    if (initial_state[0]) {
        initial_state.insert(initial_state.begin(), false);
        left_index -= 1;
    }
    if (initial_state[initial_state.size() - 1]) {
        initial_state.push_back(false);
    }
    std::vector<bool> new_state(initial_state.size());

    int pos = -2;
    int match = 0;
    for (bool c : initial_state) {
        match = ((match << 1) | int(c)) & 0b11111;
        if (pos >= 0) {
            new_state[pos] = matches[match];
        }
        pos++;
    }
    for (; pos < new_state.size(); pos++) {
        match = (match << 1) & 0b11111;
        new_state[pos] = matches[match];
    }

    return std::make_tuple(new_state, left_index);
}

int main(int argc, char* argv[]) {
    if (argc < 2) {

        return -1;
    }
    std::cout << argv[1] << std::endl;
    std::ifstream infile(argv[1]);
    if (infile.fail()) {
        std::cerr << "Could not open file" << std::endl;
        return -1;
    }
    std::string line;
    std::vector<bool> state;

    bool matches[0b100000];

    while (std::getline(infile, line)) {
        if (line.substr(0, 15) == "initial state: ") {
            state = get_initial_state(line.substr(15, std::string::npos));
            print_state(state);
        } else if (line.size() == 10){
            int match = int(line.at(0) == '#') << 4 |
                        int(line.at(1) == '#') << 3 |
                        int(line.at(2) == '#') << 2 |
                        int(line.at(3) == '#') << 1 |
                        int(line.at(4) == '#');
            bool result = (line.at(9) == '#');
            matches[match] = result;
        }
    }

    int left_index = 0;
    for (uint64_t i = 0; i < 1000; i++) {
        std::tie(state, left_index) = evolve(state, matches, left_index);
        std::time_t t = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
        std::cout << std::ctime(&t) << (i + 1) << ": (" << left_index << ") ";
        print_state(state);
    }

    return 0;
}