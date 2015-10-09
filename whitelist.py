import gl
import json

class WhiteList :
	def __init__( self ) :
		self.commands = [];
		self.enums = [];
		
	def removeNotAllowed( self, gl ) :
		commands = [];
		enums = [];
		
		for command in gl.commands :
			if True == self.is_cmd_allowed( command.name ) :
				commands.append( command );
		
		for enum in gl.enums :
			if True == self.is_enum_allowed( enum.name ) :
				enums.append( enum );
		
		gl.commands = commands;
		gl.enums = enums;
		
	def is_cmd_allowed( self, name ) :
		for command in self.commands :
			if name == command :
				return True;
		
		return False;
		
	def is_enum_allowed( self, name ) :
		for enum in self.enums :
			if name == enum :
				return True;
		
		return False;
		
	def load( self, json_path ) :
		in_file = open( json_path, 'r' );
		
		data = json.load( in_file );
		self.commands = data[ 'commands' ];
		self.enums = data[ 'enums' ];
		
		in_file.close();
	
