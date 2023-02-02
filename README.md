`make-globals-static` is used in
[DEAD](https://github.com/DeadCodeProductions/dead). It makes global variables
and functions (except `main`) static.

#### To build just the clang tool

Prerequisites: `cmake`, `make`, `clang/llvm` 13/14.

```
mkdir build
cd build
cmake .. 
cmake --build . [--parallel]
cmake --install . --prefix=/where/to/install/
```

#### Usage
```
cat test.c
int b;
int foo(int a) {
    return a + b;
}

int main(){
    return foo(2);
}


make-globals-static test.c --


cat test.c 
static int b;
static int foo(int a) {
    return a + b;
}

int main(){
    return foo(2);
}
```

#### Python wrapper

`pip install static-globals`


To use the instrumenter in python import `from static.instrumenter import annotate_with_static`: `def annotate_with_static( program: ProgramType) -> ProgramType`

#### Building the python wrapper

##### Local build

```
./build_python_wheel_local.sh #this will build the current branch
pip install .
```

#### Docker based build

```
docker run --rm -e REVISION=REV -v `pwd`:/io theodort/manylinux-with-llvm:latest /io/build_python_wheel_docker.sh
```

This will build multiple wheels for `REV` with multiple python versions.
The output is stored in the `wheelhouse` directory.
The docker image is based on https://github.com/thetheodor/manylinux-with-llvm.
