#ifndef AOC2021_RUN_H
#define AOC2021_RUN_H

#include <fstream>
#include <string>
#include <regex>
#include <utility>

#include "util.h"
#include "argparse.hpp"

typedef argparse::ArgumentParser args;

class UserError : std::exception {
public:
    explicit UserError(std::string msg) : msg(std::move(msg)) {}

    [[nodiscard]] const char* what() const noexcept override {
        return this->msg.c_str();
    }
private:
    std::string msg;
};

template<class F>
int run(int argc, const char** argv, const std::string& name, auto arg_processor, F file_processor) {
    argparse::ArgumentParser parser(name);

    arg_processor(parser);

    parser.add_argument("files").remaining();

    std::cout << std::boolalpha; // Set booleans to be output as text

    try {
        parser.parse_args(argc, argv);
        for (auto& filename : parser.get<std::vector<std::string>>("files")) {
            std::cout << "Processing " << filename << std::endl;
            std::ifstream f;
            f.exceptions(std::ifstream::badbit);
            try {
                f.open(filename);
                if (!f.is_open()) {
                    throw UserError("Could not open " + filename);
                }
                if constexpr (std::is_invocable_v<F, std::ifstream&>) {
                    file_processor(f);
                }
                else if constexpr (std::is_invocable_v<F, std::ifstream&, argparse::ArgumentParser&>) {
                    file_processor(f, parser);
                }
                else static_fail("file_processor must be callable with (ifstream&) or (ifstream&, args&)");
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

#endif //AOC2021_RUN_H
