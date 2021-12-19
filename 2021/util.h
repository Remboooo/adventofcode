#pragma once

#include <fstream>
#include <string>
#include <utility>

#include "args.hxx"

class UserError : std::exception {
public:
    explicit UserError(std::string msg) : msg(std::move(msg)) {}

    [[nodiscard]] const char* what() const noexcept override {
        return this->msg.c_str();
    }
private:
    std::string msg;
};

int run(int argc, const char** argv, const char* name, auto arg_processor, auto file_processor) {
    args::ArgumentParser parser(name, "");
    args::HelpFlag help(parser, "help", "Display this help menu", {'h', "help"});
    arg_processor(parser);
    args::PositionalList<std::string> filenames(parser, "files", "The input files to process");
    try {
        parser.ParseCLI(argc, argv);
        for (auto& filename : args::get(filenames)) {
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
    } catch (const args::Completion& e) {
        std::cout << e.what();
        return 0;
    } catch (const args::Help&) {
        std::cout << parser;
        return 0;
    } catch (const args::ParseError& e) {
        std::cerr << e.what() << std::endl;
        std::cerr << parser;
        return 1;
    } catch (const UserError& e) {
        std::cerr << e.what() << std::endl;
        return 2;
    } catch (const std::exception& e) {
        std::cerr << e.what() << std::endl;
        return 255;
    }
}

static int run(int argc, const char** argv, const char* name, auto file_processor) {
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
