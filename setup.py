from setuptools import setup, Extension, find_packages

m = Extension('huffman',
              sources = ['huffman/huffman.c','huffman/pyhuffman.c'],
              includes = ['huffman'])

setup (name = 'ql-demo-json',
       version = '0.1',
       ext_modules = [m],
       packages = ['huffman'],
       package_data = {'': ['*.h']},
       scripts = ['demo.py'],
       author = "Shawn Nock",
       author_email = "nock@nocko.se",
       description = "This package converts Quakelive Demo files in JSON",
       license = "GPLv3",
       keywords = "quake quakelive demo dm_73 quakecon",
       url = "https://aphr.asia/gitweb/?p=qldemo-python.git;a=summary"
)


