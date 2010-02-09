#!/bin/bash
# -*- coding: utf-8 -*-
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy.distutils.misc_util as nd


BOOSTDIR="/home/tranx/include"
LSHKITDIR="lshkit"

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension("pylsh", ["pylsh.pyx","pylshbase.cpp"],include_dirs=[ ".",LSHKITDIR+"/include",BOOSTDIR]+nd.get_numpy_include_dirs(),
library_dirs = [LSHKITDIR+"/lib"] , libraries=["lshkit","gsl", "gslcblas","boost_program_options-mt"], language="c++"),
                 ]
)
