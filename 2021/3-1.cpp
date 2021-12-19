#include <iostream>
#include <fstream>
#include <string>
#include "util.h"

void process_file(std::ifstream& infile) {
    int lines = 0;
    std::vector<int> counts{};
    std::string line;
    while (std::getline(infile, line)) {
        int pos = 0;
        for (const char c : line) {
            if (lines == 0) {
                counts.push_back(c == '1');
            } else {
                if (c == '1') counts.at(pos) += 1;
            }
            ++pos;
        }
        if (pos) ++lines;
    }
    int gamma = 0;
    for (int count : counts) {
        gamma <<= 1;
        if (count > (lines/2)) gamma |= 1;
    }
    int epsilon = ((1 << counts.size()) - 1) ^ gamma;
    std::cout
        << "counts: " << counts
        << ", size = " << counts.size()
        << ", lines = " << lines
        << ", gamma = " << gamma
        << ", epsilon = " << epsilon
        << ", answer = " << (epsilon * gamma)
        << std::endl;
}

int main(int argc, const char** argv) {
    return run(argc, argv, base_name(__FILE__), process_file);
}
