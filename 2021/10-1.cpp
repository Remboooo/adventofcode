#include <iostream>
#include <fstream>
#include <string>
#include <utility>
#include "util.h"

static std::map<char, long> illegal_scores {
        {')', 3},
        {']', 57},
        {'}', 1197},
        {'>', 25137}
};

static std::map<char, char> closers {
        {'(', ')'},
        {'[', ']'},
        {'{', '}'},
        {'<', '>'}
};

long get_line_score(const std::string& line) {
    std::vector<char> q;
    for (char c : line) {
        auto it = closers.find(c);
        if (it != closers.end()) {
            // this is an opening char
            char closer = it->second;
            q.push_back(closer);
        } else {
            // this is a closing char
            char expected = q.back();
            q.pop_back();
            if (c != expected) {
                dbg(std::cout << "Expected " << expected << " but got " << c << std::endl;);
                return illegal_scores.at(c);
            }
        }
    }
    return 0;
}

void process_file(std::ifstream& infile) {
    std::string line;
    long sum = 0;
    while (!std::getline(infile, line).eof()) {
        sum += get_line_score(line);
    }

    std::cout << "Answer: " << sum << std::endl;
}

int main(int argc, const char** argv) {
    return run(argc, argv, base_name(__FILE__), process_file);
}
