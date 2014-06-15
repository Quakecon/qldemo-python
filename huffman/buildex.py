from distutils.core import setup, Extension

setup( name="huffman", version="0.0", ext_modules = [ Extension( "huffman", ["pyhuffman.c", "huffman.c"] ) ] )

