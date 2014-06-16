from setuptools import setup, Extension

m = Extension('huffman',
              sources = ['huffman/huffman.c','huffman/pyhuffman.c'],
              includes = ['huffman'])

setup (name = 'huffman',
       version = '0.1',
       description = 'This is a wrapper for the Q3A GPL Source Huffman code routines',
       ext_modules = [m],
       packages = ['huffman'],
       include_package_data = True,
       package_data = {'': ['*.h']},
)


