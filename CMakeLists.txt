PROJECT(OpenGL)

SET (OPENGL_URL_GL_XML "https://cvs.khronos.org/svn/repos/ogl/trunk/doc/registry/public/api/gl.xml" CACHE STRING "Url to gl.xml file")
SET (OPENGL_VERSION "4.5" CACHE STRING "Version of OpenGL")

IF (NOT EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/gl.xml)
    FILE (DOWNLOAD ${OPENGL_URL_GL_XML} ${CMAKE_CURRENT_SOURCE_DIR}/gl.xml)
ENDIF()

ADD_CUSTOM_COMMAND (
    OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/gl.json
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/parse.py ${CMAKE_CURRENT_SOURCE_DIR}/gl.xml ${CMAKE_CURRENT_SOURCE_DIR}/gl.json
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/gl.xml)

ADD_CUSTOM_COMMAND (
    OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/white_list.json
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/command_list.py ${CMAKE_CURRENT_SOURCE_DIR}/gl.json ${CMAKE_CURRENT_SOURCE_DIR}/white_list.json ${OPENGL_VERSION}
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/gl.json)

ADD_CUSTOM_COMMAND (
    OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/gl.hpp ${CMAKE_CURRENT_SOURCE_DIR}/Gl_loader.cpp
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/generate.py ${CMAKE_CURRENT_SOURCE_DIR}/gl.json ${CMAKE_CURRENT_SOURCE_DIR}/white_list.json ${CMAKE_CURRENT_SOURCE_DIR}/gl.hpp ${CMAKE_CURRENT_SOURCE_DIR}/Gl_loader.cpp
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/white_list.json)

set_source_files_properties(gl.hpp GL_loader.cpp PROPERTIES GENERATED TRUE)

ADD_LIBRARY(OpenGL STATIC
			Context.cpp
			Context.hpp
			gl.hpp
			GL_loader.cpp
			PCH.cpp
			PCH.hpp)
            
