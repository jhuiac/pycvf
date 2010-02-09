#!/bin/bash
# -*- coding: utf-8 -*-
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy.distutils.misc_util as nd                 

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension("pysash", ["pysash.pyx","Sash.cpp","DenseVecData.cpp","DenseArrayData.cpp","PythonVecData.cpp","mtrand.cpp"], language="c++",include_dirs=nd.get_numpy_include_dirs()),
                 ]
)
