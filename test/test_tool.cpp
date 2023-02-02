#include <string>

#include <catch2/catch.hpp>
#include <clang/Tooling/Refactoring.h>
#include <clang/Tooling/Tooling.h>

#include <GlobalStaticMaker.h>
#include <RewriterTestContext.h>

#include "print_diff.h"
#include "test_tool.h"

using namespace clang;

std::string formatCode(llvm::StringRef Code) {
    tooling::Replacements Replaces = format::reformat(
        format::getLLVMStyle(), Code, {tooling::Range(0, Code.size())});
    auto ChangedCode = tooling::applyAllReplacements(Code, Replaces);
    REQUIRE(static_cast<bool>(ChangedCode));
    return *ChangedCode;
}

void compare_code(const std::string &code1, const std::string &code2) {
    auto diff = code1 != code2;
    if (diff)
        print_diff(code1, code2);
    REQUIRE(!diff);
}

std::string runMakeGlobalsStaticOnCode(llvm::StringRef Code) {
    clang::RewriterTestContext Context;
    clang::FileID ID = Context.createInMemoryFile("input.cc", Code);

    std::map<std::string, tooling::Replacements> FileToReplacements;
    dead::GlobalStaticMaker InstrumenterTool{FileToReplacements};
    ast_matchers::MatchFinder Finder;
    InstrumenterTool.registerMatchers(Finder);
    std::unique_ptr<tooling::FrontendActionFactory> Factory =
        tooling::newFrontendActionFactory(&Finder);
    REQUIRE(tooling::runToolOnCode(Factory->create(), Code, "input.cc"));
    formatAndApplyAllReplacements(FileToReplacements, Context.Rewrite);
    return formatCode(formatCode(Context.getRewrittenText(ID)));
}
