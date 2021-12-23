#include <iostream>
#include <fstream>
#include <string>
#include <utility>
#include "util.h"

long total_dist(const std::vector<int>& positions, long center) {
    return accumulate(positions, 0L, [center](long v, int p){ return v + std::abs(p - center); });
}

void process_file(std::ifstream& infile) {
    auto positions = string_split<int>(getline(infile), ",", stoi);

    dbg(std::cout << "Initial positions: " << positions << std::endl);

    long pos = long(positions.size()/2);
    long left_sum, center_sum, right_sum;

    do {
        left_sum = total_dist(positions, pos-1);
        center_sum = total_dist(positions, pos);
        right_sum = total_dist(positions, pos+1);
        dbg(std::cout << "Pos " << pos << ", sums " << left_sum << "/" << center_sum << "/" << right_sum << std::endl);
        if (left_sum > center_sum) ++pos;
        if (right_sum > center_sum) --pos;
    } while (!(left_sum > center_sum && right_sum > center_sum));

    std::cout << "Best position " << pos << ", answer: " << center_sum << std::endl;
}

int main(int argc, const char** argv) {
    return run(argc, argv, base_name(__FILE__), process_file);
}
