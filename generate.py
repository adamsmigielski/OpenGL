import gl
import gljson
import sys
import whitelist
import os.path
	
def beginFunctions( file ) :
	file.write (
	'    /* Entry points */\n'
	'    struct Functions\n'
	'    {\n' );

def beginGuardian( file, name ) :
	path, file_name = os.path.split(name)
	guardian = "O8_OPENGL_" + file_name.replace( '.', '_' );
	file.write (
	'#ifndef {}\n'
	'#define {}\n'
	'\n'.format( guardian.upper(), guardian.upper() ) );
	
def beginLoadGL( file ) :
	file.write(
	'    void LoadGL(Context & context)\n'
	'    {\n'
	'        Functions & gl = context.m_gl_functions;\n'
	'\n');
	
def beginNamespace( file ) :
	file.write (
	'namespace OpenGL\n'
	'{\n' );
	
def convertParamType( type_str ) :
	type = str();
	result = str();
	split = type_str.split();
	type_index = 0;
	
	if "const" == split[0] :
		type_index = 1;
	elif "struct" == split[0]:
		type_index = 1;
		split[0] = "";
		
	type = split[type_index];
	
	result = convertType( type );
		
	split[type_index] = result;
	
	result = "";
	for word in split :
		result += word;
		if ((word) and (word != split[-1])) :
			result += " ";
		
	return result;

def convertType( type ) :
	result = str();
	
	if "GLenum" == type :
		result = "Platform::uint32";
	elif "GLboolean" == type :
		result = "Platform::uint8";
	elif "GLbitfield" == type :
		result = "Platform::uint32";
	elif "GLvoid" == type :
		result = "void";
	elif "GLbyte" == type :
		result = "Platform::int8";
	elif "GLshort" == type :
		result = "Platform::int16";
	elif "GLint" == type :
		result = "Platform::int32";
	elif "GLclampx" == type :
		result = "Platform::int32";
	elif "GLubyte" == type :
		result = "Platform::uint8";
	elif "GLushort" == type :
		result = "Platform::uint16";
	elif "GLuint" == type :
		result = "Platform::uint32";
	elif "GLsizei" == type :
		result = "Platform::int32";
	elif "GLfloat" == type :
		result = "float";
	elif "GLclampf" == type :
		result = "float";
	elif "GLdouble" == type :
		result = "double";
	elif "GLclampd" == type :
		result = "double";
	elif "GLeglImageOES" == type :
		result = "void *";
	elif "GLchar" == type :
		result = "char";
	elif "GLcharARB" == type :
		result = "char";
	elif "GLhandleARB" == type :
		result = "void *";
	elif "GLhalfARB" == type :
		result = "Platform::uint16";
	elif "GLhalf" == type :
		result = "Platform::uint16";
	elif "GLhalfNV" == type :
		result = "Platform::uint16";
	elif "GLfixed" == type :
		result = "Platform::int32";
	elif "GLintptr" == type :
		result = "ptrdiff_t";
	elif "GLsizeiptr" == type :
		result = "ptrdiff_t";
	elif "GLint64" == type :
		result = "Platform::int64";
	elif "GLuint64" == type :
		result = "Platform::uint64";
	elif "GLintptrARB" == type :
		result = "ptrdiff_t";
	elif "GLsizeiptrARB" == type :
		result = "ptrdiff_t";
	elif "GLint64EXT" == type :
		result = "Platform::int64";
	elif "GLuint64EXT" == type :
		result = "Platform::uint64";
	elif "GLsync" == type :
		result = "void *";
	elif "_cl_context" == type :
		result = "void";
	elif "_cl_event" == type :
		result = "void";
	elif "GLvdpauSurfaceNV" == type :
		result = "Platform::int32 *";
	else :
		if (("void" != type) and
			("GLDEBUGPROC" != type) and
			("GLDEBUGPROCARB" != type) and
			("GLDEBUGPROCKHR" != type) and
			("GLDEBUGPROCAMD" != type)) :
			print ('Convert warning: |{}|'.format( type_str ));
		result = type;
		
	return result;
	
def endFunctions( file ) :
	file.write (
	'    };\n' );
	
def endGuardian( file, name ) :
	path, file_name = os.path.split(name)
	guardian = "O8_OPENGL_" + file_name;
	file.write (
	'\n'
	'#endif /* {} */\n'
	'\n'.format( guardian.upper() ) );
	
def endLoadGL( file ) :
	file.write(
	'    }\n' );
	
def endNamespace( file ) :
	file.write (
	'} /* namespace OpenGL */\n');
	
def writeCommandEntryPoints( file, gl ) :
	max_name_length = 0;
	
	for command in gl.commands :
		length = len(command.name);
		if max_name_length < length :
			max_name_length = length;
			
	max_name_length += 1;
			
	for command in gl.commands :
		name = command.name;
		length = len(name);		
		type = "PFN_" + command.name.upper();
		
		fill_len = max_name_length - length;
		
		file.write( '            ' );
		file.write( type );
		file.write( ' ' * fill_len );
		file.write( command.name[2:] );
		file.write( ';\n' );
		
def writeCommandLoad( file, gl ) :
	max_name_length = 0;
	
	for command in gl.commands :
		length = len(command.name);
		if max_name_length < length :
			max_name_length = length;
			
	max_name_length += 1;
			
	for command in gl.commands :
		name = command.name;
		length = len(name);		
		type = "PFN_" + command.name.upper();
		
		fill_len = max_name_length - length;
		
		file.write( '            gl.' );
		file.write( command.name[2:] );
		file.write( ' ' * fill_len );
		file.write( '= (' );
		file.write( type );
		file.write( ')' );
		file.write( ' ' * fill_len );
		file.write( 'load_function(context, "' );
		file.write( command.name );
		file.write( '");\n' );
	
