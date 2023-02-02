add_executable(make-globals-static MakeGlobalsStatic.cpp)
target_link_libraries(make-globals-static PUBLIC StaticGlobalslib)

install(TARGETS make-globals-static DESTINATION bin)
