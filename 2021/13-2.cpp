#include <iostream>
#include <fstream>
#include <string>
#include <utility>
#include "util.h"

enum class FoldAxis : bool {
    x,
    y
};

struct Fold {
    FoldAxis fold_axis;
    int position;
};

void out_dots(int max_x, int max_y, const std::vector<std::vector<bool>> &dots);

std::ostream& operator<<(std::ostream& o, const Fold& fold) {
    return o << '{' << (fold.fold_axis == FoldAxis::y ? 'y' : 'x') << ',' << fold.position << '}';
}

std::ostream& operator<<(std::ostream& o, const std::vector<std::vector<bool>>& f) {
    for (const auto& row : f) {
        for (bool v : row) {
            o << (v ? '#' : '.');
        }
        o << std::endl;
    }
    return o;
}

void process_file(std::ifstream& infile) {
    std::vector<std::pair<int, int>> dot_positions;
    std::vector<Fold> folds;
    for (std::string line; std::getline(infile, line) && !line.empty();) {
        dot_positions.push_back(pair(string_split<int>(line, ",", stoi)));
    }
    for (std::string line; !std::getline(infile, line).eof();) {
        auto [op_str, coord_str] = pair(string_split(line, "="));
        FoldAxis axis = op_str.at(op_str.size() - 1) == 'y' ? FoldAxis::y : FoldAxis::x;
        folds.push_back({axis, stoi(coord_str)});
    }

    int max_x = accumulate(dot_positions, 0, [](int a, const std::pair<int, int>& b){ return std::max(a, b.first); });
    int max_y = accumulate(dot_positions, 0, [](int a, const std::pair<int, int>& b){ return std::max(a, b.second); });

    std::vector<std::vector<bool>> dots(max_y+1, std::vector<bool>(max_x+1));
    for (auto [x, y] : dot_positions) {
        dots[y][x] = true;
    }

    dbg(std::cout << dot_positions << std::endl);
    dbg(std::cout << folds << std::endl);
    dbg(out_dots(max_x, max_y, dots));

    for (const Fold& fold : folds) {
        dbg(std::cout << "Fold: " << fold << std::endl);
        if (fold.fold_axis == FoldAxis::x) {
            for (int y = 0; y <= max_y; ++y) {
                for (int x = fold.position + 1; x <= max_x; ++x) {
                    int refl_x = 2 * fold.position - x;
                    if (refl_x < 0) break;
                    dots[y][refl_x] = dots[y][refl_x] || dots[y][x];
                }
            }
            max_x = fold.position - 1;
        } else {

            // y = 8, refl_y = 14 + 7 - 1 - 8
            for (int y = fold.position+1, refl_y = fold.position-1; y <= max_y && refl_y >= 0; ++y, --refl_y) {
                for (int x = 0; x <= max_x; ++x) {
                    dots[refl_y][x] = dots[refl_y][x] || dots[y][x];
                }
            }
            max_y = fold.position - 1;
        }
        dbg(out_dots(max_x, max_y, dots));
    }

    out_dots(max_x, max_y, dots);
}

void out_dots(int max_x, int max_y, const std::vector<std::vector<bool>> &dots) {
    for (int y = 0; y <= max_y; ++y) {
        for (int x = 0; x <= max_x; ++x) {
            std::cout << (dots[y][x] ? '#' : '.');
        }
        std::cout << std::endl;
    }
    std::cout << std::endl;
}

int main(int argc, const char** argv) {
    return run(argc, argv, base_name(__FILE__), process_file);
}