def writeCommandTypedefs( file, gl ) :
	file.write( '    /* Prototypes */\n' );
	
	for command in gl.commands :
		name = "PFN_" + command.name.upper();
		ret_type = convertParamType(command.ret_type);
		
		file.write( '    typedef ' );
		file.write( ret_type );
		file.write( ' (OPEN_GL_API * ' );
		file.write( name );
		file.write( ')(' );
		
		for param in command.params :
			type = convertParamType(param.type);
			file.write( '\n            ' );
			file.write( type );
			file.write( ' ' );
			file.write( param.name );
			
			if param != command.params[-1] :
				file.write( ',' );
		
		file.write( ');\n');
			
	file.write( '\n    /* End of prototypes */\n\n' );
	
def writeDefines( file ) :
	file.write( '    /* Defines */\n');
	file.write( '    #define OPEN_GL_API __stdcall\n\n');
	file.write( '    /* End of defines */\n');

def writeEnums( file, gl ) :
	file.write( '    /* GLenums */\n' );
	max_name_length = 0;
	
	for enum in gl.enums :
		length = len(enum.name);
		if max_name_length < length :
			max_name_length = length;
			
	max_name_length += 1;
			
	for enum in gl.enums :
		name = enum.name;
		length = len(name);
		
		fill_len = max_name_length - length;
		
		file.write( '    #define ' );
		file.write( enum.name );
		file.write( ' ' * fill_len );
		file.write( enum.value );
		file.write( '\n' );
			
	file.write( '\n    /* End of GLenums */\n\n' );
	
def writeIncludes( file ) :
	file.write(
	'#include "PCH.hpp"\n'
	'\n'
	'#include "Context.hpp"\n'
	'#include "gl.hpp"\n'
	'\n' );

def writeLicense( file ) :
	file.write (
	'/** License\n'
	' *\n'
	' * This file was generated from file gl.xml, which is copyrighted by Khronos Group Inc.\n'
	' *\n'
	' *\n'
	' *  Permission is hereby granted, free of charge, to any person obtaining a\n'
	' *      copy of this software and associated documentation files (the\n'
	' *      "Software"), to deal in the Software without restriction, including\n'
	' *      without limitation the rights to use, copy, modify, merge, publish,\n'
	' *      distribute, sublicense, and/or sell copies of the Software, and to\n'
	' *      permit persons to whom the Software is furnished to do so, subject to\n'
	' *      the following conditions: The above copyright notice and this permission\n'
	' *      notice shall be included in all copies or substantial portions of the\n'
	' *      Software.\n'
	' *\n'
	' *\n'
	' *  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS\n'
	' *      OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF\n'
	' *      MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.\n'
	' *      IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY\n'
	' *      CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,\n'
	' *      TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE\n'
	' *      SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n'
	' *\n'
	' **/\n'
	'\n' );
	
def writeLoadFunction( file ) :
	file.write(
	'    void * load_function(\n'
	'        Context & context,\n'
	'        const char * name)\n'
	'    {\n'
	'        void * ptr = context.Get_proc_address(name);\n'
	'\n'
	'#if DEBUG\n'
	'        if (nullptr == ptr)\n'
	'        {\n'
	'            DEBUGLOG("Not available: " << name);\n'
	'        }\n'
	'#endif /* DEBUG */\n'
	'    \n'
	'        return ptr;\n'
	'    }\n'
	'\n' );

def writeTypes( file, gl ) :
	file.write( '    /* Typedefs */\n' );
	
	types = "";
	
	for type in gl.types :
		if (("GLDEBUGPROC" == type.name) or
			("GLDEBUGPROCARB" == type.name) or
			("GLDEBUGPROCKHR" == type.name) or
			("GLDEBUGPROCAMD" == type.name) ) :
			closing_idx = type.text.index( ')' );
			args_beg = type.text[closing_idx + 1:].index( '(' ) + closing_idx + 2;
			args_end = type.text[closing_idx + 1:].index( ')' ) + closing_idx + 1;
			args = type.text[args_beg:args_end].split( ',' );
			
			text = type.text[0:args_beg];
			for arg in args :
				converted = convertParamType( arg );
				text += converted;
				if arg != args[-1]:
					text += ', ';
			text += type.text[args_end:];
			
			types += "        ";
			types += text;
			types += '\n';
			
	file.write( types );
			
	file.write( '\n    /* End of typedefs */\n\n' );

in_path = sys.argv[1];
wl_path = sys.argv[2]
gl_header_path = sys.argv[3];
gl_loader_path = sys.argv[4];

gl = gl.GL();
wl = whitelist.WhiteList();

gljson.load( gl, in_path );
wl.load( wl_path );
wl.removeNotAllowed( gl );

gl_header_file = open( gl_header_path, 'w' );

writeLicense( gl_header_file );
beginGuardian( gl_header_file, gl_header_path );
beginNamespace( gl_header_file );
writeDefines( gl_header_file );
writeTypes( gl_header_file, gl );
writeEnums( gl_header_file, gl );
writeCommandTypedefs( gl_header_file, gl );
beginFunctions( gl_header_file );
writeCommandEntryPoints( gl_header_file, gl );
endFunctions( gl_header_file );
endNamespace( gl_header_file );
endGuardian( gl_header_file, gl_header_path );

gl_header_file.close();

gl_loader_file = open( gl_loader_path, 'w' );

writeLicense( gl_loader_file );
writeIncludes( gl_loader_file );
beginNamespace( gl_loader_file );
writeLoadFunction( gl_loader_file );
beginLoadGL( gl_loader_file );
writeCommandLoad( gl_loader_file, gl );
endLoadGL( gl_loader_file );
endNamespace( gl_loader_file );

gl_loader_file.close();