from setuptools import setup, Extension

ext = Extension('foo', ['foo.c'], extra_compile_args=['-std=c99'])
setup(name='example', ext_modules=[ext])
