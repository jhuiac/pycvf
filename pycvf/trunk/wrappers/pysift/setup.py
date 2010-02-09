# -*- coding: utf-8 -*-
from distutils.core import setup, Extension
import numpy.distutils.misc_util as nd


module1 = Extension('sift',
                    sources = ['sift.cpp','siftmodule.cpp'], include_dirs=nd.get_numpy_include_dirs())

setup (name = 'pysift',
       version = '0.1',
       description = 'Py SIFT keypoints detectors',
       ext_modules = [module1]
       )
