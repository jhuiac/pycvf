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



def lowpass(x,radius=10,smooth=5):
    dx=x.shape[0]
    dy=x.shape[1]
    dx2=dx//2
    dy2=dy//2
    g=numpy.mgrid[(-dx2):(dx-dx2),(-dy2):(dy-dy2)]
    gd=((g[0]**2+g[1]**2)**.5)
    g=(numpy.pi/2.+numpy.arctan((radius-gd)/smooth))/(numpy.pi)
    if (x.ndim==2):
      return g*x
    else:
      return g.reshape(x.shape[0],x.shape[1],1)*x  

Model=genericmodel.pycvf_model_function(image.Datatype,image.Datatype)(lowpass)
__call__=Model
                 
