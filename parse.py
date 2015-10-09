import gl
import glxml
import gljson
import sys

doc_path = sys.argv[1];
out_path = sys.argv[2];

xml = glxml.GLXML();
xml.parse( doc_path );

gljson.write( xml.gl, out_path );
