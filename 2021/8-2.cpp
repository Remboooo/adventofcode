#include <iostream>
#include <fstream>
#include <string>
#include <utility>
#include <set>
#include "util.h"

constexpr static std::array<std::array<bool, 7>, 10> digits {{
        {true, true, true, true, true, true, false},
        {true, true, false, false, false, false, false},
        {true, false, true, true, false, true, true},
        {true, true, true, false, false, true, true},
        {true, true, false, false, true, false, true},
        {false, true, true, false, true, true, true},
        {false, true, true, true, true, true, true},
        {true, true, false, false, false, true, false},
        {true, true, true, true, true, true, true},
        {true, true, true, false, true, true, true}
}};

int get_digit(const std::string &seg, std::vector<char> &order) {
    std::array<bool, 7> constellation{};
    for (char c : seg) constellation.at(index_of(order, c)) = true;
    return index_of(digits, constellation);
}

void process_file(std::ifstream& infile) {
    std::string line;
    long answer = 0;
    while (true) {
        std::getline(infile, line);
        if (infile.eof()) break;
        auto in_out = string_split(line, " \\| ");
        auto in_segs = string_split(in_out.at(0), " ");
        auto out_segs = string_split(in_out.at(1), " ");

        std::vector<char> order {'a', 'b', 'c', 'd', 'e', 'f', 'g'};

        // there is probably a more intelligent way to deduce this, but brute forcing finishes in 100ms for the
        // entire puzzle input, so why bother...
        do {
            std::set<int> digits_found;
            bool success = true;
            for (auto& seg : in_segs) {
                int digit = get_digit(seg, order);
                if (digit < 0 || digits_found.contains(digit)) {
                    success = false;
                    break;
                } else {
                    digits_found.emplace(digit);
                }
            }
            if (success) {
                break;
            }
        } while (next_permutation(order));

        dbg(std::cout << "Order: " << order << std::endl);

        int result = accumulate<int>(out_segs, 0, [&order](int v, const std::string& seg){ return 10*v + get_digit(seg, order); });
        dbg(std::cout << "Result: " << result << std::endl);
        answer += result;
    }
    std::cout << "Answer: " << answer << std::endl;
}

int main(int argc, const char** argv) {
    return run(argc, argv, base_name(__FILE__), process_file);
}
