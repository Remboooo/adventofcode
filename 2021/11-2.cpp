#include <iostream>
#include <fstream>
#include <string>
#include <utility>
#include "util.h"

std::vector<std::vector<int>> read_map(std::ifstream& infile) {
    std::vector<std::vector<int>> result;
    for (std::string line; !std::getline(infile, line).eof();) {
        result.push_back(transform<int>(line, [](char c) { return c - '0'; }));
    }
    return result;
}

void process_file(std::ifstream& infile) {
    auto e = read_map(infile);

    typedef std::pair<int, int> coord;
    std::vector<coord> energy_increment_q;

    const int h = int(e.size());
    const int w = int(e.at(0).size());

    dbg(std::cout << "Before any steps:" << std::endl << e << std::endl);

    int step;
    for (step = 0; true; ++step) {
        for (int y = 0; y < h; ++y) {
            for (int x = 0; x < w; ++x) {
                energy_increment_q.emplace_back(x, y);
            }
        }
        int step_flashes = 0;
        while (!energy_increment_q.empty()) {
            auto [x, y] = energy_increment_q.back();
            energy_increment_q.pop_back();

            if (++e.at(y).at(x) == 10) {
                ++step_flashes;
                for (int nx = x-1; nx <= x+1; ++nx) {
                    for (int ny = y-1; ny <= y+1; ++ny) {
                        if ((nx != x || ny != y) && nx >= 0 && nx < w && ny >= 0 && ny < h) {
                            energy_increment_q.emplace_back(nx, ny);
                        }
                    }
                }
            }
        }
        if (step_flashes == w*h) break;
        for (int y = 0; y < h; ++y) {
            for (int x = 0; x < w; ++x) {
                if (e[y][x] > 9) {
                    e[y][x] = 0;
                }
            }
        }
        dbg(std::cout << "After step " << step << ":" << std::endl << e << std::endl);
    }

    std::cout << "Answer: " << (step+1) << std::endl;
}

int main(int argc, const char** argv) {
    return run(argc, argv, base_name(__FILE__), process_file);
}
