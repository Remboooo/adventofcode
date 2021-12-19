#include <iostream>
#include <fstream>
#include <limits>
#include <string>
#include <numeric>
#include "circular_buffer.h"
#include "util.h"

void process_file(std::ifstream& infile) {
    unsigned int now, prev = std::numeric_limits<unsigned int>::max(), largers = 0;
    CircularBuffer<unsigned int> cb(3);
    while (infile >> now) {
        cb.push_back(now);
        unsigned int sum = std::accumulate(cb.begin(), cb.end(), (unsigned) 0);
#if defined(DEBUG)
        std::cout << "now " << now << "; sum = " << sum << std::endl;
#endif
        if (cb.size() >= 3) {
            if (sum > prev) ++largers;
            prev = sum;
        }
    }
    std::cout << "Answer: " << largers << std::endl;
}

int main(int argc, const char** argv) {
    return run(argc, argv, file_name(__FILE__), process_file);
}
