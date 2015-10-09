import gl
import gljson
import json
import sys

in_path = sys.argv[1];
out_path = sys.argv[2];
number = float( sys.argv[3] );

names_of_extensions = [];
ext_number = len( sys.argv ) - 3;
for i in range( ext_number ) :
	names_of_extensions.append( sys.argv[3+ i] );

gl = gl.GL();
gljson.load( gl, in_path );

commands_list = [];
enums_list = [];

gl.features.sort( key = lambda feature: feature.number );

for feature in gl.features :
	if 'gl' != feature.api :
		continue;
	if number < feature.number :
		continue;
		
	print ('Add lvl: {}'.format( feature.name ));
	feature.add( commands_list, enums_list );
	
for extension in gl.extensions :
	if extension.name in names_of_extensions :
		print ('Add ext: {}'.format( extension.name ));
		extension.add( commands_list, enums_list );
	
commands_list.sort();
enums_list.sort();
		
dict = {
'commands':commands_list,
'enums':enums_list };

out_file = open( out_path, 'w' );
	
json.dump( dict,
		out_file,
		sort_keys=True,
		indent=4,
		separators=(',', ': ') );
		
out_file.close();
	