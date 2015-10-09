import gl
import xml.dom.minidom

class GLXML :
	def __init__( self ) :
		self.gl = gl.GL();
	
	def parseCommands( self, commands_node ) :
		command_list = commands_node.getElementsByTagName( "command" );
		
		for command_node in command_list :
			command = gl.Command();
			self.parseCommandNode( command_node, command );
			self.gl.commands.append( command );
	
	def parseParamNode( self, node, command ) :
		param = gl.Param();
		
		name = str();
		type = str();
		
		for child in node.childNodes :
			if xml.dom.Node.ELEMENT_NODE == child.nodeType :
				if "name" == child.nodeName :
					name = child.childNodes[0].nodeValue;
				elif "ptype" == child.nodeName :
					type += child.childNodes[0].nodeValue;
				else :
					print ("Not implemented: parseParamNode:")
					print (child.nodeName);
			if xml.dom.Node.TEXT_NODE == child.nodeType :
				type += child.nodeValue;
		
		param.name = name.strip();
		param.type = type.strip();
		
		command.params.append( param );
	
	def parseProtoNode( self, node, command ) :
		name = str();
		ret_type = str();
		
		for child in node.childNodes :
			if xml.dom.Node.ELEMENT_NODE == child.nodeType :
				if "name" == child.nodeName :
					name = child.childNodes[0].nodeValue;
				elif "ptype" == child.nodeName :
					ret_type += child.childNodes[0].nodeValue;
				else :
					print ("Not implemented: parseProtoNode:")
					print (child.nodeName);
			elif xml.dom.Node.TEXT_NODE == child.nodeType :
				ret_type += child.nodeValue;
				
		command.name = name.strip();
		command.ret_type = ret_type.strip();
	
	def parseCommandNode( self, node, command ) :
		if xml.dom.Node.ELEMENT_NODE == node.nodeType :
			if "proto" == node.nodeName :
				self.parseProtoNode( node, command );
			elif "param" == node.nodeName :
				self.parseParamNode( node, command );
			else :
				for child in node.childNodes :
					self.parseCommandNode( child, command );
	
	def parseEnumNode( self, node, enum ) :
		if True == node.hasAttributes() :
			attributes = node.attributes;
			for i in range(attributes.length) :
				attr = attributes.item(i);
				if "name" == attr.name :
					enum.name = attr.value;
				elif "value" == attr.name :
					enum.value = attr.value;
		
	def parseEnums ( self, enums_node ) :
		enum_list = enums_node.getElementsByTagName( "enum" );
		
		for enum_node in enum_list :
			enum = gl.Enum();
			self.parseEnumNode( enum_node, enum );
			self.gl.enums.append( enum );		
	
	def parseTypeNode ( self, node, type ) :
		if xml.dom.Node.TEXT_NODE == node.nodeType :
			type.text += node.nodeValue;
		elif xml.dom.Node.ELEMENT_NODE == node.nodeType :
			if "name" == node.nodeName :
				type.name = node.childNodes[0].nodeValue;
				type.text += type.name;
			else :
				children = node.childNodes;
				for child in children :
					self.parseTypeNode( child, type );
					
			if True == node.hasAttributes() :
				attributes = node.attributes;
				for i in range(attributes.length) :
					attr = attributes.item(i);
					if "name" == attr.name :
						type.name = attr.value;
					elif "api" == attr.name :
						type.api = attr.value;
					elif "requires" == attr.name :
						type.requires = attr.value;
	
	def parseTypes ( self, types_node ) :
		type_list = types_node.getElementsByTagName( "type" ); 
		
		for type_node in type_list :
			type = gl.Type();
			self.parseTypeNode( type_node, type );
			self.gl.types.append( type );
			
	def parseRemoveNode( self, node, feature ) :
		commands = node.getElementsByTagName( "command" );
		enums = node.getElementsByTagName( "enum" );
		
		for command in commands :
			attributes = command.attributes;
			name = "";
			
			for i in range(attributes.length) :
				attr = attributes.item(i);
				if "name" == attr.name :
					name = attr.value;
					
			feature.rem_commands.append( name );
		
		for enum in enums :
			attributes = enum.attributes;
			name = "";
			
			for i in range(attributes.length) :
				attr = attributes.item(i);
				if "name" == attr.name :
					name = attr.value;
					
			feature.rem_enums.append( name );
			
	def parseRequireNode( self, node, feature ) :
		commands = node.getElementsByTagName( "command" );
		enums = node.getElementsByTagName( "enum" );
		
		for command in commands :
			attributes = command.attributes;
			name = "";
			
			for i in range(attributes.length) :
				attr = attributes.item(i);
				if "name" == attr.name :
					name = attr.value;
					
			feature.req_commands.append( name );
		
		for enum in enums :
			attributes = enum.attributes;
			name = "";
			
			for i in range(attributes.length) :
				attr = attributes.item(i);
				if "name" == attr.name :
					name = attr.value;
					
			feature.req_enums.append( name );

	def parseExtensionNode( self, extension_node ) :
		extension = gl.Extension();
		
		if True == extension_node.hasAttributes() :
			attributes = extension_node.attributes;
			for i in range(attributes.length) :
				attr = attributes.item(i);
				if "name" == attr.name :
					extension.name = attr.value;
					
		require_list = extension_node.getElementsByTagName( "require" );
		
		for require in require_list :
			self.parseRequireNode( require, extension );
			
		self.gl.extensions.append( extension );

	def parseFeatureNode( self, feature_node ) :
		feature = gl.Feature();
		
		if True == feature_node.hasAttributes() :
			attributes = feature_node.attributes;
			for i in range(attributes.length) :
				attr = attributes.item(i);
				if "name" == attr.name :
					feature.name = attr.value;
				elif "api" == attr.name :
					feature.api = attr.value;
				elif "number" == attr.name :
					feature.number = float( attr.value );
					
		require_list = feature_node.getElementsByTagName( "require" );
		remove_list = feature_node.getElementsByTagName( "remove" );
		
		for require in require_list :
			self.parseRequireNode( require, feature );
			
		for remove in remove_list :
			self.parseRemoveNode( remove, feature );
			
		self.gl.features.append( feature );
		
		
	def parse( self, xml_path ) :
		doc = xml.dom.minidom.parse( xml_path );
		enums = doc.getElementsByTagName( "enums" );
		commands = doc.getElementsByTagName( "commands" );
		extensions_list = doc.getElementsByTagName( "extensions" );
		extension_list = extensions_list[0].getElementsByTagName( "extension" );
		feature_list = doc.getElementsByTagName( "feature" );
		types = doc.getElementsByTagName( "types" );
		
		self.parseCommands( commands[0] );
		for enums_node in enums :
			self.parseEnums( enums_node );
		for extension_node in extension_list :
			self.parseExtensionNode( extension_node );
		for feature_node in feature_list :
			self.parseFeatureNode( feature_node );
		self.parseTypes( types[0] );
