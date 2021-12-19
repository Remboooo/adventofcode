#include <iostream>
#include <fstream>
#include <limits>
#include <string>
#include "util.h"

void process_file(std::ifstream& infile) {
    unsigned int now, prev = std::numeric_limits<unsigned int>::max(), largers = 0;
    while (infile >> now) {
#if defined(DEBUG)
        std::cout << "now " << now << std::endl;
#endif
        if (now > prev) ++largers;
        prev = now;
    }
    std::cout << "Answer: " << largers << std::endl;
}

int main(int argc, const char** argv) {
    return run(argc, argv, file_name(__FILE__), process_file);
}
