#ifndef AOC2021_OSTREAM_H
#define AOC2021_OSTREAM_H

#include <fstream>
#include <string>
#include <regex>
#include <utility>
#include <set>


void ostream_container(std::ostream& o, const auto& arr, const std::string& sep=",") {
    for (auto iter = std::cbegin(arr); iter != std::cend(arr); iter++) {
        if (iter != std::cbegin(arr)) o << sep;
        o << *iter;
    }
}

// Support for outputting arrays
template <class T, std::size_t N>
std::ostream& operator<<(std::ostream& o, const std::array<T, N>& arr) {
    o << "["; ostream_container(o, arr, ","); o << "]"; return o;
}

// Support for outputting vectors
template <class T, class A>
std::ostream& operator<<(std::ostream& o, const std::vector<T, A>& vec) {
    o << "["; ostream_container(o, vec, ","); o << "]"; return o;
}

// Support for outputting sets
template <class T, class C, class A>
std::ostream& operator<<(std::ostream& o, const std::set<T, C, A>& vec) {
    o << "{"; ostream_container(o, vec, ","); o << "}"; return o;
}

// Support for outputting nested vectors (separate with newlines)
template <class T, class A1, class A2>
std::ostream& operator<<(std::ostream& o, const std::vector<std::vector<T, A2>, A1>& vec) {
    o << "[\n"; ostream_container(o, vec, "\n"); o << "\n]"; return o;
}

// Support for outputting pairs
template <class T1, class T2>
std::ostream& operator<<(std::ostream& o, const std::pair<T1, T2>& pair) {
    return o << "(" << pair.first << "," << pair.second << ")";
}

template<std::size_t I = 0, typename... T>
typename std::enable_if<I == sizeof...(T), std::ostream&>::type
static _out_tup(std::ostream& o, const std::tuple<T...>&) {
    return o;
}

template<std::size_t I = 0, typename... T>
typename std::enable_if<I < sizeof...(T), std::ostream&>::type
static _out_tup(std::ostream& o, const std::tuple<T...>& tup) {
    if constexpr (I != 0) o << ",";
    o << std::get<I>(tup);
    return _out_tup<I+1>(o, tup);
}

// Support for outputting tuples
template <class... T>
std::ostream& operator<<(std::ostream& o, const std::tuple<T...>& tup) {
    o << "("; _out_tup(o, tup); return o << ")";
}

// Support for outputting shared_ptr
template <class T>
std::ostream& operator<<(std::ostream& o, const std::shared_ptr<T> c) {
    return o << *c;
}

// Support for outputting unordered maps
template <class K, class V, class H, class P, class A>
std::ostream& operator<<(std::ostream& o, const std::unordered_map<K, V, H, P, A>& map) {
    o << "{";
    for (auto iter = std::cbegin(map); iter != std::cend(map); iter++) {
        if (iter != std::cbegin(map)) o << ", ";
        o << iter->first << ": " << iter->second;
    }
    return o << "}";
}

// Support for outputting maps
template <class K, class V, class C, class A>
std::ostream& operator<<(std::ostream& o, const std::map<K, V, C, A>& map) {
    o << "{";
    for (auto iter = std::cbegin(map); iter != std::cend(map); iter++) {
        if (iter != std::cbegin(map)) o << ", ";
        o << iter->first << ": " << iter->second;
    }
    return o << "}";
}


#endif //AOC2021_OSTREAM_H
