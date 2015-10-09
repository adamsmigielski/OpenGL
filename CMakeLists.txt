PROJECT(OpenGL)

ADD_LIBRARY(OpenGL STATIC
			Context.cpp
			Context.hpp
			gl.hpp
			GL_loader.cpp
			PCH.cpp
			PCH.hpp)