import gl
import json

class GLEncode( json.JSONEncoder ):
	def default( self, obj ) :
		if isinstance( obj, gl.GL ) :
			return obj.repr();
		else :
			return json.JSONEncoder.default( self, obj );
			
def load( gl, json_path ) :
	in_file = open( json_path, 'r' );
	
	data = json.load( in_file );
	gl.fromRepr( data );
	
	in_file.close();
	
def write( gl, json_path ) :
	out_file = open( json_path, 'w' );

	json.dump( gl,
		out_file,
		cls=GLEncode,
		sort_keys=True,
		indent=4,
		separators=(',', ': ') );
		
	out_file.close();
		