from distutils.core import setup, Extension
from distutils.sysconfig import *
from distutils.util import *
from Cython.Distutils import build_ext
import numpy
import os
import os.path

try:
   from distutils.command.build_py import build_py_2to3 \
       as build_py
except ImportError:
   from distutils.command.build_py import build_py
   
try:
   from Cython.Distutils import build_ext
except ImportError:
   use_cython = False
else:
   use_cython = True
   

py_inc = [get_python_inc()]

np_lib = os.path.dirname(numpy.__file__)
np_inc = [os.path.join(np_lib, 'core/include')]
ext_inc = os

sourcefiles = ["utilFunctions.c", "cutilFunctions.pyx"]

# Fix "LNK1181: cannot open input file 'm.lib'" error under MSVC
# This removes the 'm' lib from all extensions under MSVC, as including it causes the build to fail
class build_ext_remove_m_library(build_ext):
   def build_extensions(self):
        if 'msvc' in self.compiler.compiler_type:
            for ext in self.extensions:
               ext.libraries.remove('m')
        build_ext.build_extensions(self)

setup(
    cmdclass = {'build_ext': build_ext_remove_m_library},
    ext_modules = [Extension("utilFunctions_C",sourcefiles, libraries=['m'], include_dirs=py_inc + np_inc)]
  )
