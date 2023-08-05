# minimum version of cmake this will work on
cmake_minimum_required(VERSION 3.0.0)

# project's name and version
set(project_name {name})
project(${project_name} VERSION 1.0.0)

# add ./include/ as an include directory
include_directories(include)

# recursively search the include and src directories
file(GLOB_RECURSE srcs
	"include/*.hpp"
	"include/*.h"
	"src/*.cpp"
	"src/*.c"
)
{LIB_SNIPPET_START}
# depending on the library type, we set a correct macro
# create a library out of the sources
if(LIBTYPE STREQUAL "STATIC")
	add_library(${project_name} STATIC ${srcs})
	target_compile_definitions(${project_name} PRIVATE LIB_BUILD_STATIC)

else()
	add_library(${project_name} SHARED ${srcs})
	target_compile_definitions(${project_name} PRIVATE LIB_BUILD_SHARED)

endif()
{LIB_SNIPPET_END}{APP_SNIPPET_START}
# create an executable app out of the sources
add_executable(${project_name} ${srcs})
{APP_SNIPPET_END}