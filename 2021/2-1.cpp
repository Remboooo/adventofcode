#include <iostream>
#include <fstream>
#include <string>
#include "util.h"

void process_file(std::ifstream& infile) {
    std::string direction;
    int amount;

    int h = 0, z = 0;

    while ((infile >> direction) && (infile >> amount)) {
        switch (direction.c_str()[0]) {
            case 'd':
                z += amount;
                break;
            case 'u':
                z -= amount;
                break;
            case 'f':
                h += amount;
                break;
            default:
                throw UserError("Unknown direction " + direction);
        }
    }
    std::cout << "H " << h << ", Z " << z << "; answer = " << (h*z) << std::endl;
}

int main(int argc, const char** argv) {
    return run(argc, argv, base_name(__FILE__), process_file);
}
