#Representation of gl.xml files


		
class Command :
	def __init__( self ) :
		self.name = "";
		self.ret_type = "";
		self.params = [];
		
	def fromRepr( self, dict ) :
		self.name = dict['name'];
		self.ret_type = dict['ret_type'];
		params_repr = dict['params'];
		
		for param_repr in params_repr :
			param = Param();
			param.fromRepr( param_repr );
			self.params.append( param );
		
	def repr_params( self ) :
		params_repr = [];
				
		for param in self.params :
			params_repr.append( param.repr() );
			
		return params_repr;
		
	def repr( self ) :
		return {
			'name':self.name,
			'ret_type':self.ret_type,
			'params':self.repr_params() };				

class Enum :
	def __init__( self ) :
		self.name = "";
		self.value = "";
		
	def fromRepr( self, dict ) :
		self.name = dict['name'];
		self.value = dict['value'];
		
	def repr( self ) :
		return {
			'name':self.name,
			'value':self.value };		

class Extension :
	def __init__( self ) :
		self.name = ""
		self.req_commands = [];
		self.req_enums = [];
		
	def fromRepr( self, dict ) :
		self.name = dict['name'];
		self.req_commands = dict['required_commands'];
		self.req_enums = dict['required_enums'];
		
	def repr( self ) :
		return {
			'name':self.name,
			'required_commands':self.req_commands,
			'required_enums':self.req_enums };
			
	def add( self, commands, enums ) :			
		for req_command in self.req_commands :
			commands.append( req_command );

		for req_enum in self.req_enums :
			enums.append( req_enum );
	
class Feature :
	def __init__( self ) :
		self.api = "";
		self.name = "";
		self.number = 0;
		self.rem_commands = [];
		self.rem_enums = [];
		self.req_commands = [];
		self.req_enums = [];
		
	def fromRepr( self, dict ) :
		self.api = dict['api'];
		self.name = dict['name'];
		self.number = dict['number'];
		self.rem_commands = dict['removed_commands'];
		self.rem_enums = dict['removed_enums'];
		self.req_commands = dict['required_commands'];
		self.req_enums = dict['required_enums'];
		
	def repr( self ) :
		return {
			'api':self.api,
			'name':self.name,
			'number':self.number,
			'removed_commands':self.rem_commands,
			'removed_enums':self.rem_enums,
			'required_commands':self.req_commands,
			'required_enums':self.req_enums };
			
	def add( self, commands, enums ) :
		for rem_command in self.rem_commands :
			commands.remove( rem_command );
			
		for req_command in self.req_commands :
			commands.append( req_command );

		for rem_enum in self.rem_enums :
			enums.remove( rem_enum );

		for req_enum in self.req_enums :
			enums.append( req_enum );

class Param :
	def __init__( self ) :
		self.name = "";
		self.type = "";
		
	def repr( self ) :
		return {
			'name':self.name,
			'type':self.type };
			
	def fromRepr( self, dict ) :
		self.name = dict['name'];
		self.type = dict['type'];
		
class Type :
	def __init__(self) :
		self.text = "";
		self.name = "";
		self.comment = "";
		self.api = "";
		self.requires = "";
		
	def fromRepr( self, dict ) :
		self.name = dict['name'];
		self.text = dict['text'];
		self.comment = dict['comment'];
		self.api = dict['api'];
		self.requires = dict['requires'];
		
	def repr( self ) :
		return {
			'api':self.api,
			'comment':self.comment,
			'name':self.name,
			'requires':self.requires,
			'text':self.text };
		
class GL :
	def __init__( self ) :
		self.commands = [];
		self.enums = [];
		self.extensions = [];
		self.features = [];
		self.types = [];
		
	def fromRepr( self, dict ) :
		commands_repr = dict['commands'];
		enums_repr = dict['enums'];
		extensions_repr = dict['extensions'];
		features_repr = dict['features'];
		types_repr = dict['types'];
		
		for command_repr in commands_repr :
			command = Command();
			command.fromRepr( command_repr );
			self.commands.append( command );
		
		for enum_repr in enums_repr :
			enum = Enum();
			enum.fromRepr( enum_repr );
			self.enums.append( enum );
			
		for extension_repr in extensions_repr :
			extension = Extension();
			extension.fromRepr( extension_repr );
			self.extensions.append( extension );
			
		for feature_repr in features_repr :
			feature = Feature();
			feature.fromRepr( feature_repr );
			self.features.append( feature );
		
		for type_repr in types_repr :
			type = Type();
			type.fromRepr( type_repr );
			self.types.append( type );
		
	def repr( self ) :
		commands_repr = [];
		enums_repr = [];
		extensions_repr = [];
		features_repr = [];
		types_repr = [];
		
		for command in self.commands :
			commands_repr.append( command.repr() );
			
		for enum in self.enums :
			enums_repr.append( enum.repr() );
			
		for extension in self.extensions :
			extensions_repr.append( extension.repr() );
			
		for feature in self.features :
			features_repr.append( feature.repr() );
			
		for type in self.types :
			types_repr.append( type.repr() );
			
		return {
		'commands':commands_repr,
		'enums':enums_repr,
		'extensions':extensions_repr,
		'features':features_repr,
		'types':types_repr };
		