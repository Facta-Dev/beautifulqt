cmake_minimum_required(VERSION 3.21)
project(beautifulqt_minimal LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 REQUIRED COMPONENTS Core Widgets Test)
qt_standard_project_setup()

add_library(viewmodel STATIC viewmodel.cpp viewmodel.h)
target_link_libraries(viewmodel PUBLIC Qt6::Core)
target_include_directories(viewmodel PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

qt_add_executable(app main.cpp)
target_link_libraries(app PRIVATE Qt6::Widgets viewmodel)

# The violation harness is compiled so clang-tidy has a compile command for
# it; it is deliberately not installed.
add_library(lint_check OBJECT
  ../../lints/check/clean.cpp
  ../../lints/check/violations.cpp
)
target_link_libraries(lint_check PRIVATE Qt6::Core)

enable_testing()
qt_add_executable(tests test_viewmodel.cpp)
target_link_libraries(tests PRIVATE Qt6::Test viewmodel)
add_test(NAME viewmodel COMMAND tests)
