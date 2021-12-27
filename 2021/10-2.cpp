#include <iostream>
#include <fstream>
#include <ranges>
#include <string>
#include <utility>
#include "util.h"

static std::map<char, long long> completion_scores {
        {')', 1},
        {']', 2},
        {'}', 3},
        {'>', 4}
};

static std::map<char, char> closers {
        {'(', ')'},
        {'[', ']'},
        {'{', '}'},
        {'<', '>'}
};

long long get_line_score(const std::string& line) {
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
                dbg(std::cout << "Expected " << expected << " but got " << c << std::endl);
                return 0;
            }
        }
    }
    long long sum = 0;
    for (char c : std::ranges::reverse_view(q)) {
        long score = completion_scores.at(c);
        sum = 5LL * sum + score;
        dbg(std::cout << " + " << c << " (" << score << + ")");
    }
    dbg(std::cout << " = " << sum << std::endl);
    return sum;
}

void process_file(std::ifstream& infile) {
    std::string line;
    std::vector<long long> scores;
    while (!std::getline(infile, line).eof()) {
        auto score = get_line_score(line);
        if (score != 0) {
            scores.push_back(score);
        }
    }

    sort(scores);

    std::cout << "Answer: " << scores.at(scores.size()/2) << std::endl;
}

int main(int argc, const char** argv) {
    return run(argc, argv, base_name(__FILE__), process_file);
}
