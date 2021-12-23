#include <iostream>
#include <fstream>
#include <string>
#include <utility>
#include "util.h"

void process_file(std::ifstream& infile, int days) {
    auto fish = string_split<int>(getline(infile), ",", stoi);

    dbg(std::cout << "Initial state: " << fish << std::endl);

    for (int day = 0; day < days; ++day) {
        auto new_fish = count_if(fish, [](int v){ return v == 0; });
        transform_inplace(fish, [](int v){ return v > 0 ? v-1 : 6; });
        for (unsigned i = 0; i < new_fish; ++i) fish.push_back(8);
        dbg(std::cout << "After " << (day+1) << " days: " << fish << std::endl);
    }

    std::cout << "Answer: " << fish.size() << std::endl;
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
