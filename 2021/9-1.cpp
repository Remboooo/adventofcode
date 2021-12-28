#include <iostream>
#include <fstream>
#include <string>
#include <utility>
#include "util.h"


std::vector<std::vector<int>> read_heightmap(std::ifstream& infile) {
    std::vector<std::vector<int>> result;
    for (std::string line; !std::getline(infile, line).eof();) {
        result.push_back(transform<int>(line, [](char c) { return c - '0'; }));
    }

    return result;
}

void process_file(std::ifstream& infile) {
    auto h = read_heightmap(infile);
    dbg(std::cout << std::hex << h << std::dec << std::endl);

    pad2d(h, 1, 10);

    int sum = 0;

    for (unsigned x = 1; x < h[0].size() - 1; ++x) {
        for (unsigned y = 1; y < h.size() - 1; ++y) {
            auto v = h[y][x];
            if (v < h[y-1][x] && v < h[y+1][x] && v < h[y][x-1] && v < h[y][x+1]) {
                sum += 1+v;
            }
        }
    }

    std::cout << "Answer: " << sum << std::endl;
}

int main(int argc, const char** argv) {
    return run(argc, argv, base_name(__FILE__), process_file);
}
