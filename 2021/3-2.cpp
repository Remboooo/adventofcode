#include <iostream>
#include <fstream>
#include <string>
#include <limits>
#include "util.h"

void process_file(std::ifstream& infile) {
    std::vector<unsigned> numbers{};
    std::string line;
    unsigned chars = 0;
    while (std::getline(infile, line)) {
        unsigned num = 0;
        unsigned line_chars = 0;
        for (const char c : line) {
            num <<= 1;
            if (c == '1') num |= 1;
            ++line_chars;
        }
        if (line_chars) numbers.push_back(num);
        chars = std::max(chars, line_chars);
    }

    auto ox_candidates = numbers;
    auto co2_candidates = numbers;

#if defined(DEBUG)
    std::cout << "CO2 candidates " << co2_candidates << std::endl;
    std::cout << "OX candidates " << ox_candidates << std::endl;
#endif

    for (unsigned pos = chars; pos > 0; --pos) {
        unsigned bitmask = 1 << (pos-1);
        unsigned one_count = std::count_if(
                numbers.begin(), numbers.end(), [bitmask](unsigned v) { return v & bitmask; }
        );
        bool one_is_popular = (one_count > numbers.size() / 2);
        bool tie = (one_count == numbers.size() / 2);

#if defined(DEBUG)
        std::cout << "pos " << pos << ": ";
        if (tie) {
            std::cout << "tie";
        } else {
            std::cout << (one_is_popular ? "popular 1" : "popular 0");
        }
        std::cout << std::endl;
#endif

        if (ox_candidates.size() > 1) {
            bool want_one = one_is_popular || tie;
            keep_if(ox_candidates, [bitmask, want_one](unsigned v) { return want_one == bool(v & bitmask); });
        }

        if (co2_candidates.size() > 1) {
            bool want_one = !one_is_popular && !tie;
            keep_if(co2_candidates, [bitmask, want_one](unsigned v) { return want_one == bool(v & bitmask); });
        }

#if defined(DEBUG)
        std::cout << "OX candidates " << ox_candidates << std::endl;
        std::cout << "CO2 candidates " << co2_candidates << std::endl;
#endif
    }

    if (ox_candidates.size() != 1 || co2_candidates.size() != 1) throw UserError("Not exactly 1 candidate left for OX/CO2");

    unsigned co2 = co2_candidates.at(0);
    unsigned ox = ox_candidates.at(0);

    std::cout << "OX " << ox << ", CO2 " << co2 << ", answer = " << (co2 * ox) << std::endl;
}

int main(int argc, const char** argv) {
    return run(argc, argv, file_name(__FILE__), process_file);
}
