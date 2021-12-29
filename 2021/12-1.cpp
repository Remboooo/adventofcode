#include <iostream>
#include <fstream>
#include <string>
#include <utility>
#include "util.h"

struct CaveObj {
    const std::string name;
    const bool is_big;

    explicit CaveObj(const std::string &name) :
        name(name),
        is_big(all_match(name, [](char c){ return std::isupper(c); })) {
    }

    // Needed for usage as value type in std::set
    bool operator<(const CaveObj& other) const {
        return name < other.name;
    }
};

// Needed for debug output
std::ostream& operator<<(std::ostream& o, const CaveObj& c) {
    return o << c.name;
}

typedef std::shared_ptr<CaveObj> Cave;

int count_routes(
        const Cave& start,
        const Cave& dest,
        std::map<Cave, std::set<Cave>>& connections,
        const std::vector<Cave>& visited = {}
        ) {

    if (start == dest) {
        dbg(for (const auto& hop : visited) std::cout << hop->name << ",");
        dbg(std::cout << dest->name << std::endl);
        return 1;
    }
    std::vector<Cave> new_visited = appended({visited, {start}});
    int result = 0;
    for (const auto& next_hop : connections[start]) {
        if (!next_hop->is_big && contains(visited, next_hop)) continue;
        result += count_routes(next_hop, dest, connections, new_visited);
    }
    return result;
}

void process_file(std::ifstream& infile) {
    std::set<Cave, shared_ptr_obj_comparator_t> caves;
    std::map<Cave, std::set<Cave>> connections;
    for (std::string line; !std::getline(infile, line).eof();) {
        auto [a, b] = pair(string_split<Cave>(line, "-", [&caves](const std::string& name){
            return *caves.insert(std::make_shared<CaveObj>(name)).first;
        }));
        connections[a].insert(b);
        connections[b].insert(a);
    }

    auto start = *caves.find(std::make_shared<CaveObj>("start"));
    auto end = *caves.find(std::make_shared<CaveObj>("end"));

    int answer = count_routes(start, end, connections);

    std::cout << "Answer: " << answer << std::endl;
}

int main(int argc, const char** argv) {
    return run(argc, argv, base_name(__FILE__), process_file);
}
