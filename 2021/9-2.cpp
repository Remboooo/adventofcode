#include <iostream>
#include <fstream>
#include <string>
#include <utility>
#include "util.h"

typedef std::vector<std::vector<int>> heightmap;

heightmap read_heightmap(std::ifstream& infile) {
    std::vector<std::vector<int>> result;
    for (std::string line; !std::getline(infile, line).eof();) {
        result.push_back(transform<int>(line, [](char c) { return c - '0'; }));
    }

    return result;
}

size_t get_basin_size(unsigned start_x, unsigned start_y, const heightmap& map) {
    typedef std::pair<unsigned, unsigned> coord;
    std::set<coord> done {
        std::make_pair(start_x, start_y),
    };
    std::set<coord> queue {
        std::make_pair(start_x - 1, start_y),
        std::make_pair(start_x + 1, start_y),
        std::make_pair(start_x, start_y - 1),
        std::make_pair(start_x, start_y + 1),
    };
    size_t s = 1;
    while (!queue.empty()) {
        auto it = queue.begin();
        auto now = *it;
        queue.erase(it);
        done.insert(now);

        auto [x, y] = now;
        if (map[y][x] < 9) {
            ++s;
            auto left = std::make_pair(x-1, y);
            auto right = std::make_pair(x+1, y);
            auto up = std::make_pair(x, y-1);
            auto down = std::make_pair(x, y+1);
            if (!done.contains(left)) queue.insert(left);
            if (!done.contains(right)) queue.insert(right);
            if (!done.contains(up)) queue.insert(up);
            if (!done.contains(down)) queue.insert(down);
        }
    }
    return s;
}

void process_file(std::ifstream& infile) {
    auto h = read_heightmap(infile);
    dbg(std::cout << std::hex << h << std::dec << std::endl);

    pad2d(h, 1, 10);

    std::vector<size_t> basins;

    for (unsigned x = 1; x < h[0].size() - 1; ++x) {
        for (unsigned y = 1; y < h.size() - 1; ++y) {
            auto v = h[y][x];
            if (v < h[y-1][x] && v < h[y+1][x] && v < h[y][x-1] && v < h[y][x+1]) {
                auto s = get_basin_size(x, y, h);
                dbg(std::cout << "Basin at " << std::make_pair(x, y) << " = " << s << std::endl);
                basins.push_back(s);
            }
        }
    }

    rsort(basins);
    dbg(std::cout << "Basins: " << basins << std::endl);

    std::cout << "Answer: " << (basins.at(0) * basins.at(1) * basins.at(2)) << std::endl;
}

int main(int argc, const char** argv) {
    return run(argc, argv, base_name(__FILE__), process_file);
}
