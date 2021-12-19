#pragma once

#include <fstream>
#include <string>
#include <utility>

#include "argparse.hpp"

class UserError : std::exception {
public:
    explicit UserError(std::string msg) : msg(std::move(msg)) {}

    [[nodiscard]] const char* what() const noexcept override {
        return this->msg.c_str();
    }
private:
    std::string msg;
};

int run(int argc, const char** argv, const std::string& name, auto arg_processor, auto file_processor) {
    argparse::ArgumentParser parser(name);

    parser.add_argument("files").remaining();

    arg_processor(parser);

    try {
        parser.parse_args(argc, argv);
        for (auto& filename : parser.get<std::vector<std::string>>("files")) {
            std::cout << "Processing " << filename << std::endl;
            std::ifstream f;
            f.exceptions(std::ifstream::badbit);
            try {
                f.open(filename);
                file_processor(f);
            } catch (std::ios_base::failure& e) {
                std::cerr << "Could not read " << filename << std::endl;
                return 3;
            }
        }
        return 0;
    } catch (const std::runtime_error& err) {
        std::cerr << err.what() << std::endl;
        std::cerr << parser;
        std::exit(1);
    } catch (const UserError& e) {
        std::cerr << e.what() << std::endl;
        std::exit(2);
    } catch (const std::exception& e) {
        std::cerr << e.what() << std::endl;
        std::exit(255);
    }
}

static int run(int argc, const char** argv, const std::string& name, auto file_processor) {
    return run(argc, argv, name, [](auto){}, file_processor);
}

template <class C>
std::ostream& ostream_container(std::ostream& o, const C& arr)
{
    o << "[";
    for (auto iter = arr.cbegin(); iter != arr.cend(); iter++) {
        if (iter != arr.cbegin()) o << ",";
        o << *iter;
    }
    o << "]";
    return o;
}

// Support for outputting arrays
template <class T, std::size_t N>
std::ostream& operator<<(std::ostream& o, const std::array<T, N>& arr) {
    return ostream_container(o, arr);
}

// Support for outputting vectors
template <class T>
std::ostream& operator<<(std::ostream& o, const std::vector<T>& vec) {
    return ostream_container(o, vec);
}

constexpr const char* file_name(const char* path) {
    const char* file = path;
    while (*path) {
        if (*path++ == '/') {
            file = path;
        }
    }
    return file;
}

constexpr const char* last_dot_of(const char* p) {
    const char* last_dot = nullptr;
    for ( ; *p ; ++p) {
        if (*p == '.')
            last_dot = p;
    }
    return last_dot ? last_dot : p;
}

std::string base_name(const char* path) {
    const char *filename = file_name(path);
    return {filename, last_dot_of(filename)};
}

// convenient shorthand for removing based on predicate
void remove_if(auto& container, auto predicate) {
    container.erase(
            std::remove_if(
                    container.begin(), container.end(), predicate
            ),
            container.end()
    );
}

void keep_if(auto& container, auto predicate) {
    remove_if(container, [predicate](auto v){return !predicate(v);});
}

unsigned long long count_if(auto& container, auto predicate) {
    return std::count_if(container.begin(), container.end(), predicate);
}
