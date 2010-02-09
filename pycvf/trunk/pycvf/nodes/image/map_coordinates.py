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


import numpy, sys,scipy.ndimage
from pycvf.core import genericmodel
from pycvf.datatypes import image


def all_layer(f,i):
    return numpy.dstack([f(i[:,:,l]) for l in range(i.shape[2])])

class map_coordinates():
    def __init__(self,expr="x/2.",centralized=True):
      self.lm=None
      self.expr=expr
      self.centralized=centralized
    def process(self,x):
      if ((self.lm==None) or (self.lm.shape[0])!=x.shape[0]*x.shape[1]):
        if (not self.centralized):
          lm=numpy.mgrid[0:1:(1./x.shape[0]),0:1:(1./x.shape[1])]
        else:
          lm=numpy.mgrid[-.5:.5:(1./x.shape[0]),-.5:.5:(1./x.shape[1])]
        cmap=eval(self.expr,{'x':(lm[0]*1J+lm[1]),'numpy':numpy,'scipy':scipy})
        if (not self.centralized):
          re=numpy.real(cmap)%1
          im=numpy.imag(cmap)%1
        else:
          re=(numpy.real(cmap)+.5)%1
          im=(numpy.imag(cmap)+.5)%1
        re*=x.shape[1]
        im*=x.shape[0]
        self.lm=numpy.dstack([im, re]).swapaxes(0,2).swapaxes(1,2)
      if (x.ndim==3):
        r=all_layer(lambda y :scipy.ndimage.map_coordinates(y,self.lm) ,x)
      else:
        r=scipy.ndimage.map_coordinates(x,self.lm)
      return r 


Model=genericmodel.pycvf_model_class(image.Datatype,image.Datatype)(map_coordinates)
__call__=Model
                 

