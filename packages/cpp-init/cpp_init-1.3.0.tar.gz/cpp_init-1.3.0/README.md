## cpp-init

A simple python project used for initialising c/c++ projects.

Installation:
```
pip install cpp-init
```

Usage:
```
python -m cpp_init <options>
```

`Options` are just 3 letters telling c-init what you want the project to be:
1. First letter `<>XX`:
	- `c` - specifies it's a c project
	- `x` - specifies it's a c++ project
2. Second letter `X<>X`:
	- `a` - specifies it's an executable application
	- `l` - specifies it's a library
3. Third letter `XX<>`:
	- `m` - specifies it's a make project
	- `c` - specifies it's a cmake project

Finally, it should (somewhat) look like this:
```
cpp_init xam  # will create a C++ application project compiled with make 
cpp_init clc  # will create a C library project compiled with CMake
...
```
