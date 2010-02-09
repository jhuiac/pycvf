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


import numpy, scipy,sys
from pycvf.core import genericmodel
from pycvf.datatypes import basics
from pycvf.datatypes import image
from pycvf.datatypes import histogram
#from jfli import stats.models

##
## This is simply a color model that is to apply by filtering
##

def HOG(img,bins=16,normed=True):
  print type(img), img.shape
  r=scipy.gradient(img.squeeze())
  r=numpy.angle(r[0]+1J*r[1])
  return numpy.histogram(img,bins,normed=normed)[0]

class Model(genericmodel.Model):
        def input_datatype(self,x):
            #assert(isinstance(x,image.Datatype)), (str(type(x)) , "is not an image")
            return image.Datatype
        def output_datatype(self,x):
            return histogram.Datatype
        def init_model(self,*args, **kwargs):
              self.processing=[ ('HOG' , {'HOG':HOG })]

__call__=Model
