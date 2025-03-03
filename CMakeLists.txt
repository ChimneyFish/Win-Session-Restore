cmake_minimum_required(VERSION 3.14)
project(SnapshotApp)

set(CMAKE_CXX_STANDARD 14)

find_package(Qt5 COMPONENTS Widgets REQUIRED)
find_package(JsonCpp REQUIRED)

add_executable(SnapshotApp main.cpp SnapshotApp.cpp)

target_link_libraries(SnapshotApp Qt5::Widgets jsoncpp)
