# -*- coding: utf-8 -*-
#########################################################################################################################################
#
# MyModel By Bertrand NOUVEL
# 2009 CNRS Postdoctorate JFLI
#
# (c) All rights reserved
# ###############################################
#
################################################################################################################################################################################
# Includes
################################################################################################################################################################################


import numpy, sys
from pycvf.core import genericmodel
from pycvf.datatypes import image


def DoH(I):
      """ Determinant of Hessian """
      Ix =  scipy.diff(Ix,axis=0)
      Iy =  scipy.diff(Iy,axis=0)
      Ixx = scipy.diff(Ix,axis=0)
      Iyy = scipy.diff(Iy,axis=1)
      Ixy = scipy.diff(Ix,axis=1)
      return Ixx*Iyy-Ixy*Iyx     

Model=genericmodel.pycvf_model_function(image.Datatype,image.Datatype)(jacobian)
__call__=Model
                 
