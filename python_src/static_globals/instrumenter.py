from __future__ import annotations

from dataclasses import replace
from functools import cache
from pathlib import Path

from diopter.compiler import ClangTool, ClangToolMode, CompilerExe, ProgramType


@cache
def get_instrumenter(
    instrumenter: ClangTool | None = None, clang: CompilerExe | None = None
) -> ClangTool:
    if not instrumenter:
        if not clang:
            # TODO: move this to diopter
            try:
                clang = CompilerExe.get_system_clang()
            except:  # noqa: E722
                pass
            if not clang:
                for clang_path in ("clang-17", "clang-16", "clang-15", "clang-14"):
                    try:
                        clang = CompilerExe.from_path(Path(clang_path))
                        break
                    except:  # noqa: E722
                        pass
            assert clang, "Could not find clang"

        instrumenter = ClangTool.init_with_paths_from_clang(
            Path(__file__).parent / "make-globals-static", clang
        )
    return instrumenter


def annotate_with_static(
    program: ProgramType,
    instrumenter: ClangTool | None = None,
    clang: CompilerExe | None = None,
) -> ProgramType:
    """Turn all globals in the given file into static globals.

    Args:
        file (Path): Path to code file to be instrumented.
        flags (list[str]): list of user provided clang flags
        instrumenter (Path): Path to the instrumenter executable., if not
                             provided will use what's specified in
        clang (Path): Path to the clang executable.
    Returns:
        None:
    """

    instrumenter_resolved = get_instrumenter(instrumenter, clang)

    result = instrumenter_resolved.run_on_program(
        program, [], ClangToolMode.READ_MODIFIED_FILE
    )
    assert result.modified_source_code

    return replace(program, code=result.modified_source_code)
