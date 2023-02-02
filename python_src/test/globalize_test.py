from diopter.compiler import Language, SourceProgram
from static_globals.instrumenter import annotate_with_static


def test_globalize1() -> None:
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


def test_globalize2() -> None:
    program = annotate_with_static(
        SourceProgram(
            code="""
            int a;
            int b;
            static int c;
            int foo(int a) {
                return a + b;
            }

            int main(){
                return foo(2) + c;
            }
            """,
            language=Language.C,
        )
    )
    assert "".join(program.code.split()) == "".join(
        """
            static int a;
            static int b;
            static int c;
            static int foo(int a) {
                return a + b;
            }

            int main(){
                return foo(2) + c;
            }
            """.split()
    )
