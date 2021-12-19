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

    auto get_candidate = [numbers, chars](bool want_popular){
        auto candidates = numbers; // make a copy

#if defined(DEBUG)
        std::cout << "Finding candidates with " << (want_popular ? "popular" : "unpopular") << " bits" << std::endl;
#endif

        for (unsigned pos = chars; pos > 0; --pos) {
            unsigned bitmask = 1 << (pos - 1);
            unsigned one_count = count_if(candidates, [bitmask](unsigned v) { return v & bitmask; });

            bool one_is_popular = (one_count > (candidates.size() / 2));
            bool tie = (one_count*2 == candidates.size());

#if defined(DEBUG)
            std::cout
                << "count " << one_count << " 1bits, " << (candidates.size() - one_count) << " 0bits; "
                << "popular " << one_is_popular << ", tie " << tie << std::endl;
#endif

            bool want_one;
            if (tie) {
                want_one = want_popular;
            } else {
                want_one = (one_is_popular == want_popular);
            }

            keep_if(candidates, [bitmask, want_one](unsigned v) { return want_one == bool(v & bitmask); });

#if defined(DEBUG)
            std::cout << "candidates " << std::hex << candidates << std::dec << std::endl;
#endif

            if (candidates.size() == 1) return candidates.at(0);
        }

        throw UserError("Not exactly 1 candidate left");
    };

    auto ox = get_candidate(true);
    auto co2 = get_candidate(false);

    std::cout << std::hex << "OX " << ox << ", CO2 " << co2 << std::dec << ", answer = " << (co2 * ox) << std::endl;
}

int main(int argc, const char** argv) {
    return run(argc, argv, base_name(__FILE__), process_file);
}
