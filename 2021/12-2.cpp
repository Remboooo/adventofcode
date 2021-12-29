#include <iostream>
#include <fstream>
#include <string>
#include <utility>
#include "util.h"

struct Cave {
    const std::string name;
    const bool is_big;
    const bool is_special;

    explicit Cave(const std::string &name) :
        name(name),
        is_big(all_match(name, [](char c){ return std::isupper(c); })),
        is_special(name == "start" || name == "end"
        ){}

    // Needed for usage as value type in std::set
    bool operator<(const Cave& other) const {
        return name < other.name;
    }
};

// Needed for debug output
std::ostream& operator<<(std::ostream& o, const Cave& c) {
    return o << c.name;
}

// This comparator compares the objects pointed to by std::shared_ptr objects, in stead of the pointers themselves
static auto shared_ptr_obj_comparator = [](const auto& a, const auto& b) { return *a < *b; };
typedef decltype(shared_ptr_obj_comparator) shared_ptr_obj_comparator_t;
// This set ensures unique Cave objects
typedef std::set<std::shared_ptr<Cave>, shared_ptr_obj_comparator_t> cave_set_t;
// This map contains connections between caves, but only using (fast) pointer comparisons between std::shared_ptr<Cave>
// objects. This works because the cave_set_t above ensures we only have 1 instance of every distinct Cave.
typedef std::map<std::shared_ptr<Cave>, std::set<std::shared_ptr<Cave>>> connection_map_t;
typedef std::vector<std::shared_ptr<Cave>> route_t;

int count_routes(
        const std::shared_ptr<Cave>& start,
        const std::shared_ptr<Cave>& dest,
        connection_map_t& connections,
        const route_t& visited = {},
        const bool has_twice_visited_cave = false
        ) {

    if (start == dest) {
        dbg(for (const auto& hop : visited) std::cout << hop->name << ",");
        dbg(std::cout << dest->name << std::endl);
        return 1;
    }
    route_t new_visited = appended({visited, {start}});
    int result = 0;
    for (const auto& next_hop : connections[start]) {
        bool new_has_twice_visited_cave = has_twice_visited_cave;
        if (!next_hop->is_big) {
            auto count = count_if(visited, [&next_hop](auto& v){ return v == next_hop; });
            if (!next_hop->is_special && count == 1 && !has_twice_visited_cave) {
                new_has_twice_visited_cave = true;
            } else if (count != 0) {
                continue;
            }
        }
        result += count_routes(next_hop, dest, connections, new_visited, new_has_twice_visited_cave);
    }
    return result;
}

void process_file(std::ifstream& infile) {
    cave_set_t caves;
    connection_map_t connections;
    for (std::string line; !std::getline(infile, line).eof();) {
        auto [a, b] = pair(string_split<std::shared_ptr<Cave>>(line, "-", [&caves](const std::string& name){
            return *caves.insert(std::make_shared<Cave>(name)).first;
        }));
        connections[a].insert(b);
        connections[b].insert(a);
    }

    auto start = *caves.find(std::make_shared<Cave>("start"));
    auto end = *caves.find(std::make_shared<Cave>("end"));

    int answer = count_routes(start, end, connections);

    std::cout << "Answer: " << answer << std::endl;
}

int main(int argc, const char** argv) {
    return run(argc, argv, base_name(__FILE__), process_file);
}
