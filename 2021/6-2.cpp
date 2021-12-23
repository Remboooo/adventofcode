#include <iostream>
#include <fstream>
#include <string>
#include <utility>
#include "util.h"

void process_file(std::ifstream& infile, int days) {
    auto fish = string_split<int>(getline(infile), ",", stoi);

    dbg(std::cout << "Initial state: " << fish << std::endl);

    std::vector<unsigned long long> counts(9, 0);
    for (int v : fish) {
        ++counts.at(v);
    }

    dbg(std::cout << "Initial counts: " << counts << std::endl);

    for (int day = 0; day < days; ++day) {
        auto new_fish = counts.at(0);
        for (int i = 0; i < 8; ++i) {
            counts[i] = counts[i+1];
        }
        counts[6] += new_fish;
        counts[8] = new_fish;

        dbg(std::cout << "After " << (day+1) << " days: " << counts << std::endl);
    }

    std::cout << "Answer: " << accumulate<unsigned long long>(counts) << std::endl;
}

int main(int argc, const char** argv) {
    return run(
        argc, argv, base_name(__FILE__),
        [](argparse::ArgumentParser& parser){
            parser.add_argument("days").scan<'i', int>();
        },
        [](auto& in, args& parser){
            process_file(in, parser.get<int>("days"));
        }
    );
}
