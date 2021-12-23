#ifndef AOC2021_PARSING_H
#define AOC2021_PARSING_H

#include <fstream>
#include <string>
#include <regex>
#include <utility>


constexpr auto stoi = [](const std::string& s){return std::stoi(s);};
constexpr auto stol = [](const std::string& s){return std::stol(s);};
constexpr auto stoll = [](const std::string& s){return std::stoll(s);};
constexpr auto stou = [](const std::string& s){return (unsigned) std::stoul(s);};
constexpr auto stoul = [](const std::string& s){return std::stoul(s);};
constexpr auto stoull = [](const std::string& s){return std::stoull(s);};

template <typename T>
std::vector<T> string_split(const std::string& s, const std::string& sep, auto converter=[](const std::string& v){return v;}, bool skip_empty=true) {
    std::regex splitter(sep);
    std::vector<T> t{};

    auto begin = std::sregex_token_iterator(std::begin(s), std::end(s), splitter, -1);
    auto end = std::sregex_token_iterator();

    for (auto it = begin; it != end; ++it) {
        const auto part = it->str();
        if (skip_empty && part.empty()) continue;
        t.push_back(converter(part));
    }

    return t;
}

template <typename T>
std::pair<T, T> pair(const std::vector<T>& vec) {
    return std::make_pair(vec.at(0), vec.at(1));
}

std::string getline(std::istream& i) {
    std::string result;
    std::getline(i, result);
    return result;
}


#endif //AOC2021_PARSING_H
