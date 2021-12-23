#include <iostream>
#include <fstream>
#include <string>
#include <utility>
#include "util.h"

#include <blaze/Blaze.h>

typedef std::pair<int, int> coord;
typedef std::pair<coord, coord> line;

std::vector<line> read_lines(std::ifstream &infile) {
    std::vector<line> lines{};
    std::string file_line;

    while (true) {
        std::getline(infile, file_line);
        if (infile.eof()) return lines;

        lines.push_back(
            pair(string_split<coord>(file_line, " -> ", [](auto& v){
                return pair(string_split<int>(v, ",", stoi));
            }))
        );
    }
}

void process_file(std::ifstream& infile) {
    auto lines = read_lines(infile);

    dbg(std::cout << lines << std::endl);

    auto x_max = accumulate(lines, 0, [](auto x, auto& l) { return std::max({l.first.first, l.second.first, x}); });
    auto y_max = accumulate(lines, 0, [](auto y, auto& l) { return std::max({l.first.second, l.second.second, y}); });

    blaze::DynamicMatrix<int> field(x_max+1, y_max+1, 0);

    for (auto& l : lines) {
        int dx, dy;
        if (l.first.first == l.second.first) {
            dx = 0;
            dy = l.first.second < l.second.second ? +1 : -1;
        }
        else if (l.first.second == l.second.second) {
            dx = l.first.first < l.second.first ? +1 : -1;
            dy = 0;
        }
        else if (std::abs(l.first.first - l.second.first) == std::abs(l.first.second - l.second.second)) {
            dx = l.first.first < l.second.first ? +1 : -1;
            dy = l.first.second < l.second.second ? +1 : -1;
        }
        else {
            continue;
        }
        int x = l.first.first, y = l.first.second;
        ++field.at(x, y);
        while (x != l.second.first || y != l.second.second) {
            x += dx;
            y += dy;
            ++field.at(x, y);
        }
    }

    dbg(std::cout << field.transpose() << std::endl);

    std::cout << "Answer: " << blaze::sum(blaze::map(field, [](auto v){ return v >= 2; })) << std::endl;
}

int main(int argc, const char** argv) {
    return run(argc, argv, base_name(__FILE__), process_file);
}
