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

add_library(util util.cpp util.h args.hxx circular_buffer.h)
link_libraries(util)

add_executable(1-1 1-1.cpp)
add_executable(1-2 1-2.cpp)
add_executable(2-1 2-1.cpp)
add_executable(2-2 2-2.cpp)
add_executable(3-1 3-1.cpp)
add_executable(3-2 3-2.cpp)
