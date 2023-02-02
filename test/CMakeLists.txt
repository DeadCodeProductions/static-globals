add_executable(static_globals_test
               test_driver.cpp
               test_tool.cpp
               static_global_test.cpp
               print_diff.cpp)

target_link_libraries(static_globals_test PRIVATE Catch2::Catch2 StaticGlobalslib)
target_include_directories(static_globals_test SYSTEM PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/extern)

catch_discover_tests(static_globals_test)
