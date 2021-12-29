#include <iostream>
#include <fstream>
#include <string>
#include <utility>
#include "util.h"

struct CaveObj {
    const std::string name;
    const bool is_big;
    const bool is_special;

    explicit CaveObj(const std::string &name) :
        name(name),
        is_big(all_match(name, [](char c){ return std::isupper(c); })),
        is_special(name == "start" || name == "end"
        ){}

    // Needed for usage as value type in std::set
    bool operator<(const CaveObj &other) const {
        return name < other.name;
    }
};

// Needed for debug output
std::ostream& operator<<(std::ostream &o, const CaveObj &c) {
    return o << c.name;
}

typedef std::shared_ptr<CaveObj> Cave;

int count_routes(
        const Cave &start, // where we are currently
        const Cave &dest, // where we want to be
        const std::map<Cave, std::set<Cave>> &connections, // the set of other caves connected to each cave
        const std::set<Cave> &visited_set, // the set of all small caves we visited so far
        const bool twice_small_allowed, // whether we can still visit a cave twice
        const std::shared_ptr<std::map<std::tuple<std::set<Cave>, Cave, bool>, int>> &memo, // result cache
        const std::vector<Cave> &visited, // only for debug output
        const int indent = 0 // only for debug output
    ) {

    if (start == dest) {
        dbg(std::cout << std::string(indent, ' ') << visited << " = 1" << std::endl;);
        return 1;
    }

    const auto memo_key = std::make_tuple(visited_set, start, twice_small_allowed);
    auto memo_it = memo->find(memo_key);
    if (memo_it != memo->end()) {
        dbg(std::cout << std::string(indent, ' ') << visited << " ... = " << memo_it->second << " " << memo_key << std::endl);
        return memo_it->second;
    }

    int result = 0;
    for (auto &next_hop : connections.at(start)) {
        bool new_twice_small_allowed = twice_small_allowed;

        if (visited_set.contains(next_hop)) {
            if (twice_small_allowed && !next_hop->is_special) {
                new_twice_small_allowed = false;
            } else {
                continue;
            }
        }

        std::set<Cave> new_visited_set = visited_set;
        if (!next_hop->is_big) {
            new_visited_set.insert(next_hop);
        }

        result += count_routes(
                next_hop, dest, connections, new_visited_set, new_twice_small_allowed, memo,
                is_dbg() ? appended({visited, {next_hop}}) : visited, indent + 1
        );
    }

    dbg(std::cout << std::string(indent, ' ') << "Memoizing ");
    dbg(std::cout << visited << " ... = " << result << " " << memo_key << std::endl);
    (*memo)[memo_key] = result;

    return result;
}

int count_routes(
        const Cave &start,
        const Cave &dest,
        const std::map<Cave, std::set<Cave>> &connections
) {
    auto memo_pad = std::make_shared<std::map<std::tuple<std::set<Cave>, Cave, bool>, int>>();
    return count_routes(start, dest, connections, {start}, true, memo_pad, {start});
}

void process_file(std::ifstream &infile) {
    // This set compares the objects themselves in stead of the "shared_ptr"s to ensure only unique CaveObj objects exist
    std::set<Cave, shared_ptr_obj_comparator_t> caves;
    std::map<Cave, std::set<Cave>> connections;
    for (std::string line; !std::getline(infile, line).eof();) {
        auto [a, b] = pair(string_split<Cave>(line, "-", [&caves](const std::string& name){
            return *caves.insert(std::make_shared<CaveObj>(name)).first;
        }));
        connections[a].insert(b);
        connections[b].insert(a);
    }
    std::cout << "Answer: "
        << count_routes(*caves.find(std::make_shared<CaveObj>("start")),
                        *caves.find(std::make_shared<CaveObj>("end")),
                        connections)
        << std::endl;
}

int main(int argc, const char** argv) {
    return run(argc, argv, base_name(__FILE__), process_file);
}
