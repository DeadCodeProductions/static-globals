add_library(StaticGlobalslib
            GlobalStaticMaker.cpp
            VersionChecks.cpp)
target_include_directories(StaticGlobalslib PUBLIC ${CLANG_INCLUDE_DIRS} ${LLVM_INCLUDE_DIRS} ${CMAKE_CURRENT_SOURCE_DIR})

if(CLANG_LINK_CLANG_DYLIB)
    target_link_libraries(StaticGlobalslib PUBLIC LLVM)
    clang_target_link_libraries(StaticGlobalslib PUBLIC)
else()
    llvm_map_components_to_libnames(llvm_libs support core)
    target_link_libraries(StaticGlobalslib PUBLIC ${llvm_libs}
                                                   clangASTMatchers
                                                   clangTransformer
                                                   clangTooling)
endif(CLANG_LINK_CLANG_DYLIB)


add_subdirectory(tool)
