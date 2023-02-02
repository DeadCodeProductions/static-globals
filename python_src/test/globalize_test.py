from diopter.compiler import Language, SourceProgram
from static_globals.instrumenter import annotate_with_static


def test_globalize() -> None:
    program = annotate_with_static(
        SourceProgram(
            code="""
            int a;
            int b;
            static int c;
            """,
            language=Language.C,
        )
    )
    assert "".join(program.code.split()) == "staticinta;staticintb;staticintc;"
