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

def ddif(x,y):
    dpi=(2*numpy.pi)
    z=((((x-y)%dpi)+dpi)%dpi)
    z[z>numpy.pi]-=dpi
    return abs(z)

def orient_filter(x,value=0,smooth=0.08,oneside=False):
    dx=x.shape[0]
    dy=x.shape[1]
    dx2=dx//2
    dy2=dy//2
    g=numpy.mgrid[(-dx2):(dx-dx2),(-dy2):(dy-dy2)]
    gd=numpy.angle(g[0]+g[1]*1J)
    if (oneside):
       g=((numpy.pi/2.)-numpy.arctan(ddif(gd,value)/smooth))/(numpy.pi/2.)
    else:
       g=((numpy.pi/2.)-numpy.arctan(ddif(gd,value)/smooth))/(numpy.pi/2.)+((numpy.pi/2.)-numpy.arctan(ddif(gd,(value+numpy.pi))/smooth))/(numpy.pi/2.)
    if (x.ndim==2):
      return g*x
    else:
      return g.reshape(x.shape[0],x.shape[1],1)*x  

Model=genericmodel.pycvf_model_function(image.Datatype,image.Datatype)(orient_filter)
__call__=Model
                 
