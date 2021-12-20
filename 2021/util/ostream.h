#ifndef AOC2021_OSTREAM_H
#define AOC2021_OSTREAM_H

#include <fstream>
#include <string>
#include <regex>
#include <utility>


void ostream_container(std::ostream& o, const auto& arr, const std::string& sep=",") {
    for (auto iter = std::cbegin(arr); iter != std::cend(arr); iter++) {
        if (iter != std::cbegin(arr)) o << sep;
        o << *iter;
    }
}

// Support for outputting arrays
template <class T, std::size_t N>
std::ostream& operator<<(std::ostream& o, const std::array<T, N>& arr) {
    o << "["; ostream_container(o, arr, ", "); o << "]"; return o;
}

// Support for outputting vectors
template <class T>
std::ostream& operator<<(std::ostream& o, const std::vector<T>& vec) {
    o << "["; ostream_container(o, vec, ", "); o << "]"; return o;
}

// Support for outputting nested vectors (separate with newlines)
template <class T>
std::ostream& operator<<(std::ostream& o, const std::vector<std::vector<T>>& vec) {
    o << "[\n"; ostream_container(o, vec, "\n"); o << "\n]"; return o;
}

// Support for outputting pairs
template <class T1, class T2>
std::ostream& operator<<(std::ostream& o, const std::pair<T1, T2>& pair) {
    return o << "(" << pair.first << "," << pair.second << ")";
}


#endif //AOC2021_OSTREAM_H
