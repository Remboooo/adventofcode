cmake_minimum_required(VERSION 3.21)
project(aoc2021)

set(CMAKE_CXX_STANDARD 23)

add_compile_options(-Wall -Wextra -Wpedantic)

if (MINGW)
    add_link_options(-static-libgcc -static-libstdc++ -Wl,-Bstatic,--whole-archive -lwinpthread -Wl,--no-whole-archive)
else()
    add_link_options(-static-libgcc -static-libstdc++)
endif()

set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -DDEBUG")

include_directories(BEFORE util)
include_directories(SYSTEM shared/blaze/)

add_library(util util/util.cpp util/util.h util/circular_buffer.h util/argparse.hpp util/ostream.h util/parsing.h util/run.h util/containers.h)
link_libraries(util)

add_executable(1-1 1-1.cpp 13-1.cpp)
add_executable(1-2 1-2.cpp)
add_executable(2-1 2-1.cpp)
add_executable(2-2 2-2.cpp)
add_executable(3-1 3-1.cpp)
add_executable(3-2 3-2.cpp)
add_executable(4-1 4-1.cpp)
add_executable(4-2 4-2.cpp)
add_executable(5-1 5-1.cpp)
add_executable(5-2 5-2.cpp)
add_executable(6-1 6-1.cpp)
add_executable(6-2 6-2.cpp)
add_executable(7-1 7-1.cpp)
add_executable(7-2 7-2.cpp)
add_executable(8-1 8-1.cpp)
add_executable(8-2 8-2.cpp)
add_executable(9-1 9-1.cpp)
add_executable(9-2 9-2.cpp)
add_executable(10-1 10-1.cpp)
add_executable(10-2 10-2.cpp)
add_executable(11-1 11-1.cpp)
add_executable(11-2 11-2.cpp)
add_executable(12-1 12-1.cpp)
add_executable(12-2 12-2.cpp)
add_executable(13-1 13-1.cpp)
add_executable(13-2 13-2.cpp)
