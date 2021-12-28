#include <iostream>
#include <fstream>
#include <string>
#include <utility>
#include "util.h"

struct Cave {
    const std::string name;
    const bool is_big;

    explicit Cave(const std::string &name) :
        name(name),
        is_big(all_match(name, [](char c){ return std::isupper(c); }))
        {}

    bool operator<(const Cave& other) const {
        return name < other.name;
    }

    bool operator==(const Cave& other) const {
        return name == other.name;
    }
};

std::ostream& operator<<(std::ostream& o, const Cave& c) {
    return o << c.name;
}

typedef std::set<Cave> cave_set_t;
typedef std::map<Cave, cave_set_t> connection_map_t;
typedef std::vector<const Cave*> route_t;

int count_routes(
        const Cave& start,
        const Cave& dest,
        connection_map_t& connections,
        const route_t& visited = {}
        ) {

    if (start == dest) {
        dbg(for (const auto& hop : visited) std::cout << hop->name << ",");
        dbg(std::cout << dest.name << std::endl);
        return 1;
    }
    route_t new_visited = appended({visited, {&start}});
    int result = 0;
    for (const auto& next_hop : connections[start]) {
        if (!next_hop.is_big && any_match(visited, [&next_hop](const Cave* c){ return *c == next_hop; })) continue;
        result += count_routes(next_hop, dest, connections, new_visited);
    }
    return result;
}

void process_file(std::ifstream& infile) {
    cave_set_t caves;
    connection_map_t connections;
    for (std::string line; !std::getline(infile, line).eof();) {
        auto [a, b] = pair(string_split<Cave>(line, "-", [&caves](const std::string& name){
            return *caves.insert(Cave(name)).first;
        }));
        connections[a].insert(b);
        connections[b].insert(a);
    }

    auto start = *caves.find(Cave("start"));
    auto end = *caves.find(Cave("end"));

    int answer = count_routes(start, end, connections);

    std::cout << "Answer: " << answer << std::endl;
}

int main(int argc, const char** argv) {
    return run(argc, argv, base_name(__FILE__), process_file);
}
