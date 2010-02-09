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


import numpy
from pycvf.core import genericmodel
from pycvf.datatypes import basics
from pycvf.datatypes import image
#from jfli import stats.models

##
## This is simply a color model that is to apply by filtering
##

class Model(genericmodel.GenericModel):
        input_datatype=lambda self,x:image.Datatype
        datatype=lambda self,x:image.Datatype
	def init(self,postfilter=None,centered=True):
           if (postfilter!=None):
              self.postfilter=eval(postfilter)
           else:
              self.postfilter=None    
           self.centered=centered
           genericmodel.GenericModel.init(self)
        def fftcenter(self,x):
            if (self.centered):
               return numpy.roll(numpy.roll(x,x.shape[0]//2,axis=0),x.shape[1]//2,axis=1)
            else: 
               return x
        def dofft2(self,x):
            if (x.ndim==3):
              assert(x.shape[2]==1)
              x=x.reshape(x.shape[0],x.shape[1])
            if (self.postfilter!=None):
              return self.postfilter(self.fftcenter(numpy.fft.fft2(x))).reshape(x.shape[0],x.shape[1],1)
            else:
              return numpy.fft.fft2(self.fftcenter(x)).reshape(x.shape[0],x.shape[1],1)
        def init_featurefilter(self):
              self.featurefilter=('src|fft2'  ,{'fft2':self.dofft2},  {})
        def init_structures(self):
              return {}

__call__=Model           