# OpenGL
Multi context OpenGL wrapper for C++

Build system
CMake - adds static library OpenGL
Depends on DEBUG symbol
Global configuration should be done before adding

Requirements
Depends on Platform.hpp
Depends on DEBUGLOG if DEBUG is set

Usage
Application should implement interface OpenGL::Context in a platform specific manner.
Entry points are defined in gl.hpp. They are aggregated in structure OpenGL::Functions.
OpenGL::LoadGL will load all entry points. When DEBUG is set, than missing entries will be logged.
	Entry points are loaded for the specified context. Concurrency is not allowed.


To generate files:
1 Get gl.xml: https://www.opengl.org/registry
2 parse.py gl.xml gl.json
3 command_list.py gl.json white_list.json 4.5
4 generate.py gl.json white_list.json gl.hpp Gl_loader.cpp
