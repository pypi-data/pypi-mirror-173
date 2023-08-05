#pragma once

// On windows we need spec declarations for shared libraries:
#ifdef _WIN32
	#ifdef LIB_BUILD_SHARED
		// When building the DLL, we specify we want the classes and functions treated as export
		#define LIB_API __declspec(dllexport)
	#elif LIB_BUILD_STATIC
		// Compiling statically we don't want to specify anything as an import
		#define LIB_API 
	#else
		// When building the executables, we specify we want everything treated as import
		#define LIB_API __declspec(dllimport)
	#endif
#else
	// On other systems we can leave it empty
	#define LIB_API 
#endif

#include <string>

extern "C" std::string LIB_API areYouTheOneImLookingFor();