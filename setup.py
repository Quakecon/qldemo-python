from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, Extension

m = Extension('huffman',
              sources = ['huffman/huffman.c','huffman/pyhuffman.c'],
              includes = ['huffman'])

setup (name = 'huffman',
       version = '0.1',
       description = 'This is a wrapper for the Q3A GPL Source Huffman code routines',
       ext_modules = [m])


