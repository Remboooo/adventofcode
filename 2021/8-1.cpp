#include <iostream>
#include <fstream>
#include <string>
#include <utility>
#include "util.h"

void process_file(std::ifstream& infile) {
    unsigned count = 0;
    std::string line;
    while (true) {
        std::getline(infile, line);
        if (infile.eof()) break;
        auto out_segs = string_split(string_split(line, " \\| ").at(1), " ");
        count += count_if(out_segs, [](const std::string& v){ auto l = v.size(); return l == 2 || l == 4 || l == 3 || l == 7; });
    }
    std::cout << "Answer: " << count << std::endl;
}

int main(int argc, const char** argv) {
    return run(argc, argv, base_name(__FILE__), process_file);
}
